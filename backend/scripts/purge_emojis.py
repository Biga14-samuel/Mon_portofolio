#!/usr/bin/env python3
"""Purge emojis from text fields in the database.

Usage:
  python purge_emojis.py         # dry-run, shows counts and examples
  python purge_emojis.py --apply # apply changes to the DB

This script is safe by default (dry-run). It supports SQLite and Postgres via the project's DB config.
"""
import re
import argparse
from pprint import pprint

from app.database import SessionLocal
from app.models import Item, Tag, Testimonial

# Broad emoji/pictograph ranges
EMOJI_RE = re.compile(
    r'['
    r'\U0001F300-\U0001F5FF'  # symbols & pictographs
    r'\U0001F600-\U0001F64F'  # emoticons
    r'\U0001F680-\U0001F6FF'  # transport & map
    r'\U0001F1E0-\U0001F1FF'  # flags
    r'\U00002700-\U000027BF'  # dingbats
    r'\U00002600-\U000026FF'  # misc symbols
    r'\U0000FE00-\U0000FE0F'  # variation selectors
    r'\U0001F900-\U0001F9FF'  # supplemental symbols and pictographs
    r'\U0000200D'              # zero width joiner
    r']+', flags=re.UNICODE)

VARIATION_SELECTORS = re.compile(r"[\uFE0E\uFE0F]")


def strip_emojis(text: str | None) -> str | None:
    if text is None:
        return None
    s = str(text)
    s = EMOJI_RE.sub('', s)
    s = VARIATION_SELECTORS.sub('', s)
    return s.strip()


def process_items(session, apply: bool):
    items = session.query(Item).all()
    changed = 0
    samples = []
    for it in items:
        orig = {
            'title': it.title,
            'subtitle': it.subtitle,
            'description': it.description,
            'category': it.category,
        }
        cleaned = {k: strip_emojis(v) for k, v in orig.items()}
        if any((cleaned[k] != orig[k] for k in orig)):
            changed += 1
            samples.append({'id': it.id, 'before': orig, 'after': cleaned})
            if apply:
                it.title = cleaned['title'] or it.title
                it.subtitle = cleaned['subtitle'] or it.subtitle
                it.description = cleaned['description'] or it.description
                it.category = cleaned['category'] or it.category
    return changed, samples


def process_tags(session, apply: bool):
    tags = session.query(Tag).all()
    changed = 0
    samples = []
    for t in tags:
        orig = {'name': t.name}
        cleaned = {'name': strip_emojis(t.name)}
        if cleaned['name'] != t.name:
            changed += 1
            samples.append({'id': t.id, 'before': t.name, 'after': cleaned['name']})
            if apply:
                t.name = cleaned['name'] or t.name
    return changed, samples


def process_testimonials(session, apply: bool):
    tests = session.query(Testimonial).all()
    changed = 0
    samples = []
    for tt in tests:
        orig = {'client_name': tt.client_name, 'client_company': tt.client_company, 'content': tt.content}
        cleaned = {k: strip_emojis(v) for k, v in orig.items()}
        if any((cleaned[k] != orig[k] for k in orig)):
            changed += 1
            samples.append({'id': tt.id, 'before': orig, 'after': cleaned})
            if apply:
                tt.client_name = cleaned['client_name'] or tt.client_name
                tt.client_company = cleaned['client_company'] or tt.client_company
                tt.content = cleaned['content'] or tt.content
    return changed, samples


def main():
    parser = argparse.ArgumentParser(description='Purge emojis in DB text fields')
    parser.add_argument('--apply', action='store_true', help='Apply changes to the database')

    args = parser.parse_args()
    apply = args.apply

    session = SessionLocal()
    try:
        print('Scanning DB for emoji occurrences (dry-run={})...'.format(not apply))
        items_changed, item_samples = process_items(session, apply)
        tags_changed, tag_samples = process_tags(session, apply)
        tests_changed, test_samples = process_testimonials(session, apply)

        print('\nSummary:')
        print(f'  Items affected: {items_changed}')
        print(f'  Tags affected: {tags_changed}')
        print(f'  Testimonials affected: {tests_changed}')

        if item_samples:
            print('\nItem samples:')
            pprint(item_samples[:5])
        if tag_samples:
            print('\nTag samples:')
            pprint(tag_samples[:5])
        if test_samples:
            print('\nTestimonial samples:')
            pprint(test_samples[:5])

        if apply:
            session.commit()
            print('\nChanges applied and committed.')
        else:
            session.rollback()
            print('\nDry-run complete. No changes were written. Rerun with --apply to apply.')

    finally:
        session.close()


if __name__ == '__main__':
    main()
