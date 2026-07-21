<template>
  <div class="app-shell">
    <header class="topbar">
      <a class="brand" href="#accueil" aria-label="Portfolio - accueil">
        <span class="brand-mark" aria-hidden="true"></span>
        <span>Portfolio</span>
      </a>
      <nav aria-label="Navigation principale">
        <a href="#apropos">À propos</a>
        <a href="#parcours">Parcours</a>
        <a href="#competences">Stack & outils</a>
        <a href="#realisations">Realisations</a>
        <a href="#contact">Contact</a>
        <button v-if="!authState.token" class="nav-button" type="button" @click="showLogin = true">Admin</button>
        <button v-else class="nav-button" type="button" @click="logout">Deconnexion</button>
      </nav>
    </header>

    <main id="accueil">
      <section class="hero">
        <div class="hero-copy">
          <div class="availability-card" aria-label="Statut professionnel">
            <span class="availability-dot" aria-hidden="true"></span>
            <strong>Disponible</strong>
            <span>Stage, emploi junior, mission IT ou cybersécurité.</span>
          </div>
          <h1 class="wave-name" aria-label="SAMNICK BIGA RAOUL AUBIN">
            <span
              v-for="(word, wIdx) in nameWords"
              :key="wIdx"
              class="wave-word"
            >
              <span
                v-for="(char, cIdx) in word.split('')"
                :key="cIdx"
                class="wave-char"
                :style="{ animationDelay: `${getGlobalCharIndex(wIdx, cIdx) * 0.07}s` }"
              >
                {{ char }}
              </span>
              <span v-if="wIdx < nameWords.length - 1" class="wave-space">&nbsp;</span>
            </span>
          </h1>
          <h2>Administrateur réseau & sécurité | IT Consultant | SOC Analyst Junior</h2>
          <p>
            Je conçois, sécurise et documente des environnements réseau avec une attention particulière pour la
            supervision, la détection et la réponse aux incidents.
          </p>
          <ul class="hero-facts" aria-label="Informations principales">
            <li>Yaoundé, Cameroun</li>
            <li>Réseaux (Cisco, Fortinet), Systèmes (Linux/Windows), Sécurité (SIEM, EDR)</li>
            <li>Détection, réponse aux incidents et hardening</li>
          </ul>
          <div class="hero-actions">
            <a class="button primary" href="#realisations">Voir mes projets</a>
            <a class="button secondary" href="#contact">Me contacter</a>
            <button class="button tertiary" type="button" disabled title="Le CV sera ajouté plus tard">Télécharger CV</button>
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

      <section class="about-section reveal-on-scroll" id="apropos" aria-labelledby="about-title">
        <div class="about-kicker">
          <PillBadge tone="aubergine">À propos</PillBadge>
        </div>
        <div class="about-lead">
          <h2 id="about-title">
            Construire des infrastructures fiables, lisibles et prêtes à détecter les incidents avant qu'ils ne
            deviennent critiques.
          </h2>
          <p>
            Jeune diplômé en Licence Professionnelle Réseaux et Sécurité Informatique à l'IHTM, je suis passionné par la conception d'architectures sécurisées et l'administration des systèmes. Ma récente expérience chez PANESS IT m'a permis de consolider mes acquis en déployant de A à Z un environnement complet de supervision et de réponse aux incidents.
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
              Un environnement stimulant où je pourrai approfondir mon expertise terrain et participer activement au maintien en conditions de sécurité de l'infrastructure.
            </p>
          </article>
        </div>
      </section>

      <section class="featured-section reveal-on-scroll" id="projets-a-la-une" aria-labelledby="featured-title">
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

      <section v-if="authState.token" class="admin-strip reveal-on-scroll" aria-label="Administration du portfolio">
        <div>
          <PillBadge tone="aubergine">Mode administration</PillBadge>
          <strong>Tu peux ajouter, modifier ou supprimer les éléments affichés aux visiteurs.</strong>
        </div>
        <div style="display: flex; gap: 1rem; align-items: center;">
          <button class="button secondary" type="button" @click="showTagManager = true">
            Gérer les tags
          </button>
          <button class="button primary" type="button" @click="openCreate">
            <Plus :size="18" aria-hidden="true" />
            Ajouter un element
          </button>
        </div>
      </section>

      <section class="filter-band reveal-on-scroll" aria-label="Filtrer le portfolio">
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

      <section v-if="categoryFilters.length" class="filter-band compact reveal-on-scroll" aria-label="Filtrer par tag">
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
            <StackToolsSection
              id="competences"
              :items="grouped.competence"
              empty="Aucune compétence publiée pour le moment."
              :editable="Boolean(authState.token)"
              @edit="openEdit"
              @delete="remove"
              @view-case="openCaseStudy"
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

      <section class="contact-section reveal-on-scroll" id="contact" aria-labelledby="contact-title">
        <div class="contact-copy">
          <PillBadge tone="orange">Contact</PillBadge>
          <h2 id="contact-title">Discutons d'une opportunité IT, réseau ou cybersécurité.</h2>
          <p>
            Disponible à Yaoundé et ouvert aux stages, emplois juniors, missions IT et collaborations techniques.
          </p>
          <div class="contact-actions">
            <button class="button primary" type="button" @click="copyEmail">
              {{ emailCopied ? 'Email copié' : 'Copier email' }}
            </button>
            <a class="button secondary" :href="whatsappUrl" target="_blank" rel="noreferrer">Écrire sur WhatsApp</a>
          </div>
        </div>

        <div class="contact-panel" aria-label="Coordonnées">
          <a href="mailto:samuelbiga10@gmail.com">
            <span>Email</span>
            <strong>samuelbiga10@gmail.com</strong>
          </a>
          <a href="https://wa.me/237654881101" target="_blank" rel="noreferrer">
            <span>WhatsApp</span>
            <strong>+237 654 881 101</strong>
          </a>
          <a href="https://www.linkedin.com/in/aubinbiga" target="_blank" rel="noreferrer">
            <span>LinkedIn</span>
            <strong>linkedin.com/in/aubinbiga</strong>
          </a>
          <a href="https://github.com/Biga14-samuel" target="_blank" rel="noreferrer">
            <span>GitHub</span>
            <strong>github.com/Biga14-samuel</strong>
          </a>
          <div>
            <span>Localisation</span>
            <strong>Yaoundé, Cameroun</strong>
          </div>
        </div>
      </section>
    </main>

    <div v-if="caseStudyItem" class="modal-backdrop" role="presentation" @click.self="closeCaseStudy" @dblclick="closeCaseStudy">
      <section
        ref="caseModal"
        class="case-modal"
        role="dialog"
        aria-modal="true"
        aria-labelledby="case-title"
        @scroll="updateCaseProgress"
        @dblclick="closeCaseStudy"
      >
        <div class="case-progress" aria-hidden="true">
          <span :style="{ width: `${caseProgress}%` }"></span>
        </div>
        <div class="case-nav-header">
          <button class="case-back-button" type="button" aria-label="Retourner en arrière" @click="closeCaseStudy">
            <ArrowLeft :size="20" aria-hidden="true" />
            <span>Retour</span>
          </button>
          <button class="case-close" type="button" aria-label="Fermer la vue" @click="closeCaseStudy">×</button>
        </div>
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
                <p style="white-space: pre-wrap;">{{ section.body }}</p>
                <div v-if="section.image" class="case-section-image-wrapper">
                  <img :src="section.image" alt="Schéma d'architecture" />
                </div>
              </div>
            </article>
          </div>
        </div>

        <div class="case-placeholder">
          <strong>Captures et démonstration</strong>
          <p v-if="!caseStudyItem.image_url && !caseStudyItem.github_url && !caseStudyItem.demo_url">Emplacement prévu pour ajouter plus tard des captures, liens GitHub, lien de démo ou vidéo du projet.</p>
          <div v-if="caseStudyItem.image_url" style="margin-top: 1.5rem; width: 100%; border-radius: var(--radius-md); overflow: hidden;">
             <img :src="caseStudyItem.image_url" alt="Capture d'écran du projet" style="width: 100%; height: auto; display: block;" />
          </div>
          <div v-if="caseStudyItem.github_url || caseStudyItem.demo_url" style="display: flex; gap: 1rem; margin-top: 1.5rem; flex-wrap: wrap;">
             <a v-if="caseStudyItem.github_url" :href="caseStudyItem.github_url" target="_blank" rel="noreferrer" class="button secondary">Code source (GitHub)</a>
             <a v-if="caseStudyItem.demo_url" :href="caseStudyItem.demo_url" target="_blank" rel="noreferrer" class="button primary">Démonstration en ligne</a>
          </div>
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

    <div v-if="showTagManager" class="modal-backdrop" role="presentation" @click.self="showTagManager = false">
      <section class="modal" role="dialog" aria-modal="true" aria-labelledby="tag-manager-title">
        <h2 id="tag-manager-title">Gestion des tags</h2>
        <TagManager @session-expired="handleSessionExpired" />
        <div class="form-actions" style="margin-top: 1.5rem;">
          <button class="button secondary" type="button" @click="showTagManager = false">Fermer</button>
        </div>
      </section>
    </div>

    <div v-if="editing" class="modal-backdrop" role="presentation" @click.self="closeForm">
      <section class="modal" role="dialog" aria-modal="true" aria-labelledby="form-title">
        <h2 id="form-title">{{ editing.id ? 'Modifier un element' : 'Ajouter un element' }}</h2>
        <ItemForm :item="editing" @submit="saveItem" @cancel="closeForm" />
      </section>
    </div>

    <footer>
      <strong>&copy; {{ new Date().getFullYear() }} Samnick Biga</strong>
      <a href="#accueil" style="text-decoration: none;">Retour en haut &uarr;</a>
    </footer>
  </div>
</template>

<script setup>
import { computed, nextTick, onBeforeUnmount, onMounted, reactive, ref, watch } from 'vue';
import { LockKeyhole, Plus, ArrowLeft } from 'lucide-vue-next';
import ContentSection from './components/ContentSection.vue';

const nameWords = ['SAMNICK', 'BIGA', 'RAOUL', 'AUBIN'];

function getGlobalCharIndex(wIdx, cIdx) {
  let count = 0;
  for (let i = 0; i < wIdx; i++) {
    count += nameWords[i].length + 1;
  }
  return count + cIdx;
}
import ItemForm from './components/ItemForm.vue';
import PillBadge from './components/PillBadge.vue';
import StackToolsSection from './components/StackToolsSection.vue';
import TagManager from './components/TagManager.vue';
import { authState, clearToken, setToken } from './store/auth';
import { createItem, deleteItem, getItems, login, updateItem } from './services/api';
import { tagTone } from './services/tags';

const profilePhoto = `${import.meta.env.BASE_URL}profile-photo.jpg`;
const contactEmail = 'samuelbiga10@gmail.com';
const whatsappUrl = 'https://wa.me/237654881101?text=Bonjour%20Samnick%2C%20je%20viens%20de%20voir%20votre%20portfolio%20et%20je%20souhaite%20%C3%A9changer%20avec%20vous.';

const filters = [
  { label: 'Tous', value: '' },
  { label: 'Parcours', value: 'parcours' },
  { label: 'Competences', value: 'competence' },
  { label: 'Realisations', value: 'realisation' },
];

const futureProjectCategories = ['Cloud & Virtualisation', 'Automatisation', 'Forensic', 'DevSecOps', 'Réseau'];

const selectedType = ref('');
const selectedCategory = ref('');
const showLogin = ref(false);
const showTagManager = ref(false);
const items = ref([]);
const loading = ref(false);
const loadError = ref('');
const authError = ref('');
const editing = ref(null);
const caseStudyItem = ref(null);
const caseModal = ref(null);
const caseProgress = ref(0);
const emailCopied = ref(false);
const credentials = reactive({ username: '', password: '' });

let revealObserver;
let prefersReducedMotion;

const typeFilteredItems = computed(() => (selectedType.value ? items.value.filter((item) => item.type === selectedType.value) : items.value));

const caseStudyStack = computed(() => {
  if (!caseStudyItem.value) return [];
  const list = [];
  if (caseStudyItem.value.subtitle) {
    list.push(...caseStudyItem.value.subtitle.split(',').map((e) => e.trim()).filter(Boolean));
  }
  const tools = caseStudyItem.value.content?.tools;
  if (tools) {
    list.push(...tools.split(',').map((e) => e.trim()).filter(Boolean));
  }
  return list.length ? list : ['À compléter'];
});

const activeCaseStudy = computed(() => {
  if (!caseStudyItem.value) return [];
  const c = caseStudyItem.value.content || {};
  const type = caseStudyItem.value.type;
  const sections = [];
  let num = 1;

  sections.push({
    number: String(num++).padStart(2, '0'),
    title: 'Présentation & Contexte',
    body: caseStudyItem.value.description,
  });

  if (c.objective) {
    sections.push({
      number: String(num++).padStart(2, '0'),
      title: type === 'realisation' ? 'Objectif' : type === 'parcours' ? 'Missions & Objectifs' : 'Contexte & Utilisation',
      body: c.objective,
    });
  }

  if (c.architecture) {
    sections.push({
      number: String(num++).padStart(2, '0'),
      title: type === 'realisation' ? 'Architecture / méthode' : type === 'parcours' ? 'Activités clés & Déroulement' : 'Détails techniques & Niveau',
      body: c.architecture,
      image: c.architecture_image,
    });
  } else if (c.architecture_image) {
    sections.push({
      number: String(num++).padStart(2, '0'),
      title: 'Illustration / Document',
      body: '',
      image: c.architecture_image,
    });
  }

  if (c.alert_flow) {
    sections.push({
      number: String(num++).padStart(2, '0'),
      title: type === 'realisation' ? 'Flux d\'alerte' : type === 'parcours' ? 'Méthodologie & Organisation' : 'Cas d\'usage & Projets liés',
      body: c.alert_flow,
    });
  }

  if (c.lessons) {
    sections.push({
      number: String(num++).padStart(2, '0'),
      title: type === 'realisation' ? 'Ce que j\'ai appris' : type === 'parcours' ? 'Compétences développées' : 'Points forts & Maîtrise',
      body: c.lessons,
    });
  }

  if (c.impact) {
    sections.push({
      number: String(num++).padStart(2, '0'),
      title: type === 'realisation' ? 'Impact' : type === 'parcours' ? 'Bilan / Résultat' : 'Certifications / Attestation',
      body: c.impact,
    });
  }

  if (sections.length === 1) {
    sections.push({
      number: String(num++).padStart(2, '0'),
      title: 'Détails complémentaires',
      body: "Vous pouvez compléter cette fiche depuis l'espace Administration pour ajouter des images, des explications détaillées ou un bilan.",
    });
  }

  return sections;
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

onMounted(() => {
  prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  setupScrollReveal();
  setupPhotoParallax();
  loadItems();
});

onBeforeUnmount(() => {
  revealObserver?.disconnect();
  window.removeEventListener('scroll', updatePhotoParallax);
});

watch(selectedType, () => {
  selectedCategory.value = '';
});

async function loadItems() {
  loading.value = true;
  loadError.value = '';
  try {
    items.value = await getItems();
    await nextTick();
    setupScrollReveal();
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

function handleSessionExpired() {
  clearToken();
  showTagManager.value = false;
  closeForm();
  authError.value = 'Session expirée. Veuillez vous reconnecter.';
  showLogin.value = true;
}

function openCreate() {
  editing.value = { type: 'parcours', category: 'Cursus', featured: false, title: '', subtitle: '', description: '' };
}

function openEdit(item) {
  editing.value = { ...item };
}

function openCaseStudy(item) {
  caseStudyItem.value = item;
  caseProgress.value = 0;
  nextTick(updateCaseProgress);
}

function closeCaseStudy() {
  caseStudyItem.value = null;
  caseProgress.value = 0;
}

function setupScrollReveal() {
  revealObserver?.disconnect();
  const revealTargets = document.querySelectorAll('.reveal-on-scroll');

  if (prefersReducedMotion || !('IntersectionObserver' in window)) {
    revealTargets.forEach((target) => target.classList.add('is-visible'));
    return;
  }

  revealObserver = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          revealObserver.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.16, rootMargin: '0px 0px -80px 0px' },
  );

  revealTargets.forEach((target) => revealObserver.observe(target));
}

function setupPhotoParallax() {
  updatePhotoParallax();
  window.addEventListener('scroll', updatePhotoParallax, { passive: true });
}

function updatePhotoParallax() {
  const photo = document.querySelector('.profile-photo-card img');
  if (!photo || prefersReducedMotion) return;

  const offset = Math.min(18, Math.max(-18, window.scrollY * -0.035));
  photo.style.transform = `translateY(${offset}px) scale(1.035)`;
}

function updateCaseProgress() {
  const modal = caseModal.value;
  if (!modal) return;

  const maxScroll = modal.scrollHeight - modal.clientHeight;
  caseProgress.value = maxScroll > 0 ? Math.min(100, Math.round((modal.scrollTop / maxScroll) * 100)) : 100;
}

async function copyEmail() {
  try {
    await navigator.clipboard.writeText(contactEmail);
    emailCopied.value = true;
    window.setTimeout(() => {
      emailCopied.value = false;
    }, 1800);
  } catch {
    window.location.href = `mailto:${contactEmail}`;
  }
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

<style scoped>
.case-section-image-wrapper {
  margin-top: 1.5rem;
  border-radius: var(--radius-md);
  overflow: hidden;
  border: 1px solid var(--border);
  background: var(--surface-1);
}
.case-section-image-wrapper img {
  width: 100%;
  height: auto;
  display: block;
}
</style>
