Mon Portfolio Personnel (Raoul BIGA)
Salut ! Bienvenue sur le code source de mon portfolio professionnel.
Je suis Raoul BIGA, Administrateur réseau & sécurité et ce dépôt contient mon site vitrine. Je lai construit pour mettre en avant mon parcours, mes compétences et mes projets, et pour permettre à nimporte qui de télécharger facilement mon CV en PDF depuis la page daccueil !

Stack Technique
Jai voulu concevoir une application qui soit à la fois performante, esthétique et surtout sécurisée (cest mon domaine après tout !).
Frontend : Vue.js 3 avec Vite. Design sur mesure, moderne et fluide (inspiré du Bento Grid et du Glassmorphism).
Backend : FastAPI en Python avec une base de données SQLite, facilement adaptable pour le cloud.
Sécurité : Jy ai intégré un tas de choses : Rate Limiting contre les spams, sanitization XSS avec nh3 (Rust), JWT pour mon espace admin, et même des petites protections anti-copie sur le frontend.

Fonctionnalités phares
Téléchargement de mon CV PDF en un clic.
UX soignée avec des Skeleton screens pour les chargements et de jolies modales pour les témoignages.
Espace Admin caché pour me permettre dajouter/éditer mes projets et gérer les témoignages des visiteurs.
Contact direct via un formulaire intégré et sécurisé.

Comment lancer le projet chez vous ?
Si vous voulez tester le code en local, cest très simple :

1. Lancer le Backend (FastAPI)
Ouvrez un terminal et allez dans le dossier backend :

bash
cd backend
.venv\Scripts\Activate.ps1
uvicorn app.main:app --reload
Le serveur tourne alors sur <http://127.0.0.1:8000>. Sil vous manque la base de données, un petit python seed.py --init-db suffira pour la créer !

1. Lancer le Frontend (Vue.js)
Ouvrez un deuxième terminal dans le dossier frontend :

bash
cd frontend
npm run dev
Le site est maintenant accessible sur <http://localhost:5173>.

Déploiement
Frontend hébergé sur Vercel (Pensez juste à bien renseigner la variable VITE_API_URL pour pointer vers votre backend).
Backend hébergé sur Render, avec toute ma configuration SMTP pour recevoir les emails depuis le formulaire.

Merci de votre visite et bonne lecture de mon code ! Nhésitez pas à me contacter via le site si vous avez des questions ou des opportunités.
