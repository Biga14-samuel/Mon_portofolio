<template>
  <div class="app-shell">
    <header class="topbar">
      <a class="brand" href="#accueil" aria-label="Portfolio - accueil">
        <span class="brand-mark" aria-hidden="true"></span>
        <span>SAMNICK BIGA</span>
      </a>
      <nav aria-label="Navigation principale">
        <a href="#apropos">À propos</a>
        <a href="#parcours">Parcours</a>
        <a href="#competences">Competences</a>
        <a href="#realisations">Realisations</a>
        <button v-if="!authState.token" class="nav-button" type="button" @click="showLogin = true">Admin</button>
        <button v-else class="nav-button" type="button" @click="logout">Deconnexion</button>
      </nav>
    </header>

    <main id="accueil">
      <section class="hero">
        <div class="hero-copy">
          <PillBadge tone="orange">Disponible pour stage, emploi ou mission IT</PillBadge>
          <h1>SAMNICK BIGA RAOUL AUBIN</h1>
          <h2>Administrateur réseau et sécurité des systèmes | IT Consultant | SOC Analyst Junior</h2>
          <p>
            Je conçois, sécurise et documente des environnements réseau avec une attention particulière pour la
            supervision, la détection et la réponse aux incidents.
          </p>
          <div class="availability-card" aria-label="Statut professionnel">
            <span class="availability-dot" aria-hidden="true"></span>
            <strong>Disponible</strong>
            <span>Stage, emploi junior, mission IT, administration réseau ou support cybersécurité.</span>
          </div>
          <ul class="hero-facts" aria-label="Informations principales">
            <li>Yaoundé, Cameroun</li>
            <li>Wazuh, Suricata, MISP, DFIR-IRIS, Shuffle</li>
            <li>Threat intelligence et incident response</li>
          </ul>
          <div class="hero-actions">
            <a class="button primary" href="#realisations">Voir mes projets</a>
            <a class="button secondary" href="mailto:samuelbiga10@gmail.com">Me contacter</a>
            <button class="button tertiary" type="button" disabled title="Le CV sera ajouté plus tard">Télécharger CV</button>
          </div>
          <div class="contact-links" aria-label="Liens de contact">
            <a href="mailto:samuelbiga10@gmail.com">samuelbiga10@gmail.com</a>
            <a href="tel:+237654881101">+237 654 881 101</a>
            <a href="https://github.com/Biga14-samuel" target="_blank" rel="noreferrer">GitHub</a>
            <a href="https://www.linkedin.com/in/aubinbiga" target="_blank" rel="noreferrer">LinkedIn</a>
          </div>
          <a class="scroll-cue" href="#realisations" aria-label="Descendre vers les projets">
            <span></span>
            Défiler
          </a>
        </div>
        <figure class="hero-visual profile-photo-card">
          <img :src="profilePhoto" alt="Portrait de SAMNICK BIGA RAOUL AUBIN" />
        </figure>
      </section>

      <section class="about-section" id="apropos" aria-labelledby="about-title">
        <div class="about-kicker">
          <PillBadge tone="aubergine">À propos</PillBadge>
        </div>
        <div class="about-lead">
          <h2 id="about-title">
            Construire des infrastructures fiables, lisibles et prêtes à détecter les incidents avant qu'ils ne
            deviennent critiques.
          </h2>
          <p>
            Jeune diplômé en Licence Professionnelle Réseaux et Sécurité Informatique à l'IHTM, je me spécialise dans
            la conception d'architectures SOC open-source. Mon expérience récente chez PANESS IT m'a permis de déployer
            un environnement complet basé sur Wazuh, MISP, Suricata, DFIR-IRIS et Shuffle.
          </p>
        </div>
        <div class="about-grid">
          <article class="about-card">
            <span>01</span>
            <h3>Ce que je fais</h3>
            <p>
              Administration réseau et système, intégration SIEM/EDR, supervision sécurité, durcissement de services,
              scripting Python/Bash et documentation technique exploitable.
            </p>
          </article>
          <article class="about-card">
            <span>02</span>
            <h3>Comment je travaille</h3>
            <p>
              Je pars du besoin terrain, je schématise l'architecture, je teste par scénarios, puis je documente les
              choix techniques pour rendre les solutions maintenables et transmissibles.
            </p>
          </article>
          <article class="about-card">
            <span>03</span>
            <h3>Ce que je recherche</h3>
            <p>
              Un stage, un premier emploi ou une mission IT où je peux contribuer sur l'administration réseau, la
              sécurité des systèmes, le SOC, le support infrastructure ou la réponse aux incidents.
            </p>
          </article>
        </div>
      </section>

      <section class="featured-section" id="projets-a-la-une" aria-labelledby="featured-title">
        <div class="section-heading">
          <h2 id="featured-title">Projets à la une</h2>
        </div>
        <div class="featured-grid">
          <article v-if="featuredProject" class="featured-project-card">
            <div class="featured-project-card__content">
              <PillBadge :tone="tagTone(featuredProject.category)">{{ featuredProject.category }}</PillBadge>
              <h3>{{ featuredProject.title }}</h3>
              <p>{{ featuredProject.description }}</p>
              <button class="button primary" type="button" @click="openCaseStudy(featuredProject)">
                Voir l'étude de cas
              </button>
            </div>
          </article>
          <article v-else class="featured-project-card empty-featured">
            <div class="featured-project-card__content">
              <PillBadge tone="neutral">À sélectionner</PillBadge>
              <h3>Aucun projet à la une pour le moment</h3>
              <p>
                Connecte-toi en administrateur, ajoute une réalisation puis coche “Mettre cette réalisation à la une”.
              </p>
            </div>
          </article>

          <div class="future-projects" aria-label="Domaines de projets futurs">
            <article v-for="category in futureProjectCategories" :key="category" class="future-project-card" :class="tagTone(category)">
              <span>{{ category }}</span>
              <small>À venir</small>
            </article>
          </div>
        </div>
      </section>

      <section v-if="authState.token" class="admin-strip" aria-label="Administration du portfolio">
        <div>
          <PillBadge tone="aubergine">Mode administration</PillBadge>
          <strong>Tu peux ajouter, modifier ou supprimer les éléments affichés aux visiteurs.</strong>
        </div>
        <button class="button primary" type="button" @click="openCreate">
          <Plus :size="18" aria-hidden="true" />
          Ajouter un element
        </button>
      </section>

      <section class="filter-band" aria-label="Filtrer le portfolio">
        <button
          v-for="filter in filters"
          :key="filter.value"
          class="filter-pill"
          :class="{ active: selectedType === filter.value }"
          type="button"
          :aria-pressed="selectedType === filter.value"
          @click="selectedType = filter.value"
        >
          {{ filter.label }}
        </button>
      </section>

      <section v-if="categoryFilters.length" class="filter-band compact" aria-label="Filtrer par tag">
        <button
          class="filter-pill small"
          :class="{ active: selectedCategory === '' }"
          type="button"
          :aria-pressed="selectedCategory === ''"
          @click="selectedCategory = ''"
        >
          Tous les tags
        </button>
        <button
          v-for="category in categoryFilters"
          :key="category"
          class="filter-pill small"
          :class="[{ active: selectedCategory === category }, tagTone(category)]"
          type="button"
          :aria-pressed="selectedCategory === category"
          @click="selectedCategory = category"
        >
          {{ category }}
        </button>
      </section>

      <Transition name="filter-swap" mode="out-in">
        <div :key="`${selectedType}-${selectedCategory}`" class="portfolio-results">
          <p v-if="loading" class="empty-state" role="status">Chargement du portfolio...</p>
          <p v-else-if="loadError" class="form-error" role="alert">{{ loadError }}</p>

          <template v-else>
            <ContentSection
              id="parcours"
              title="Mon parcours"
              :items="grouped.parcours"
              empty="Aucun parcours publie pour le moment."
              :editable="Boolean(authState.token)"
              @edit="openEdit"
              @delete="remove"
            />
            <ContentSection
              id="competences"
              title="Mes competences"
              :items="grouped.competence"
              empty="Aucune competence publiee pour le moment."
              :editable="Boolean(authState.token)"
              @edit="openEdit"
              @delete="remove"
            />
            <ContentSection
              id="realisations"
              title="Mes realisations"
              :items="grouped.realisation"
              empty="Aucune realisation publiee pour le moment."
              :editable="Boolean(authState.token)"
              @edit="openEdit"
              @delete="remove"
              @view-case="openCaseStudy"
            />
          </template>
        </div>
      </Transition>
    </main>

    <div v-if="caseStudyItem" class="modal-backdrop" role="presentation" @click.self="closeCaseStudy">
      <section class="case-modal" role="dialog" aria-modal="true" aria-labelledby="case-title">
        <button class="case-close" type="button" aria-label="Fermer l'étude de cas" @click="closeCaseStudy">×</button>
        <div class="case-hero">
          <PillBadge :tone="tagTone(caseStudyItem.category)">{{ caseStudyItem.category }}</PillBadge>
          <h2 id="case-title">{{ caseStudyItem.title }}</h2>
          <p>{{ caseStudyItem.description }}</p>
        </div>

        <div class="case-layout">
          <aside class="case-summary" aria-label="Résumé du projet">
            <strong>{{ caseStudyItem.subtitle ? 'Informations / stack' : 'Informations' }}</strong>
            <ul>
              <li v-for="entry in caseStudyStack" :key="entry">{{ entry }}</li>
            </ul>
          </aside>

          <div class="case-timeline">
            <article v-for="section in activeCaseStudy" :key="section.title" class="case-step">
              <span>{{ section.number }}</span>
              <div>
                <h3>{{ section.title }}</h3>
                <p>{{ section.body }}</p>
              </div>
            </article>
          </div>
        </div>

        <div class="case-placeholder">
          <strong>Captures et démonstration</strong>
          <p>Emplacement prévu pour ajouter plus tard des captures, liens GitHub, lien de démo ou vidéo du projet.</p>
        </div>
      </section>
    </div>

    <div v-if="showLogin" class="modal-backdrop" role="presentation" @click.self="showLogin = false">
      <section class="modal login-card" role="dialog" aria-modal="true" aria-labelledby="login-title">
        <LockKeyhole aria-hidden="true" :size="34" />
        <h2 id="login-title">Administration du portfolio</h2>
        <p>Connexion reservee au proprietaire du portfolio.</p>
        <form @submit.prevent="handleLogin">
          <label>
            Identifiant
            <input v-model.trim="credentials.username" required autocomplete="username" />
          </label>
          <label>
            Mot de passe
            <input v-model="credentials.password" required type="password" autocomplete="current-password" />
          </label>
          <p v-if="authError" class="form-error" role="alert">{{ authError }}</p>
          <div class="form-actions">
            <button class="button secondary" type="button" @click="showLogin = false">Annuler</button>
            <button class="button primary" type="submit">Se connecter</button>
          </div>
        </form>
      </section>
    </div>

    <div v-if="editing" class="modal-backdrop" role="presentation" @click.self="closeForm">
      <section class="modal" role="dialog" aria-modal="true" aria-labelledby="form-title">
        <h2 id="form-title">{{ editing.id ? 'Modifier un element' : 'Ajouter un element' }}</h2>
        <ItemForm :item="editing" @submit="saveItem" @cancel="closeForm" />
      </section>
    </div>

    <footer>
      <strong>SAMNICK BIGA RAOUL AUBIN</strong>
      <span>Yaoundé, Cameroun - samuelbiga10@gmail.com</span>
    </footer>
  </div>
</template>

<script setup>
import { computed, onMounted, reactive, ref, watch } from 'vue';
import { LockKeyhole, Plus } from 'lucide-vue-next';
import ContentSection from './components/ContentSection.vue';
import ItemForm from './components/ItemForm.vue';
import PillBadge from './components/PillBadge.vue';
import { authState, clearToken, setToken } from './store/auth';
import { createItem, deleteItem, getItems, login, updateItem } from './services/api';
import { tagTone } from './services/tags';

const profilePhoto = `${import.meta.env.BASE_URL}profile-photo.jpg`;

const filters = [
  { label: 'Tous', value: '' },
  { label: 'Parcours', value: 'parcours' },
  { label: 'Competences', value: 'competence' },
  { label: 'Realisations', value: 'realisation' },
];

const futureProjectCategories = ['Fibre optique', 'Maintenance', 'Réseau', 'Web', 'Base de données'];

const selectedType = ref('');
const selectedCategory = ref('');
const showLogin = ref(false);
const items = ref([]);
const loading = ref(false);
const loadError = ref('');
const authError = ref('');
const editing = ref(null);
const caseStudyItem = ref(null);
const credentials = reactive({ username: '', password: '' });

const typeFilteredItems = computed(() => (selectedType.value ? items.value.filter((item) => item.type === selectedType.value) : items.value));

const caseStudyStack = computed(() => {
  if (!caseStudyItem.value?.subtitle) return ['À compléter'];
  return caseStudyItem.value.subtitle
    .split(',')
    .map((entry) => entry.trim())
    .filter(Boolean);
});

const activeCaseStudy = computed(() => {
  if (!caseStudyItem.value) return [];
  return [
    {
      number: '01',
      title: 'Contexte',
      body: caseStudyItem.value.description,
    },
    {
      number: '02',
      title: 'Objectif',
      body: "À préciser dans l'administration lorsque tu complèteras cette réalisation.",
    },
    {
      number: '03',
      title: 'Architecture / méthode',
      body: "À compléter avec l'organisation technique, les étapes de conception ou la méthode de réalisation.",
    },
    {
      number: '04',
      title: 'Tests / validation',
      body: "À compléter avec les scénarios testés, les vérifications effectuées ou les contraintes rencontrées.",
    },
    {
      number: '05',
      title: 'Résultats',
      body: "À compléter avec les résultats obtenus, les livrables produits ou l'impact du projet.",
    },
  ];
});

const categoryFilters = computed(() => {
  const values = typeFilteredItems.value.map((item) => item.category).filter(Boolean);
  return [...new Set(values)].sort((a, b) => a.localeCompare(b));
});

const visibleItems = computed(() =>
  selectedCategory.value ? typeFilteredItems.value.filter((item) => item.category === selectedCategory.value) : typeFilteredItems.value,
);

const grouped = computed(() => ({
  parcours: visibleItems.value.filter((item) => item.type === 'parcours'),
  competence: visibleItems.value.filter((item) => item.type === 'competence'),
  realisation: visibleItems.value.filter((item) => item.type === 'realisation'),
}));

const featuredProject = computed(() => items.value.find((item) => item.type === 'realisation' && item.featured));

onMounted(loadItems);

watch(selectedType, () => {
  selectedCategory.value = '';
});

async function loadItems() {
  loading.value = true;
  loadError.value = '';
  try {
    items.value = await getItems();
  } catch (error) {
    loadError.value = "Impossible de charger les elements du portfolio. Verifie que l'API est lancee.";
    if (error.status === 401 || error.status === 403) clearToken();
  } finally {
    loading.value = false;
  }
}

async function handleLogin() {
  authError.value = '';
  try {
    const data = await login(credentials.username, credentials.password);
    setToken(data.access_token);
    credentials.password = '';
    showLogin.value = false;
    await loadItems();
  } catch (error) {
    authError.value = error.message;
  }
}

function logout() {
  clearToken();
  closeForm();
}

function openCreate() {
  editing.value = { type: 'parcours', category: 'Cursus', featured: false, title: '', subtitle: '', description: '' };
}

function openEdit(item) {
  editing.value = { ...item };
}

function openCaseStudy(item) {
  caseStudyItem.value = item;
}

function closeCaseStudy() {
  caseStudyItem.value = null;
}

function closeForm() {
  editing.value = null;
}

async function saveItem(payload) {
  try {
    if (editing.value.id) {
      await updateItem(editing.value.id, payload, authState.token);
    } else {
      await createItem(payload, authState.token);
    }
    closeForm();
    await loadItems();
  } catch (error) {
    if (error.status === 401 || error.status === 403) {
      clearToken();
      authError.value = 'Session expiree. Veuillez vous reconnecter.';
      showLogin.value = true;
    } else {
      alert(error.message);
    }
  }
}

async function remove(item) {
  if (!confirm(`Supprimer "${item.title}" du portfolio ?`)) return;
  try {
    await deleteItem(item.id, authState.token);
    await loadItems();
  } catch (error) {
    if (error.status === 401 || error.status === 403) {
      clearToken();
      authError.value = 'Session expiree. Veuillez vous reconnecter.';
      showLogin.value = true;
    } else {
      alert(error.message);
    }
  }
}
</script>
