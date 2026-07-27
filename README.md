# Portfolio Premium - Vue.js / FastAPI / SQLite

Application web complète de portfolio professionnel dotée d'un design "Éditorial" ultra-moderne (Bento Grid, Glassmorphism, Lettrine) et d'une sécurité maximale (>95%).

Le frontend (Vue 3 / Vite) est buildable en fichiers statiques, tandis que le backend (FastAPI) gère l'API sécurisée avec une base de données locale SQLite (facilement migratable vers PostgreSQL).

## 🌟 Nouveautés & Fonctionnalités (Refonte Ultime)
- **Design Éditorial Premium** : Lettrine géante "Magazine", badges d'index minimalistes, Mur de logos interactif.
- **Bento Grid & Glassmorphism** : Cartes de compétences asymétriques avec effet "verre", ombres portées et image de profil détourée flottante.
- **Logo Dynamique** : Logo géométrique animé de style Bauhaus.
- **Sécurité Maximale (Defense in Depth)** : 
  - Protection Anti-Copie : Désactivation du clic droit, de la sélection, du drag-and-drop et des raccourcis dev (F12).
  - Sanitization XSS avec `nh3` (Rust) pour nettoyer les entrées HTML.
  - Limiteur de trafic (Rate Limiting) avec `slowapi` pour bloquer les spams.
  - En-têtes HTTP de sécurité (CSP, HSTS, X-Frame-Options).
  - Validation forte des emails via `pydantic[email]`.

---

## 🚀 Comment lancer le projet localement ?

### 1. Lancer le Backend (FastAPI)
Ouvrez un terminal et naviguez dans le dossier `backend` :
```bash
cd backend

# Activer l'environnement virtuel (si pas déjà fait)
.venv\Scripts\Activate.ps1

# Lancer le serveur d'API
uvicorn app.main:app --reload
```
Le backend tourne désormais sur **http://127.0.0.1:8000**.
*(Si la base de données SQLite n'existe pas encore, exécutez d'abord `alembic upgrade head` puis `python seed.py --init-db` pour la créer).*

### 2. Lancer le Frontend (Vue.js)
Ouvrez un second terminal et naviguez dans le dossier `frontend` :
```bash
cd frontend

# Lancer le serveur de développement
npm run dev
```
Le site est désormais accessible sur **http://localhost:5173** (ou l'URL indiquée dans le terminal).

---

## 🏗️ Structure
- `frontend/`: Vue.js 3, Vite, composants Bento, animations Lenis/Parallax, styles CSS natifs.
- `backend/`: FastAPI, SQLAlchemy, Alembic, JWT, nh3, slowapi, SQLite.
- `.github/workflows/deploy.yml`: build et déploiement du frontend sur GitHub Pages.

## 🔐 API
- `POST /api/login`: Authentification admin, retourne un JWT.
- `GET /api/items`: Liste publique (filtrable).
- `POST /api/contact`: Formulaire de contact (protégé par Rate Limit 3/min).
- `POST /api/testimonials`: Formulaire de témoignages (protégé par Rate Limit 5/min, Sanitization XSS).
