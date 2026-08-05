<template>
  <div class="app-shell">
    <Preloader />
    <div class="topbar-wrapper">
      <header class="topbar">
        <a href="#accueil" class="brand" @click="playClick" @mouseenter="playHover">
          <DynamicLogo />
          <span style="margin-left: 12px;">Mon portfolio</span>
        </a>
        <button class="hamburger" @click="menuOpen = !menuOpen; playClick()" aria-label="Menu">
          <span class="hamburger-line"></span>
          <span class="hamburger-line"></span>
          <span class="hamburger-line"></span>
        </button>
        <nav class="nav-links" :class="{ 'is-open': menuOpen }" aria-label="Navigation principale" @click="menuOpen = false">
          <button class="nav-button" @click.stop="handleToggleSound" @mouseenter="playHover" aria-label="Activer/Désactiver le son">
            {{ audioEnabled ? '🔊 Son ON' : '🔇 Son OFF' }}
          </button>
          <a href="#apropos" @click="playClick" @mouseenter="playHover">À propos</a>
          <a href="#parcours" @click="playClick" @mouseenter="playHover">Parcours</a>
          <a href="#competences" @click="playClick" @mouseenter="playHover">Stack & outils</a>
          <a href="#realisations" @click="playClick" @mouseenter="playHover">Réalisations</a>
          <a href="#contact" @click="playClick" @mouseenter="playHover">Contact</a>
          <button v-if="!authState.token" class="nav-button" type="button" @click.stop="showLogin = true; menuOpen = false; playClick()" @mouseenter="playHover">Admin</button>
          <button v-else class="nav-button" type="button" @click.stop="logout(); menuOpen = false; playClick()" @mouseenter="playHover">Déconnexion</button>
        </nav>
      </header>
    </div>

    <main id="accueil" v-if="!isNotFound">
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
                :style="charStyles[getGlobalCharIndex(wIdx, cIdx)]"
                @mousemove="handleCharMouseMove($event, getGlobalCharIndex(wIdx, cIdx))"
                @mouseleave="handleCharMouseLeave(getGlobalCharIndex(wIdx, cIdx))"
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
            <a class="button button-pill primary" href="#realisations" @click="playClick" @mouseenter="playHover">
              Voir mes projets
              <span class="icon-circle"><ArrowDown :size="16" /></span>
            </a>
            <a class="button button-pill secondary" href="#contact" @click="playClick" @mouseenter="playHover">
              Me contacter
              <span class="icon-circle"><ArrowRight :size="16" /></span>
            </a>
          </div>
          <a class="scroll-cue" href="#realisations" aria-label="Descendre vers les projets" @click="playClick" @mouseenter="playHover">
            <span></span>
            Défiler
          </a>
        </div>
        <figure class="hero-visual profile-photo-card">
          <img :src="profilePhoto" alt="Portrait de SAMNICK BIGA RAOUL AUBIN" />
        </figure>
      </section>

      <section class="logo-wall-section reveal-on-scroll">
        <p class="logo-wall-title">Ils m'ont fait confiance</p>
        <div class="logo-wall-grid">
          <img src="/Logos/paness.jpg" alt="PANESS IT" title="PANESS IT" />
          <img src="/Logos/ihtm.png" alt="IHTM" title="IHTM" />
          <img src="/Logos/minat.png" alt="MINAT" title="MINAT" />
          <img src="/Logos/minsep.jpg" alt="MINSEP" title="MINSEP" />
          <img src="/Logos/hgy.png" alt="Hôpital Général de Yaoundé" title="Hôpital Général de Yaoundé" />
          <img src="/Logos/hcy.jpg" alt="Hôpital Central de Yaoundé" title="Hôpital Central de Yaoundé" />
          <img src="/Logos/cury.jpg" alt="CURY" title="CURY" />
        </div>
      </section>

      <section class="about-section reveal-on-scroll" id="apropos" aria-labelledby="about-title" style="position: relative; overflow: hidden;">
        <div class="giant-watermark">ÉVOLUER</div>
        <div class="section-heading" style="position: relative; z-index: 1;">
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
              <button class="button primary" type="button" @click="openCaseStudy(featuredProject); playClick()" @mouseenter="playHover">
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
          <button class="button secondary" type="button" @click="showTagManager = true; playClick()" @mouseenter="playHover">
            Gérer les tags
          </button>
          <button class="button primary" type="button" @click="openCreate(); playClick()" @mouseenter="playHover">
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
          @click="selectedType = filter.value; playClick()"
          @mouseenter="playHover"
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
          @click="selectedCategory = ''; playClick()"
          @mouseenter="playHover"
        >
          Tous les tags
        </button>
        <button
          v-for="category in categoryFilters"
          :key="category"
          class="filter-pill"
          :class="[{ active: selectedCategory === category }, tagTone(category)]"
          type="button"
          :aria-pressed="selectedCategory === category"
          @click="selectedCategory = category; playClick()"
          @mouseenter="playHover"
        >
          <span style="margin-right: 4px;" aria-hidden="true">{{ getCategoryIcon(category) }}</span>{{ category }}
        </button>
      </section>

      <Transition name="filter-swap" mode="out-in">
        <div :key="`${selectedType}-${selectedCategory}`" class="portfolio-results">
          <p v-if="loading" class="empty-state" role="status" style="display: flex; justify-content: center; align-items: center; min-height: 50vh; font-size: 1.2rem; color: var(--ubuntu-orange);">Chargement du portfolio...</p>
          <p v-else-if="loadError" class="form-error" role="alert" style="text-align: center;">{{ loadError }}</p>

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
              layout="zig-zag"
              @edit="openEdit"
              @delete="remove"
              @view-case="openCaseStudy"
            />
          </template>
        </div>
      </Transition>

      <TestimonialSection 
        :testimonials="testimonials"
        :editable="Boolean(authState.token)"
        @toggle-visibility="handleToggleTestimonialVisibility"
        @delete="handleDeleteTestimonial"
        @add-testimonial="showTestimonialForm = true; playClick()"
      />

      <section class="contact-section reveal-on-scroll" id="contact" aria-labelledby="contact-title">
        <div class="contact-copy">
          <PillBadge tone="orange">Contact</PillBadge>
          <h2 id="contact-title">Posez-moi vos questions.</h2>
          <p>
            Vous avez une question ou une proposition ? Envoyez-moi un message directement, ou utilisez l'une des suggestions ci-dessous !
          </p>
          
          <div class="suggestions-chips">
            <button v-for="q in suggestedQuestions" :key="q" type="button" class="chip-button" @click="fillQuestion(q); playClick()" @mouseenter="playHover">
              {{ q }}
            </button>
          </div>

          <form @submit.prevent="handleContactSubmit(); playClick()" class="styled-contact-form">
            <div class="form-row">
              <span class="row-label">À</span>
              <span class="row-static-text">{{ contactEmail }}</span>
              <span class="row-feedback" v-if="contactStatus === 'success'">Bien reçu</span>
            </div>
            
            <div class="form-row">
              <label for="contact-email" class="row-label">De</label>
              <input id="contact-email" v-model.trim="contactDraft.email" type="email" required placeholder="vous@exemple.com" class="row-input" />
            </div>

            <div class="form-row">
              <label for="contact-subject" class="row-label">Sujet</label>
              <input id="contact-subject" v-model.trim="contactDraft.subject" type="text" placeholder="Entrez le sujet de votre message" class="row-input" />
            </div>

            <div class="form-row textarea-row">
              <label for="contact-msg" class="row-label">Message</label>
              <textarea id="contact-msg" v-model.trim="contactDraft.message" required rows="5" placeholder="Bonjour..." class="row-input"></textarea>
            </div>

            <p v-if="contactStatus === 'error'" class="form-error" role="alert" style="margin-top: 1rem;">{{ contactError }}</p>

            <div class="form-footer">
              <button class="send-button" type="submit" :disabled="contactStatus === 'sending'" @mouseenter="playHover">
                {{ contactStatus === 'sending' ? 'Envoi...' : 'Envoyer' }}
              </button>
            </div>
          </form>
        </div>

        <div class="contact-panel" aria-label="Coordonnées">
          <a href="mailto:samuelbiga10@gmail.com" @click="playClick" @mouseenter="playHover">
            <span>Email</span>
            <strong>samuelbiga10@gmail.com</strong>
          </a>
          <a href="https://wa.me/237654881101" target="_blank" rel="noreferrer" @click="playClick" @mouseenter="playHover">
            <span>WhatsApp</span>
            <strong>+237 654 881 101</strong>
          </a>
          <a href="https://www.linkedin.com/in/aubinbiga" target="_blank" rel="noreferrer" @click="playClick" @mouseenter="playHover">
            <span>LinkedIn</span>
            <strong>linkedin.com/in/aubinbiga</strong>
          </a>
          <a href="https://github.com/Biga14-samuel" target="_blank" rel="noreferrer" @click="playClick" @mouseenter="playHover">
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
    <NotFound v-else />

    <div v-if="caseStudyItem" class="modal-backdrop" role="presentation" @click.self="closeCaseStudy(); playClick()">
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
          <button class="case-back-button" type="button" aria-label="Retourner en arrière" @click="closeCaseStudy(); playClick()" @mouseenter="playHover">
            <ArrowLeft :size="20" aria-hidden="true" />
            <span>Retour</span>
          </button>
          <button class="case-close" type="button" aria-label="Fermer la vue" @click="closeCaseStudy(); playClick()" @mouseenter="playHover">×</button>
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
             <a v-if="caseStudyItem.github_url" :href="caseStudyItem.github_url" target="_blank" rel="noreferrer" class="button secondary" @click="playClick" @mouseenter="playHover">Code source (GitHub)</a>
             <a v-if="caseStudyItem.demo_url" :href="caseStudyItem.demo_url" target="_blank" rel="noreferrer" class="button primary" @click="playClick" @mouseenter="playHover">Démonstration en ligne</a>
          </div>
        </div>
      </section>
    </div>

    <div v-if="showLogin" class="modal-backdrop" role="presentation" @click.self="showLogin = false; playClick()">
      <section class="modal login-card" role="dialog" aria-modal="true" aria-labelledby="login-title">
        <LockKeyhole aria-hidden="true" :size="34" />
        <h2 id="login-title">Administration du portfolio</h2>
        <p>Connexion reservee au proprietaire du portfolio.</p>
        <form @submit.prevent="handleLogin(); playClick()">
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
            <button class="button secondary" type="button" @click="showLogin = false; playClick()" @mouseenter="playHover">Annuler</button>
            <button class="button primary" type="submit" @mouseenter="playHover">Se connecter</button>
          </div>
        </form>
      </section>
    </div>

    <div v-if="showTagManager" class="modal-backdrop" role="presentation" @click.self="showTagManager = false; playClick()">
      <section class="modal" role="dialog" aria-modal="true" aria-labelledby="tag-manager-title">
        <h2 id="tag-manager-title">Gestion des tags</h2>
        <TagManager @session-expired="handleSessionExpired" />
        <div class="form-actions" style="margin-top: 1.5rem;">
          <button class="button secondary" type="button" @click="showTagManager = false; playClick()" @mouseenter="playHover">Fermer</button>
        </div>
      </section>
    </div>

    <div v-if="editing" class="modal-backdrop" role="presentation" @click.self="closeForm(); playClick()">
      <section class="modal" role="dialog" aria-modal="true" aria-labelledby="form-title">
        <h2 id="form-title">{{ editing.id ? 'Modifier un element' : 'Ajouter un element' }}</h2>
        <ItemForm :item="editing" @submit="saveItem" @cancel="closeForm(); playClick()" />
      </section>
    </div>

    <div v-if="showTestimonialForm" class="modal-backdrop" role="presentation" @click.self="showTestimonialForm = false; playClick()">
      <section class="modal" role="dialog" aria-modal="true" aria-labelledby="testimonial-form-title">
        <h2 id="testimonial-form-title">Laisser un témoignage</h2>
        <form @submit.prevent="handleCreateTestimonial(); playClick()">
          <label>
            Votre nom complet *
            <input v-model.trim="testimonialDraft.client_name" required minlength="2" maxlength="140" />
          </label>
          <label>
            Votre entreprise ou poste (optionnel)
            <input v-model.trim="testimonialDraft.client_company" maxlength="140" />
          </label>
          <label>
            Lien de votre profil LinkedIn (optionnel)
            <input v-model.trim="testimonialDraft.linkedin_url" type="url" maxlength="500" placeholder="https://linkedin.com/in/..." />
          </label>
          <label>
            Votre message *
            <textarea v-model.trim="testimonialDraft.content" required minlength="5" maxlength="2000" rows="5"></textarea>
          </label>
          <p v-if="testimonialError" class="form-error" role="alert">{{ testimonialError }}</p>
          <div class="form-actions">
            <button class="button secondary" type="button" @click="showTestimonialForm = false; playClick()" @mouseenter="playHover">Annuler</button>
            <button class="button primary" type="submit" @mouseenter="playHover">Envoyer</button>
          </div>
        </form>
      </section>
    </div>
    <footer class="footer">
      <p>© 2026 Samuel Biga. Tous droits réservés.</p>
    </footer>

    <button 
      class="scroll-to-top" 
      :class="{ visible: showScrollToTop }" 
      @click="scrollToTop(); playClick()" 
      aria-label="Retour en haut"
      @mouseenter="playHover"
    >
      <ArrowUp :size="24" />
    </button>
  </div>
</template>

<script setup>
import { computed, nextTick, onBeforeUnmount, onMounted, reactive, ref, watch, onUnmounted, onErrorCaptured } from 'vue';
import { LockKeyhole, Plus, ArrowLeft, ArrowUp, ArrowRight, ArrowDown } from 'lucide-vue-next';
import ContentSection from './components/ContentSection.vue';
import DynamicLogo from './components/DynamicLogo.vue';
import Preloader from './components/Preloader.vue';
import { toggleSound, isSoundEnabled, playHover, playClick } from './services/sounds';
import Lenis from '@studio-freight/lenis';
import ItemForm from './components/ItemForm.vue';
import PillBadge from './components/PillBadge.vue';
import StackToolsSection from './components/StackToolsSection.vue';
import TagManager from './components/TagManager.vue';
import { authState, clearToken, setToken } from './store/auth';
import { createItem, deleteItem, getItems, login, updateItem, getTestimonials, createTestimonial, updateTestimonial, deleteTestimonial as apiDeleteTestimonial, sendContactMessage } from './services/api';
import TestimonialSection from './components/TestimonialSection.vue';
import { tagTone } from './services/tags';
import NotFound from './components/NotFound.vue';

const currentPath = ref(window.location.pathname);
const hasError = ref(false);

onErrorCaptured((err) => {
  console.error("Vue Error Captured:", err);
  hasError.value = true;
  return false;
});

const isNotFound = computed(() => {
  return hasError.value || (currentPath.value !== '/' && currentPath.value !== '/index.html' && currentPath.value !== '');
});

const audioEnabled = ref(isSoundEnabled());
const nameWords = ['SAMNICK', 'BIGA', 'RAOUL', 'AUBIN'];
const charStyles = reactive({});
let lastMouseX = 0;
let lenis;
let rafId;

function handleToggleSound() {
  audioEnabled.value = toggleSound();
  if (audioEnabled.value) playClick();
}

function getGlobalCharIndex(wIdx, cIdx) {
  let count = 0;
  for (let i = 0; i < wIdx; i++) {
    count += nameWords[i].length + 1;
  }
  return count + cIdx;
}

function handleCharMouseMove(e, idx) {
  const currentX = e.clientX;
  const deltaX = currentX - (lastMouseX || currentX);
  lastMouseX = currentX;

  const dir = deltaX > 0 ? 1 : deltaX < 0 ? -1 : 0;
  const shiftX = dir !== 0 ? dir * 20 : 14;
  const rotateDeg = dir !== 0 ? dir * 22 : 16;

  charStyles[idx] = {
    transform: `translate(${shiftX}px, -20px) rotate(${rotateDeg}deg) scale(1.24)`,
    color: 'var(--ubuntu-orange-dark)',
  };
}

function handleCharMouseLeave(idx) {
  charStyles[idx] = {
    transform: 'translate(0px, 0px) rotate(0deg) scale(1)',
    color: 'inherit',
  };
}

const profilePhoto = `${import.meta.env.BASE_URL}profile-photo.jpg`;
const contactEmail = 'samuelbiga10@gmail.com';

const filters = [
  { label: 'Tous', value: '' },
  { label: 'Réalisations', value: 'realisation' },
  { label: 'Parcours', value: 'parcours' },
  { label: 'Stack & Outils', value: 'competence' },
];

const categoryIcons = {
  'web': '🌐',
  'data': '📊',
  'cyber': '🔒',
  'system': '⚙️',
  'design': '🎨',
  'mobile': '📱',
  'cloud': '☁️',
  'réseau': '🔌',
  'default': '✨'
};

function getCategoryIcon(cat) {
  const lowerCat = cat.toLowerCase();
  for (const [key, icon] of Object.entries(categoryIcons)) {
    if (lowerCat.includes(key)) return icon;
  }
  return categoryIcons.default;
}

const futureProjectCategories = ['Cloud & Virtualisation', 'Automatisation', 'Forensic', 'DevSecOps', 'Réseau'];

const selectedType = ref('');
const selectedCategory = ref('');
const showLogin = ref(false);
const menuOpen = ref(false);
const showTagManager = ref(false);
const items = ref([]);
const testimonials = ref([]);
const showTestimonialForm = ref(false);
const testimonialDraft = reactive({ client_name: '', client_company: '', linkedin_url: '', content: '' });
const testimonialError = ref('');
const contactDraft = reactive({ email: '', subject: '', message: '' });
const contactStatus = ref('');
const contactError = ref('');
const suggestedQuestions = [
  "Quels sont vos tarifs ?",
  "Êtes-vous disponible pour un emploi ?",
  "Pouvez-vous configurer un firewall Fortinet ?",
  "Quel est votre niveau en Python ?"
];
const loading = ref(false);
const loadError = ref('');
const authError = ref('');
const editing = ref(null);
const caseStudyItem = ref(null);
const caseModal = ref(null);
const caseProgress = ref(0);
const emailCopied = ref(false);
const credentials = reactive({ username: '', password: '' });
const showScrollToTop = ref(false);

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

onMounted(async () => {
  // --- PROTECTION DU CONTENU ---
  // Désactiver le clic droit
  document.addEventListener('contextmenu', (e) => {
    e.preventDefault();
  });

  // Désactiver la copie
  document.addEventListener('copy', (e) => {
    e.preventDefault();
  });

  // Désactiver les raccourcis clavier de développement (F12, Ctrl+Maj+I, Ctrl+U)
  document.addEventListener('keydown', (e) => {
    if (
      e.key === 'F12' || 
      (e.ctrlKey && e.shiftKey && e.key === 'I') || 
      (e.ctrlKey && e.shiftKey && e.key === 'J') || 
      (e.ctrlKey && e.key === 'U') ||
      (e.ctrlKey && e.key === 'S') ||
      (e.ctrlKey && e.key === 'P')
    ) {
      e.preventDefault();
    }
  });

  // -----------------------------

  lenis = new Lenis({
    duration: 1.2,
    easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
    smooth: true,
  });

  function raf(time) {
    lenis.raf(time);
    rafId = requestAnimationFrame(raf);
  }
  rafId = requestAnimationFrame(raf);

  prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  setupScrollReveal();
  setupPhotoParallax();
  loadItems();
  window.addEventListener('scroll', handleScroll, { passive: true });
});

onUnmounted(() => {
  if (rafId) cancelAnimationFrame(rafId);
  if (lenis) lenis.destroy();
  revealObserver?.disconnect();
  window.removeEventListener('scroll', updatePhotoParallax);
  window.removeEventListener('scroll', handleScroll);
});

function handleScroll() {
  const scrollPosition = window.scrollY || document.documentElement.scrollTop;
  const pageHeight = document.documentElement.scrollHeight - document.documentElement.clientHeight;
  showScrollToTop.value = scrollPosition > (pageHeight * 0.4);
}

function scrollToTop() {
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

watch(selectedType, () => {
  selectedCategory.value = '';
});

async function loadItems() {
  loading.value = true;
  loadError.value = '';
  try {
    items.value = await getItems();
    testimonials.value = await getTestimonials(authState.token);
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
async function handleDeleteTestimonial(t) {
  if (!confirm(`Supprimer le témoignage de "${t.client_name}" ?`)) return;
  try {
    await apiDeleteTestimonial(t.id, authState.token);
    await loadItems();
  } catch (error) {
    alert(error.message);
  }
}

async function handleToggleTestimonialVisibility(t, is_visible) {
  try {
    await updateTestimonial(t.id, is_visible, authState.token);
    await loadItems();
  } catch (error) {
    alert(error.message);
  }
}

async function handleCreateTestimonial() {
  testimonialError.value = '';
  try {
    await createTestimonial(testimonialDraft);
    showTestimonialForm.value = false;
    testimonialDraft.client_name = '';
    testimonialDraft.client_company = '';
    testimonialDraft.linkedin_url = '';
    testimonialDraft.content = '';
    alert('Merci ! Votre témoignage a bien été envoyé et sera examiné.');
    await loadItems();
  } catch (error) {
    testimonialError.value = error.message;
  }
}

function fillQuestion(q) {
  if (contactDraft.message && !contactDraft.message.endsWith('\n')) {
    contactDraft.message += '\n' + q;
  } else {
    contactDraft.message += q;
  }
}

async function handleContactSubmit() {
  contactStatus.value = 'sending';
  contactError.value = '';
  try {
    await sendContactMessage(contactDraft.email, contactDraft.subject, contactDraft.message);
    contactStatus.value = 'success';
    contactDraft.email = '';
    contactDraft.subject = '';
    contactDraft.message = '';
    setTimeout(() => {
      if (contactStatus.value === 'success') contactStatus.value = '';
    }, 6000);
  } catch (error) {
    contactStatus.value = 'error';
    contactError.value = error.message || "Une erreur est survenue lors de l'envoi.";
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

.styled-contact-form {
  background: var(--surface-card);
  border: 1px solid var(--outline);
  box-shadow: var(--shadow);
  border-radius: 1.5rem;
  padding: 1.5rem 2rem;
  margin-top: 1.5rem;
  display: flex;
  flex-direction: column;
}

.form-row {
  display: flex;
  align-items: center;
  border-bottom: 1px solid var(--outline);
  padding: 1.2rem 0;
}

.textarea-row {
  align-items: flex-start;
  border-bottom: none;
}

.row-label {
  color: var(--muted);
  width: 80px;
  font-size: 1rem;
  flex-shrink: 0;
  font-weight: 500;
}

.row-static-text {
  color: var(--text);
  flex-grow: 1;
  font-size: 1rem;
  word-break: break-all;
}

.row-feedback {
  color: #10b981;
  font-size: 0.85rem;
  font-weight: 500;
}

.row-input {
  background: transparent;
  border: none;
  color: var(--text);
  font-size: 1rem;
  flex-grow: 1;
  outline: none;
  font-family: inherit;
  resize: none;
  min-width: 0;
}

.row-input::placeholder {
  color: var(--muted);
  opacity: 0.6;
}

.form-footer {
  margin-top: 1.5rem;
}

.send-button {
  background: var(--ubuntu-orange);
  border: none;
  color: #fff;
  padding: 0.6rem 1.5rem;
  border-radius: 999px;
  font-weight: 700;
  font-size: 0.95rem;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s, background 0.2s;
}

.send-button:hover:not(:disabled) {
  background: var(--ubuntu-orange-dark);
  transform: translateY(-2px);
  box-shadow: var(--shadow-lift);
}

.send-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.suggestions-chips {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-top: 1rem;
}

.chip-button {
  background: var(--surface-2);
  border: 1px solid var(--border);
  color: var(--text);
  padding: 0.4rem 0.8rem;
  border-radius: 20px;
  font-size: 0.85rem;
  cursor: pointer;
  transition: background 0.2s, color 0.2s;
}

.chip-button:hover {
  background: var(--accent);
  color: white;
}

.form-success {
  color: #10b981;
  background: rgba(16, 185, 129, 0.1);
  padding: 0.75rem;
  border-radius: var(--radius-sm);
  font-size: 0.9rem;
}

.scroll-to-top {
  position: fixed;
  bottom: 2rem;
  right: 2rem;
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background-color: var(--ubuntu-orange);
  color: white;
  border: none;
  cursor: pointer;
  box-shadow: var(--shadow-lift);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  opacity: 0;
  visibility: hidden;
  transform: translateY(20px);
  transition: opacity 0.4s ease, transform 0.4s ease, visibility 0.4s;
}

.scroll-to-top.visible {
  opacity: 1;
  visibility: visible;
  transform: translateY(0);
}

.scroll-to-top:hover {
  background-color: var(--ubuntu-orange-dark);
  transform: translateY(-3px) scale(1.05);
}

@media (max-width: 768px) {
  .scroll-to-top {
    bottom: 1.5rem;
    right: 1.5rem;
    width: 45px;
    height: 45px;
  }
}
@media (max-width: 560px) {
  .styled-contact-form {
    padding: 1.2rem;
  }
  .row-label {
    width: 60px;
  }
}
.admin-strip {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  margin: 2rem auto;
  text-align: center;
}
.admin-strip > div {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}
</style>
