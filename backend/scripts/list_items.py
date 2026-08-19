#!/usr/bin/env python3
"""List items in DB for debugging.

Usage: python list_items.py
"""
from pprint import pprint
from app.database import SessionLocal
from app.models import Item

session = SessionLocal()
try:
    items = session.query(Item).order_by(Item.id).all()
    print(f"Found {len(items)} items:\n")
    for it in items:
        pprint({
            'id': it.id,
            'type': it.type,
            'category': it.category,
            'title': it.title,
            'subtitle': it.subtitle,
            'description': it.description[:200] if it.description else None,
            'display_order': it.display_order,
            'featured': it.featured,
            'created_at': str(it.created_at),
        })
        print('\n')
finally:
    session.close()
