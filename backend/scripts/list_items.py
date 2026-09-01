#!/usr/bin/env python3
"""List items in DB for debugging.

Usage: python list_items.py
"""
import logging
from pprint import pformat
from app.database import SessionLocal
from app.models import Item

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

session = SessionLocal()
try:
    items = session.query(Item).order_by(Item.id).all()
    logger.info("Found %d items:\n", len(items))
    for it in items:
        logger.info(pformat({
            'id': it.id,
            'type': it.type,
            'category': it.category,
            'title': it.title,
            'subtitle': it.subtitle,
            'description': it.description[:200] if it.description else None,
            'display_order': it.display_order,
            'featured': it.featured,
            'created_at': str(it.created_at),
        }))
finally:
    session.close()
