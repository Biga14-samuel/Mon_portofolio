PORTFOLIO PREMIUM - VUE.JS / FASTAPI / SQLITE

Application web complete de portfolio professionnel dotee d'un design Editorial ultra-moderne (Bento Grid, Glassmorphism, Lettrine) et d'une securite maximale.

Le frontend (Vue 3 / Vite) est buildable en fichiers statiques, tandis que le backend (FastAPI) gere l'API securisee avec une base de donnees locale SQLite (facilement migratable vers PostgreSQL).


NOUVEAUTES ET FONCTIONNALITES (REFONTE ULTIME)
Design Editorial Premium : Lettrine geante Magazine, badges d'index minimalistes, Mur de logos interactif.
Bento Grid et Glassmorphism : Cartes de competences asymetriques avec effet verre, ombres portees et image de profil detouree flottante.
Logo Dynamique : Logo geometrique anime de style Bauhaus.
Securite Maximale : 
Protection Anti-Copie : Desactivation du clic droit, de la selection, du drag-and-drop et des raccourcis dev (F12).
Sanitization XSS avec nh3 (Rust) pour nettoyer les entrees HTML.
Limiteur de trafic (Rate Limiting) avec slowapi pour bloquer les spams.
En-tetes HTTP de securite (CSP, HSTS, X-Frame-Options).
Validation forte des emails via pydantic.


COMMENT LANCER LE PROJET LOCALEMENT ?

1. Lancer le Backend (FastAPI)
Ouvrez un terminal et naviguez dans le dossier backend :
cd backend

Activer l'environnement virtuel (si pas deja fait)
.venv\Scripts\Activate.ps1

Lancer le serveur d'API
uvicorn app.main:app --reload

Le backend tourne desormais sur http://127.0.0.1:8000.
(Si la base de donnees SQLite n'existe pas encore, executez d'abord alembic upgrade head puis python seed.py --init-db pour la creer).

2. Lancer le Frontend (Vue.js)
Ouvrez un second terminal et naviguez dans le dossier frontend :
cd frontend

Lancer le serveur de developpement
npm run dev

Le site est desormais accessible sur http://localhost:5173 (ou l'URL indiquee dans le terminal).


STRUCTURE
frontend/ : Vue.js 3, Vite, composants Bento, animations Lenis/Parallax, styles CSS natifs.
backend/ : FastAPI, SQLAlchemy, Alembic, JWT, nh3, slowapi, SQLite.
.github/workflows/deploy.yml : build et deploiement du frontend sur GitHub Pages.

API
POST /api/login : Authentification admin, retourne un JWT.
GET /api/items : Liste publique (filtrable).
POST /api/contact : Formulaire de contact (protege par Rate Limit 3/min).
POST /api/testimonials : Formulaire de temoignages (protege par Rate Limit 5/min, Sanitization XSS).
