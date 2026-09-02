PORTFOLIO PROFESSIONNEL — SAMNICK BIGA RAOUL AUBIN
Ingénieur Réseaux, Systèmes et Cybersécurité — SOC Analyst Junior — IT Consultant
Yaoundé, Cameroun

Site en ligne : https://raoulbiga-phi.vercel.app
Code source : https://github.com/Biga14-samuel/Mon_portofolio
LinkedIn : https://www.linkedin.com/in/aubinbiga


PRÉSENTATION DU PROJET

Ce portfolio professionnel est une application web fullstack que j'ai conçue, développée et déployée intégralement.
Il ne s'agit pas d'un simple site statique : il dispose d'un vrai backend sécurisé, d'un espace d'administration
protégé, d'animations interactives soignées, et d'un système de contenu dynamique géré en base de données.
L'objectif est de présenter mon parcours, mes compétences, mes réalisations techniques et mes publications,
tout en offrant une expérience visuelle moderne et mémorable aux visiteurs.


STACK TECHNIQUE

Frontend
  Vue.js 3 avec Vite (composition API, script setup)
  CSS entièrement sur mesure, sans framework (glassmorphisme, Bento Grid, dark mode)
  Animations Canvas sur mesure avec l'API Web Audio pour les effets sonores
  Lenis pour le smooth scroll cinématique
  Vue-Sonner pour les notifications toast
  Lucide Vue pour les icônes

Backend
  FastAPI (Python) avec architecture modulaire
  SQLAlchemy comme ORM, base de données SQLite en local, Supabase Storage pour les médias en production
  Alembic pour les migrations de base de données
  JWT (JSON Web Tokens) pour l'authentification de l'espace admin
  Bcrypt pour le hachage sécurisé des mots de passe
  SlowAPI pour le rate limiting (protection contre les attaques par force brute)
  Bibliothèque nh3 (Rust) pour la sanitisation XSS des contenus textuels

Déploiement
  Frontend hébergé sur Vercel (build automatique depuis GitHub Actions)
  Backend hébergé sur Render (serveur Python persistant)
  Stockage des images et fichiers sur Supabase Storage (bucket public CDN)
  CI/CD via GitHub Actions (déclenchement automatique à chaque push sur main)


FONCTIONNALITÉS PRINCIPALES

Navigation et interface générale
  Barre de navigation fixe en haut avec menu hamburger responsive sur mobile
  Bouton de contrôle du son (activer ou désactiver les effets sonores)
  Liens d'ancrage fluides vers chaque section
  Scroll-to-top avec bouton visible dès que l'utilisateur descend dans la page
  Horloge en temps réel dans le footer (heure locale affichée dynamiquement)
  Logo animé dynamique dans la topbar
  Preloader animé au chargement initial
  Gestion d'une page 404 personnalisée avec redirection propre

Section Héros (accueil)
  Titre interactif lettre par lettre : chaque caractère réagit au survol de la souris avec une animation de vague
  Effet machine à écrire qui fait défiler les titres professionnels automatiquement
  Badge de disponibilité animé (point vert pulsant)
  Trois boutons d'action : Voir mes projets, Me contacter, Télécharger mon CV en PDF
  Bouton de partage (natif sur mobile, fallback copie du lien sur bureau)
  Photo de profil avec animation au chargement
  Mur de logos des organisations avec lesquelles j'ai travaillé (PANESS IT, IHTM, MINAT, etc.)

Section À propos
  Présentation en trois blocs numérotés : ce que je réalise, ma démarche, ce que j'apporte
  Filigrane géant animé en fond
  Texte optimisé pour les moteurs de recherche (SEO)

Projet à la une
  Carte mise en avant avec métriques clés du projet (nombre de VMs, phases, scénarios, coût)
  Bouton d'accès direct à la fiche détaillée du projet
  Sélection de la réalisation à mettre en avant depuis l'espace admin

Section Parcours
  Timeline de mon parcours académique et professionnel
  Chaque étape peut contenir une description riche, des images, un PDF, des tags de compétences

Section Stack et outils (Compétences)
  Présentation visuelle de mes compétences organisées par domaine (réseau, sécurité, systèmes, web, DevOps)
  Vue statistiques avec compteurs animés
  Chaque compétence peut avoir une fiche détaillée accessible en un clic

Section Réalisations
  Grille de cartes de projets avec images, descriptions, tags colorés par domaine
  Filtrage dynamique par tag ou domaine en temps réel
  Skeleton loaders pendant le chargement (effet de chargement progressif)
  Cartes cliquables ouvrant une fiche de cas détaillée (Case Study)

Fiches de cas (Case Studies)
  Vue immersive en pleine page par-dessus le contenu
  Galerie d'images avec lightbox (zoom, navigation par flèches, fermeture par touche Échap)
  Timeline des étapes de réalisation du projet
  Schéma d'architecture visuel
  Description riche avec sections organisées
  PDF téléchargeable pour chaque projet

Section Blog
  Articles, notes et retours d'expérience publiés dynamiquement
  Chaque article peut inclure un PDF en pièce jointe
  Géré intégralement depuis l'espace admin

Section Témoignages
  Formulaire de témoignage pour les visiteurs (avec animation de succès après envoi)
  Modération des témoignages depuis l'espace admin (afficher ou masquer)
  Affichage public des témoignages validés

Section Veille automatique
  Flux de vulnérabilités actualisé automatiquement (CVE depuis la CISA KEV)
  Barre de statut avec date de dernière mise à jour et nombre de vulnérabilités affichées
  Lien vers la source officielle pour chaque entrée

Section Contact
  Formulaire de contact intégré avec champ email, sujet et message
  Envoi par email via SMTP Gmail sécurisé (application password)
  Feedback visuel en temps réel (état envoi, succès, erreur)
  Suggestions de sujets de contact rapide sous forme de chips cliquables

Footer
  Liens vers GitHub, LinkedIn et email
  Horloge en temps réel
  Copyright


ESPACE ADMINISTRATEUR

L'espace admin est accessible depuis un bouton discret dans la navigation.
Il est protégé par un login JWT avec rate limiting (5 tentatives maximum par minute par IP).

Depuis l'espace admin, il est possible de :
  Ajouter, modifier ou supprimer des éléments (parcours, compétences, réalisations, articles de blog)
  Uploader des images ou des PDF directement vers Supabase Storage
  Gérer les tags et catégories affichés dans les filtres
  Modérer les témoignages (afficher ou masquer chaque témoignage)
  Sélectionner le projet à mettre en avant sur la page d'accueil
  Rédiger un contenu riche avec galerie d'images, schéma d'architecture, timeline et PDF

Le formulaire d'édition propose un éditeur riche avec :
  Champ de titre et description courte
  Uploader multi-images glisser-déposer
  Champ d'URL de schéma d'architecture
  Uploader de PDF
  Éditeur de timeline avec étapes numérotées
  Gestionnaire de tags avec suggestions intelligentes
  Option de mise en avant (projet à la une)


DESIGN ET ANIMATIONS

Palette de couleurs
  Orange Ubuntu (E95420) pour les actions principales
  Aubergine (77216F) pour les fonds et accents
  Aubergine foncée (2C001E) pour les zones sombres
  Dégradés subtils entre ces teintes

Effets visuels
  Arrière-plan animé avec des particules de type bâtonnets (Sticks) en Canvas WebGL-like
  Les particules réagissent au mouvement de la souris (effet de répulsion et retour naturel)
  Orbe cursor qui suit le pointeur de souris avec du lag physique
  Effets glassmorphisme sur les cartes et modales (flou d'arrière-plan, opacité)
  Animations d'apparition au scroll (reveal-on-scroll avec IntersectionObserver)
  Effet de vague sur les lettres du titre au survol
  Animations CSS sur les cartes au survol (élévation, lueur)
  Sections qui s'animent à l'entrée dans le viewport
  Orbite animée dans la section contact (rotation perpétuelle d'un cercle décoratif)

Effets sonores (optionnels, désactivés par défaut)
  Son de survol sur les éléments interactifs (tick discret à 600 Hz)
  Son de clic (pop triangle à 400 Hz)
  Son de succès (carillon Do-Mi)
  Son de basse erreur (sawtooth à 200 Hz)
  Tous générés par l'API Web Audio sans fichier externe

Typographie
  Police Ubuntu Sans chargée depuis Google Fonts (400, 500, 700)
  Hiérarchie typographique claire avec clamp() pour la fluidité entre tailles d'écran

Responsive
  Breakpoints à 900px et 560px
  Menu hamburger sur mobile
  Grilles CSS qui passent en colonne unique sur petits écrans
  Images et cartes qui s'adaptent à la largeur disponible

Accessibilité
  Support de la préférence système prefers-reduced-motion (animations désactivées si l'utilisateur préfère)
  Attributs aria-label sur tous les éléments interactifs
  Structure sémantique HTML5 correcte
  Contraste respectant les standards WCAG


SÉCURITÉ

Authentification JWT avec expiration configurable (60 minutes par défaut)
Hachage bcrypt du mot de passe (facteur de coût 12)
Rate limiting sur la route de login (5 essais max par minute par IP, puis blocage)
Comparaison à temps constant des identifiants (protection contre les timing attacks)
Sanitisation XSS de tous les contenus textuels via nh3 (binding Rust)
Headers de sécurité HTTP sur toutes les réponses du backend :
  X-Content-Type-Options: nosniff
  X-Frame-Options: DENY
  X-XSS-Protection
  Strict-Transport-Security (HSTS, 1 an)
Content Security Policy (CSP) déclaré dans le HTML
Protection anti-copie sur le frontend (user-select: none, blocage du drag sur les images)
CORS strict (seules les origines autorisées peuvent interroger l'API)


SEO ET RÉFÉRENCEMENT

Balises Open Graph complètes (WhatsApp, LinkedIn, Facebook, Discord, Telegram)
Twitter Card pour le partage sur X
Données structurées JSON-LD (Schema.org Person) pour Google Knowledge Graph
Balise canonique
Meta description optimisée
Vérification Google Search Console (deux tokens)
Sitemap et robots configurés


LANCER LE PROJET EN LOCAL

1. Lancer le backend

  cd backend
  Créer un fichier .env en copiant .env.example et en remplissant les variables
  .venv\Scripts\Activate.ps1
  pip install -r requirements.txt
  python seed.py --init-db
  uvicorn app.main:app --reload

  Le serveur tourne sur http://127.0.0.1:8000

2. Lancer le frontend

  cd frontend
  Copier .env.example en .env et définir VITE_API_URL=http://localhost:8000
  npm install
  npm run dev

  L'application est accessible sur http://localhost:5173


VARIABLES D'ENVIRONNEMENT BACKEND

DATABASE_URL        URL de connexion à la base de données (SQLite ou PostgreSQL)
JWT_SECRET          Clé secrète longue et aléatoire pour signer les tokens JWT
JWT_EXPIRE_MINUTES  Durée de validité d'un token en minutes (60 par défaut)
ADMIN_USERNAME      Nom d'utilisateur de l'espace admin
ADMIN_PASSWORD_HASH Hash bcrypt du mot de passe admin (généré avec bcrypt)
CORS_ORIGINS        Liste des origines autorisées séparées par des virgules
SMTP_SERVER         Serveur SMTP pour l'envoi d'emails (smtp.gmail.com)
SMTP_PORT           Port SMTP (465 pour SSL)
SMTP_USER           Adresse email Gmail d'envoi
SMTP_PASSWORD       Mot de passe d'application Gmail
SMTP_RECIPIENT      Adresse email destinataire des messages de contact
SUPABASE_URL        URL racine du projet Supabase (format https://xxx.supabase.co)
SUPABASE_KEY        Clé service_role Supabase
SUPABASE_BUCKET     Nom du bucket de stockage (portfolio-uploads par défaut)


STRUCTURE DES DOSSIERS

portfolio/
  backend/
    app/
      main.py         Routes de l'API (items, tags, témoignages, upload, contact, login)
      auth.py         JWT, bcrypt, rate limiting, vérification des tokens
      config.py       Chargement des variables d'environnement (pydantic-settings)
      models.py       Modèles SQLAlchemy (Item, Tag, Testimonial)
      schemas.py      Schémas de validation Pydantic
      database.py     Connexion et session SQLAlchemy
    alembic/          Migrations de base de données
    scripts/          Scripts utilitaires d'import de données
    tests/            Tests unitaires
  frontend/
    src/
      App.vue         Composant racine, logique globale et routing
      components/     Composants réutilisables (cartes, formulaires, lightbox, etc.)
      services/       Appels API, sons, tags
      store/          État global de l'authentification
      utils/          Utilitaires (sanitisation des emojis)
      assets/
        styles/       Fichiers CSS modulaires (base, layout, cards, animations, etc.)
    public/           Images publiques, favicon, CV PDF, logos
    index.html        Point d'entrée HTML avec toutes les balises SEO et méta


Merci de votre visite.
N'hésitez pas à me contacter via le formulaire sur le site ou par LinkedIn si vous avez des questions,
des opportunités ou simplement envie d'échanger sur un sujet lié aux réseaux et à la cybersécurité.
