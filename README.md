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

CONFIGURATION DE DEPLOIEMENT
- Frontend Vercel : définissez la variable d'environnement VITE_API_URL sur l'URL de votre backend FastAPI déployé (par exemple https://votre-backend.onrender.com).
- Backend Render/production : définissez DATABASE_URL, JWT_SECRET, ADMIN_USERNAME, ADMIN_PASSWORD_HASH, SMTP_SERVER, SMTP_PORT, SMTP_USER et SMTP_PASSWORD.
- Vous pouvez générer le hash bcrypt de votre mot de passe avec :
  python seed.py --password "votre_mot_de_passe"
- Ce projet n'utilise pas Supabase pour l'authentification ou l'envoi d'emails. Le login administrateur est géré uniquement par le backend FastAPI.
- Si vous utilisez Gmail pour l'envoi d'emails, configurez un mot de passe d'application et utilisez SMTP_PORT=465 ou 587 selon votre configuration.
- Si Vercel héberge uniquement le frontend, les requêtes /api depuis le navigateur doivent pointer vers le backend via VITE_API_URL. Sans cette variable, le frontend essayera par défaut d'atteindre http://localhost:8000 en développement et window.location.origin en production.
- Après déploiement, soumettez votre site à Google Search Console pour accélérer l'indexation.
