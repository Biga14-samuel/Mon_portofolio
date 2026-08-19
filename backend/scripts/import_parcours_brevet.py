#!/usr/bin/env python3
"""Import a single 'Parcours' item: Brevet de Technicien (2020).
Run with the project's venv and PYTHONPATH set to backend.
"""
from datetime import datetime
from app.database import SessionLocal
from app.models import Item

session = SessionLocal()
try:
    item = Item(
        type='parcours',
        category='Formation',
        featured=False,
        display_order=1,
        title='Brevet de Technicien — Maintenance Hospitalière & Biomédicale',
        subtitle='2020 | Lycée technique et bilingue de Nkolbisson',
        description=(
            "Obtention du diplôme de Brevet de Technicien, marquant le début du parcours "
            "technique avec un apprentissage axé sur la maintenance et la rigueur opérationnelle."
        ),
        github_url=None,
        demo_url=None,
        image_url=None,
        content={
            'objective': (
                'Acquérir les bases théoriques et pratiques de la maintenance technique, '
                'du diagnostic de dysfonctionnements et du suivi des équipements.'
            ),
            'tools': 'Électronique, Maintenance technique, Diagnostic, Appareillages biomédicaux',
            'architecture': (
                '- Apprentissage des méthodes de maintenance préventive et corrective sur des équipements techniques.\n'
                '- Analyse de schémas techniques, détection de pannes et application des normes de sécurité.'
            ),
            'alert_flow': None,
            'lessons': (
                '- Analyse méthodique et diagnostic de pannes matérielles.\n'
                '- Rigueur, esprit logique et respect des règles de sécurité.'
            ),
            'impact': 'Diplôme du Brevet de Technicien obtenu en 2020, validant les fondations techniques du parcours.'
        }
    )
    session.add(item)
    session.commit()
    print('Inserted item id:', item.id)
finally:
    session.close()
