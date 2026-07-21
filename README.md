# Portfolio Vue/FastAPI/PostgreSQL

Application web complete de portfolio professionnel inspiree du design system Ubuntu Yaru. Le frontend Vue 3 est buildable en fichiers statiques pour GitHub Pages, tandis que FastAPI et PostgreSQL sont prevus pour un hebergement separe.

## Structure

- `frontend/`: Vue.js 3, Vite, composants, dashboard admin, styles Yaru.
- `backend/`: FastAPI, SQLAlchemy, Alembic, JWT, bcrypt, PostgreSQL.
- `.github/workflows/deploy.yml`: build et deploiement du frontend sur GitHub Pages.

## Frontend

```bash
cd frontend
npm install
npm run dev
```

Variables utiles:

```bash
VITE_API_URL=https://votre-api-fastapi.render.com
VITE_BASE_PATH=/nom-du-depot/
```

Pour GitHub Pages, configurez le secret `VITE_API_URL` et, si le site est publie sous `https://user.github.io/repo/`, la variable repository `VITE_BASE_PATH=/repo/`.

## Backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

Generez le hash bcrypt du mot de passe admin:

```bash
python seed.py --password "mot-de-passe-admin-solide"
```

Copiez le hash dans `ADMIN_PASSWORD_HASH`, puis lancez les migrations:

```bash
alembic upgrade head
python seed.py --init-db
uvicorn app.main:app --reload
```

## API

- `POST /api/login`: authentification admin, retourne un JWT.
- `GET /api/items?type=`: liste publique, filtrable par `parcours`, `competence` ou `realisation`.
- `POST /api/items`: creation protegee par JWT.
- `PUT /api/items/{id}`: edition protegee par JWT.
- `DELETE /api/items/{id}`: suppression protegee par JWT.

## Deploiement

Frontend GitHub Pages:

1. Poussez le projet sur GitHub.
2. Dans Settings > Pages, choisissez GitHub Actions.
3. Ajoutez le secret `VITE_API_URL` avec l'URL publique du backend.
4. Ajoutez `VITE_BASE_PATH` si le depot n'est pas publie a la racine.
5. Chaque push sur `main` declenche `.github/workflows/deploy.yml`.

Backend Render/Railway/Fly.io:

1. Creez un service Python depuis le dossier `backend`.
2. Build command: `pip install -r requirements.txt`.
3. Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`.
4. Ajoutez les variables `DATABASE_URL`, `JWT_SECRET`, `JWT_EXPIRE_MINUTES`, `ADMIN_USERNAME`, `ADMIN_PASSWORD_HASH`, `CORS_ORIGINS`.
5. Executez `alembic upgrade head` au deploiement ou via une console du service.

PostgreSQL Supabase/Neon:

1. Creez une base PostgreSQL.
2. Copiez l'URL de connexion dans `DATABASE_URL` au format `postgresql+psycopg://...`.
3. Ajoutez l'origine GitHub Pages dans `CORS_ORIGINS`, par exemple `https://votre-user.github.io`.
