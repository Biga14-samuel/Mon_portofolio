#!/usr/bin/env python3
"""Upsert the five certification parcours entries in chronological order.
Run with the project's venv and PYTHONPATH set to backend.
"""
from app.database import SessionLocal
from app.models import Item, Tag

TAGS = [
    'Marketing',
    'Entrepreneuriat',
    'Cybersécurité',
    'Réseaux',
    'Sécurité Réseau',
]

CERTIFICATIONS = [
    {
        'display_order': 11,
        'title': 'Certification — Marketing Digital',
        'subtitle': '2024 | Obtenue',
        'category': 'Marketing',
        'description': "Acquisition des bases du marketing digital, de la stratégie de contenu et du développement de la présence en ligne.",
        'content': {
            'objective': 'Comprendre les fondamentaux du marketing digital et appliquer une stratégie de visibilité cohérente.',
            'tools': 'Marketing, Contenu, Présence en ligne',
            'architecture': (
                '- Construction d’un plan éditorial orienté visibilité.\n'
                '- Mise en pratique des leviers de communication digitale et de contenu.\n'
                '- Suivi des bonnes pratiques de présence en ligne.'
            ),
            'alert_flow': None,
            'lessons': (
                '- Structurer une présence digitale plus claire et plus lisible.\n'
                '- Adapter le contenu à un objectif de visibilité et d’engagement.'
            ),
            'impact': 'Certification obtenue en 2024, consolidant les bases du marketing digital.'
        },
    },
    {
        'display_order': 12,
        'title': 'Certification — Entrepreneuriat',
        'subtitle': '2024 | MIU (Obtenue)',
        'category': 'Entrepreneuriat',
        'description': "Certification sur la création d'entreprise, la modélisation économique (Business Plan, SWOT) et la gestion de projet.",
        'content': {
            'objective': 'Comprendre les ressorts de la création d’entreprise et de la structuration d’un projet viable.',
            'tools': 'Business Plan, SWOT, Gestion de projet',
            'architecture': (
                '- Étude du besoin, positionnement et proposition de valeur.\n'
                '- Construction d’un business plan simplifié et analyse SWOT.\n'
                '- Organisation du projet et suivi des étapes de mise en œuvre.'
            ),
            'alert_flow': None,
            'lessons': (
                '- Formaliser une idée en projet exploitable.\n'
                '- Relier la technique, la gestion et la logique de valeur.'
            ),
            'impact': 'Certification obtenue en 2024, renforçant la capacité à structurer un projet.'
        },
    },
    {
        'display_order': 13,
        'title': 'Certification — Ethical Hacking (Hacker Éthique)',
        'subtitle': '2026 | Cisco NetAcad & Credly (Obtenue)',
        'category': 'Cybersécurité',
        'description': "Maîtrise des concepts de hacking éthique, exécution des techniques de post-exploitation, analyse de vulnérabilités et sécurité du Cloud/IoT.",
        'content': {
            'objective': 'Approfondir les techniques de sécurité offensive et la compréhension des vulnérabilités.',
            'tools': 'Cybersécurité, Hacking éthique, Cloud, IoT',
            'architecture': (
                '- Découverte des étapes d’une démarche d’hacking éthique.\n'
                '- Analyse des vulnérabilités et des vecteurs d’exploitation.\n'
                '- Approche des enjeux Cloud et IoT dans un contexte de sécurité.'
            ),
            'alert_flow': None,
            'lessons': (
                '- Lire une surface d’attaque avec une logique méthodique.\n'
                '- Mieux relier la prévention, l’analyse et la remédiation.'
            ),
            'impact': 'Certification obtenue en 2026, validée par Cisco NetAcad et Credly.'
        },
    },
    {
        'display_order': 14,
        'title': "CCNA — Routage, Switching & Réseautage d'entreprise",
        'subtitle': '2026 | Cisco NetAcad (En cours)',
        'category': 'Réseaux',
        'description': "Formation approfondie sur les essentiels de la commutation, le routage, la sécurité des infrastructures LAN/WLAN et l'automatisation réseau.",
        'content': {
            'objective': 'Renforcer les bases réseau sur le routage, la commutation et l’architecture d’entreprise.',
            'tools': 'Routage, Switching, LAN, WLAN, Automatisation',
            'architecture': (
                '- Étude des mécanismes de routage et de switching.\n'
                '- Sécurisation des infrastructures LAN et WLAN.\n'
                '- Introduction à l’automatisation réseau et aux pratiques d’entreprise.'
            ),
            'alert_flow': None,
            'lessons': (
                '- Consolider la logique réseau de bout en bout.\n'
                '- Préparer la mise en œuvre de réseaux plus robustes et plus automatisés.'
            ),
            'impact': 'Certification en cours en 2026 au sein de Cisco NetAcad.'
        },
    },
    {
        'display_order': 15,
        'title': 'Certification — Sécurité des réseaux en entreprise & Défense du réseau',
        'subtitle': '2026 | Cisco NetAcad (En cours)',
        'category': 'Sécurité Réseau',
        'description': "Apprentissage des techniques de surveillance réseau, de défense périmétrique, de sécurisation des flux et de gestion des alertes de sécurité.",
        'content': {
            'objective': 'Approfondir la défense réseau et la surveillance des incidents dans un contexte d’entreprise.',
            'tools': 'Surveillance réseau, Défense périmétrique, Alertes',
            'architecture': (
                '- Analyse des flux et de la posture de défense du réseau.\n'
                '- Sécurisation périmétrique et gestion des alertes.\n'
                '- Mise en pratique des techniques de surveillance et de réponse.'
            ),
            'alert_flow': None,
            'lessons': (
                '- Développer une lecture défensive du réseau.\n'
                '- Construire des réflexes de surveillance et de protection des services.'
            ),
            'impact': 'Certification en cours en 2026 au sein de Cisco NetAcad.'
        },
    },
]


def upsert_tag(session, tag_name):
    tag = session.query(Tag).filter(Tag.type == 'parcours', Tag.name == tag_name).one_or_none()
    if tag is None:
        tag = Tag(type='parcours', name=tag_name)
        session.add(tag)


def upsert_item(session, payload):
    item = session.query(Item).filter(Item.type == 'parcours', Item.title == payload['title']).one_or_none()
    if item is None:
        item = Item(type='parcours')
        session.add(item)

    item.category = payload['category']
    item.featured = False
    item.display_order = payload['display_order']
    item.title = payload['title']
    item.subtitle = payload['subtitle']
    item.description = payload['description']
    item.github_url = None
    item.demo_url = None
    item.image_url = None
    item.content = payload['content']


session = SessionLocal()
try:
    for tag_name in TAGS:
        upsert_tag(session, tag_name)

    for payload in CERTIFICATIONS:
        upsert_item(session, payload)

    session.commit()
    print(f"Upserted {len(CERTIFICATIONS)} certification items and {len(TAGS)} tags.")
finally:
    session.close()
