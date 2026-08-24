<template>
  <div class="app-shell">
    <Toaster 
      position="bottom-left" 
      :toastOptions="{ 
        classNames: {
          success: 'toast-pastel-success',
          error: 'toast-pastel-error'
        },
        style: { borderRadius: '12px', padding: '16px', fontSize: '15px' } 
      }" 
    />
    <Preloader />
    <div class="cursor-orb" :style="cursorStyle" aria-hidden="true"></div>
    <div class="topbar-wrapper">
      <header class="topbar">
        <a href="#accueil" class="brand" @click="playClick" @mouseenter="playHover">
          <DynamicLogo />
          <span style="margin-left: 12px;">Mon portfolio</span>
        </a>
        <button class="hamburger" @click.stop="menuOpen = !menuOpen; playClick()" aria-label="Menu">
          <span class="hamburger-line"></span>
          <span class="hamburger-line"></span>
          <span class="hamburger-line"></span>
        </button>
        <nav class="nav-links" :class="{ 'is-open': menuOpen }" aria-label="Navigation principale" @click="menuOpen = false">
          <button class="nav-button nav-button--sound" @click.stop="handleToggleSound" @mouseenter="playHover" aria-label="Activer/Désactiver le son">
            {{ audioEnabled ? 'Son ON' : 'Son OFF' }}
          </button>
          <a href="#apropos" @click="playClick" @mouseenter="playHover">À propos</a>
          <a href="#parcours" @click="playClick" @mouseenter="playHover">Parcours</a>
          <a href="#competences" @click="playClick" @mouseenter="playHover">Stack & outils</a>
          <a href="#realisations" @click="playClick" @mouseenter="playHover">Réalisations</a>
          <a href="#blog" @click="playClick" @mouseenter="playHover">Blog</a>
          <a href="#temoignages" @click="playClick" @mouseenter="playHover">Témoignages</a>
          <a href="#veille" @click="playClick" @mouseenter="playHover">Veille</a>
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
            <a class="button button-pill tertiary" href="/CV_Samnick_Biga_Raoul_Aubin.pdf" download="CV_Samnick_Biga_Raoul_Aubin.pdf" @click="playClick" @mouseenter="playHover" style="background: rgba(233, 84, 32, 0.1); color: var(--ubuntu-orange);">
              Télécharger mon CV
              <span class="icon-circle" style="background: var(--ubuntu-orange); color: white;"><FileDown :size="16" /></span>
            </a>
          </div>
          <a class="scroll-cue" href="#realisations" aria-label="Descendre vers les projets" @click="playClick" @mouseenter="playHover">
            <span></span>
            Défiler
          </a>
        </div>
        <figure class="hero-visual profile-photo-card">
          <img :src="profilePhoto" alt="Portrait de SAMNICK BIGA RAOUL AUBIN" @error="handleImgError" />
        </figure>
      </section>

      <section class="logo-wall-section reveal-on-scroll">
        <p class="logo-wall-title">Ils m'ont fait confiance</p>
        <div class="logo-wall-grid">
          <img src="/Logos/paness.jpg" alt="PANESS IT" title="PANESS IT" @error="handleImgError" />
          <img src="/Logos/ihtm.png" alt="IHTM" title="IHTM" @error="handleImgError" />
          <img src="/Logos/minat.png" alt="MINAT" title="MINAT" @error="handleImgError" />
          <img src="/Logos/minsep.jpg" alt="MINSEP" title="MINSEP" @error="handleImgError" />
          <img src="/Logos/hgy.png" alt="Hôpital Général de Yaoundé" title="Hôpital Général de Yaoundé" @error="handleImgError" />
          <img src="/Logos/hcy.jpg" alt="Hôpital Central de Yaoundé" title="Hôpital Central de Yaoundé" @error="handleImgError" />
          <img src="/Logos/cury.jpg" alt="CURY" title="CURY" @error="handleImgError" />
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

      <Transition name="filter-swap" mode="out-in" @after-enter="setupScrollReveal">
        <div :key="`${selectedType}-${selectedCategory}`" class="portfolio-results">
          <div v-if="loading" class="skeleton-container" aria-label="Chargement du portfolio...">
            <div class="skeleton-grid">
              <div v-for="n in 3" :key="n" class="skeleton-card">
                <div class="skeleton-img"></div>
                <div class="skeleton-content">
                  <div class="skeleton-title"></div>
                  <div class="skeleton-text"></div>
                  <div class="skeleton-text short"></div>
                </div>
              </div>
            </div>
          </div>
          <div v-else class="portfolio-content">
            <p v-if="loadError" class="form-error portfolio-load-error" role="alert">{{ loadError }}</p>

            <ContentSection
              v-if="!selectedType || selectedType === 'parcours'"
              id="parcours"
              title="Mon parcours"
              :items="grouped.parcours"
              empty="Aucun parcours publié pour le moment."
              :editable="Boolean(authState.token)"
              @edit="openEdit"
              @delete="remove"
              @view-case="openCaseStudy"
            />
            <StackToolsSection
              v-if="!selectedType || selectedType === 'competence'"
              id="competences"
              :items="grouped.competence"
              empty="Aucune compétence publiée pour le moment."
              :editable="Boolean(authState.token)"
              @edit="openEdit"
              @delete="remove"
              @view-case="openCaseStudy"
            />
            <RealisationsSection
              v-if="!selectedType || selectedType === 'realisation'"
              :items="grouped.realisation"
              :editable="Boolean(authState.token)"
              @edit="openEdit"
              @delete="remove"
              @view-case="openCaseStudy"
              @add="openCreate('realisation'); playClick()"
            />
            <section
              v-if="!selectedType || selectedType === 'blog'"
              class="blog-section reveal-on-scroll"
              id="blog"
              aria-labelledby="blog-title"
            >
              <div class="section-heading">
                <PillBadge tone="aubergine">Blog</PillBadge>
                <h2 id="blog-title">Blog</h2>
              </div>
              <p v-if="authState.token" class="blog-intro">Articles, notes et retours d'expérience publiés depuis l'administration. Les PDF peuvent être attachés à chaque article.</p>
              <div v-if="grouped.blog.length" class="blog-grid blog-grid--managed">
                <ItemCard
                  v-for="item in grouped.blog"
                  :key="item.id"
                  :item="item"
                  :editable="Boolean(authState.token)"
                  @edit="openEdit"
                  @delete="remove"
                  @view-case="openCaseStudy"
                />
              </div>
              <div v-else class="empty-state-card blog-empty-state">
                <SearchX class="empty-icon" :size="48" />
                <p>Aucun article publié pour le moment. Les articles seront disponibles ici dès qu'ils seront ajoutés.</p>
                <button v-if="authState.token" class="button primary" type="button" @click="openCreate('blog'); playClick()" @mouseenter="playHover">Ajouter un article</button>
              </div>
            </section>
          </div>
        </div>
      </Transition>

      <TestimonialSection 
        :testimonials="testimonials"
        :editable="Boolean(authState.token)"
        :loading="loading"
        @toggle-visibility="handleToggleTestimonialVisibility"
        @delete="handleDeleteTestimonial"
        @add-testimonial="showTestimonialForm = true; playClick()"
      />

      <section class="watch-section reveal-on-scroll" id="veille" aria-labelledby="veille-title">
        <div class="section-heading">
          <PillBadge tone="blue">Veille automatique</PillBadge>
          <h2 id="veille-title">Surveillance des vulnérabilités critiques en temps réel</h2>
        </div>
        <div class="veille-status-bar">
          <span>Surveillance active</span>
          <span>Dernière mise à jour : {{ veilleUpdatedAtLabel || '—' }}</span>
          <span>{{ veilleItems.length }} vulnérabilités affichées</span>
        </div>
        <div class="veille-grid">
          <article v-for="item in veilleItems" :key="item.cveID" class="veille-card">
            <div class="veille-card__top">
              <strong>{{ item.cveID }}</strong>
              <span>{{ item.dateAdded }}</span>
            </div>
            <h3>{{ item.vendorProject }} {{ item.product }}</h3>
            <p>{{ item.shortDescription }}</p>
            <div class="veille-actions">
              <a :href="veilleSourceUrl" target="_blank" rel="noreferrer" class="button secondary" @click="playClick" @mouseenter="playHover">Source officielle</a>
            </div>
          </article>
        </div>
      </section>
      <section class="contact-section contact-section--artistic reveal-on-scroll" id="contact" aria-labelledby="contact-title">
        <div class="contact-copy">
          <PillBadge tone="orange">Contact</PillBadge>
          <h2 id="contact-title">Posez-moi vos questions.</h2>
          <p>
            Vous avez une question ou une proposition ? Envoyez-moi un message directement, ou utilisez l'une des suggestions ci-dessous !
          </p>
          

          <form @submit.prevent="handleContactSubmit" class="styled-contact-form">
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

        <aside class="contact-aside" aria-label="Coordonnées et questions rapides">
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

          <div class="contact-suggestions" aria-label="Questions rapides">
            <span class="contact-suggestions__title">Questions rapides</span>
            <div class="suggestions-chips">
              <button v-for="q in suggestedQuestions" :key="q" type="button" class="chip-button" @click="fillQuestion(q); playClick()" @mouseenter="playHover">
                {{ q }}
              </button>
            </div>
          </div>

        </aside>
      </section>
    </main>
    <NotFound v-else />

    <div v-if="caseStudyItem" class="modal-backdrop" role="presentation" @click.self="closeCaseStudy(); playClick()">
      <section
        ref="caseModal"
        :class="['case-modal', { 'case-modal--project': normalizeType(caseStudyItem.type) === 'realisation' }]"
        role="dialog"
        aria-modal="true"
        aria-labelledby="case-title"
        @scroll="updateCaseProgress"
      >
        <div class="case-progress" aria-hidden="true">
          <span :style="{ width: `${caseProgress}%` }"></span>
        </div>
        <div class="case-nav-header">
          <button class="case-back-button" type="button" aria-label="Retourner en arrière" @click="closeCaseStudy(); playClick()" @mouseenter="playHover">
            <ArrowLeft :size="20" aria-hidden="true" />
            <span>Retour</span>
          </button>
        </div>
        <div class="case-hero" :class="{ 'case-hero--has-image': Boolean(casePrimaryImage) }">
          <div class="case-hero-copy" :style="storyStyle(0)">
            <PillBadge :tone="tagTone(caseStudyItem.category)">{{ stripEmojis(caseStudyItem.category) }}</PillBadge>
            <h2 id="case-title">{{ stripEmojis(caseStudyItem.title) }}</h2>
            <p>{{ stripEmojis(caseStudyItem.description) }}</p>
            <div v-if="normalizeType(caseStudyItem.type) === 'realisation' && (caseStudyItem.demo_url || caseStudyItem.github_url || casePdfUrl)" class="project-quick-actions">
              <a v-if="caseStudyItem.demo_url" :href="caseStudyItem.demo_url" target="_blank" rel="noreferrer" class="project-action project-action--primary" @click="playClick" @mouseenter="playHover"><ExternalLink :size="18" aria-hidden="true" /><span>Voir la démo</span></a>
              <a v-if="caseStudyItem.github_url" :href="caseStudyItem.github_url" target="_blank" rel="noreferrer" class="project-action" @click="playClick" @mouseenter="playHover"><Github :size="18" aria-hidden="true" /><span>Code source</span></a>
              <a v-if="casePdfUrl" :href="casePdfUrl" target="_blank" rel="noreferrer" class="project-action" @click="playClick" @mouseenter="playHover"><FileText :size="18" aria-hidden="true" /><span>Documentation PDF</span></a>
            </div>
          </div>
          <figure v-if="casePrimaryImage" class="case-hero-visual case-main-visual" :class="{ 'is-loaded': caseHeroImageLoaded }" :style="storyStyle(1)">
            <img
              :src="casePrimaryImage"
              :alt="`Illustration de ${stripEmojis(caseStudyItem.title)}`"
              data-hide-on-error="1"
              class="case-clickable-image"
              @click="openImageViewer(caseDetailImages, 0, stripEmojis(caseStudyItem.title)); playClick()"
              @mouseenter="playHover"
              @load="handleCaseHeroImageLoad"
              @error="handleCaseHeroImageError"
            />
            <figcaption class="case-gallery-caption">Cliquer pour agrandir</figcaption>
          </figure>
        </div>

        <!-- ===== REALISATION: Vue immersive (SOC timeline ou galerie moodboard) ===== -->
        <template v-if="normalizeType(caseStudyItem.type) === 'realisation'">
          <!-- SOC Project → Timeline verticale -->
          <div v-if="isSocProject" class="case-immersive-block" :style="storyStyle(casePrimaryImage ? 2 : 1)">
            <ProjectTimeline
              :steps="socTimelineSteps"
              @open-lightbox="(imgs, idx, title) => { openImageViewer(imgs, idx, title); playClick(); }"
            />
          </div>

          <!-- Autres projets → Galerie moodboard + case study classique -->
          <template v-else>
            <div v-if="caseDetailImages.length" class="case-immersive-block" :style="storyStyle(casePrimaryImage ? 2 : 1)">
              <ProjectGallery
                :images="caseDetailImages"
                :project-title="stripEmojis(caseStudyItem.title)"
                :tools="caseStudyStack"
                @open-lightbox="(idx) => { openImageViewer(caseDetailImages, idx, stripEmojis(caseStudyItem.title)); playClick(); }"
              />
            </div>

            <!-- Case study sections -->
            <div class="case-layout">
              <aside class="case-summary" aria-label="Informations du projet" :style="storyStyle(casePrimaryImage ? 3 : 2)">
                <strong>Informations clés</strong>
                <p v-if="caseStudyItem.subtitle" class="case-summary-period">{{ stripEmojis(caseStudyItem.subtitle) }}</p>
                <ul v-if="caseStudyStack.length">
                  <li v-for="entry in caseStudyStack" :key="entry">{{ entry }}</li>
                </ul>
                <p v-else class="case-summary-empty">Les compétences associées seront précisées prochainement.</p>
              </aside>
              <div class="case-timeline">
                <article v-for="(section, index) in activeCaseStudy" :key="section.title" class="case-step" :class="{ 'is-active': activeCaseStepIndex === index, 'is-past': activeCaseStepIndex > index }" :style="storyStyle((casePrimaryImage ? 4 : 3) + index)">
                  <span>{{ section.number }}</span>
                  <div>
                    <h3>{{ section.title }}</h3>
                    <p style="white-space: pre-wrap;">{{ stripEmojis(section.body) }}</p>
                    <div v-if="section.images?.length" class="case-section-gallery">
                      <figure class="case-section-image-wrapper case-gallery-card case-section-image-wrapper--interactive" :class="{ 'is-loaded': true, 'is-multi': section.images.length > 1 }" @click="openImageViewer(section.images, getSectionImageIndex(section), stripEmojis(section.title)); playClick()" @mouseenter="playHover">
                        <button v-if="section.images.length > 1" type="button" class="case-gallery-nav case-gallery-nav--prev" @click.stop="setSectionImageIndex(section, getSectionImageIndex(section) - 1); playClick()" aria-label="Image précédente"><ArrowLeft :size="18" aria-hidden="true" /></button>
                        <img :src="section.images[getSectionImageIndex(section)]" :alt="`Illustration de ${stripEmojis(section.title)}`" data-hide-on-error="1" @load="markImageLoaded" @error="handleImgError" />
                        <button v-if="section.images.length > 1" type="button" class="case-gallery-nav case-gallery-nav--next" @click.stop="setSectionImageIndex(section, getSectionImageIndex(section) + 1); playClick()" aria-label="Image suivante"><ArrowRight :size="18" aria-hidden="true" /></button>
                        <span class="case-gallery-hint">Cliquer pour agrandir</span>
                      </figure>
                    </div>
                  </div>
                </article>
              </div>
            </div>
          </template>

          <!-- Resources (always shown for realisations) -->
          <div v-if="caseStudyItem.github_url || caseStudyItem.demo_url || casePdfUrl" class="case-resources" :style="storyStyle(10)">
            <strong>Ressources du projet</strong>
            <div style="display: flex; gap: 1rem; margin-top: 1rem; flex-wrap: wrap;">
               <a v-if="caseStudyItem.github_url" :href="caseStudyItem.github_url" target="_blank" rel="noreferrer" class="button secondary" @click="playClick" @mouseenter="playHover">Code source (GitHub)</a>
               <a v-if="casePdfUrl" :href="casePdfUrl" target="_blank" rel="noreferrer" class="button secondary" @click="playClick" @mouseenter="playHover">Documentation PDF</a>
               <a v-if="caseStudyItem.demo_url" :href="caseStudyItem.demo_url" target="_blank" rel="noreferrer" class="button primary" @click="playClick" @mouseenter="playHover">Démonstration en ligne</a>
            </div>
          </div>
        </template>

        <!-- ===== NON-REALISATION: Vue classique (parcours, competence, blog) ===== -->
        <template v-else>
          <div class="case-layout">
            <aside class="case-summary" :aria-label="caseStudyItem.type === 'parcours' ? 'Repères du parcours' : 'Informations du projet'" :style="storyStyle(casePrimaryImage ? 2 : 1)">
              <strong>{{ caseStudyItem.type === 'parcours' ? 'Repères' : 'Informations clés' }}</strong>
              <p v-if="caseStudyItem.subtitle" class="case-summary-period">{{ stripEmojis(caseStudyItem.subtitle) }}</p>
              <ul v-if="caseStudyStack.length">
                <li v-for="entry in caseStudyStack" :key="entry">{{ entry }}</li>
              </ul>
              <p v-else class="case-summary-empty">Les compétences associées seront précisées prochainement.</p>
            </aside>
            <div class="case-timeline">
              <article v-for="(section, index) in activeCaseStudy" :key="section.title" class="case-step" :class="{ 'is-active': activeCaseStepIndex === index, 'is-past': activeCaseStepIndex > index }" :style="storyStyle((casePrimaryImage ? 3 : 2) + index)">
                <span>{{ section.number }}</span>
                <div>
                  <h3>{{ section.title }}</h3>
                  <p style="white-space: pre-wrap;">{{ stripEmojis(section.body) }}</p>
                  <div v-if="section.images?.length" class="case-section-gallery">
                    <figure class="case-section-image-wrapper case-gallery-card case-section-image-wrapper--interactive" :class="{ 'is-loaded': true, 'is-multi': section.images.length > 1 }" @click="openImageViewer(section.images, getSectionImageIndex(section), stripEmojis(section.title)); playClick()" @mouseenter="playHover">
                      <button v-if="section.images.length > 1" type="button" class="case-gallery-nav case-gallery-nav--prev" @click.stop="setSectionImageIndex(section, getSectionImageIndex(section) - 1); playClick()" aria-label="Image précédente"><ArrowLeft :size="18" aria-hidden="true" /></button>
                      <img :src="section.images[getSectionImageIndex(section)]" :alt="`Illustration de ${stripEmojis(section.title)}`" data-hide-on-error="1" @load="markImageLoaded" @error="handleImgError" />
                      <button v-if="section.images.length > 1" type="button" class="case-gallery-nav case-gallery-nav--next" @click.stop="setSectionImageIndex(section, getSectionImageIndex(section) + 1); playClick()" aria-label="Image suivante"><ArrowRight :size="18" aria-hidden="true" /></button>
                      <span class="case-gallery-hint">Cliquer pour agrandir</span>
                    </figure>
                    <div v-if="section.images.length > 1" class="case-gallery-thumbs">
                      <button v-for="(image, imageIndex) in section.images" :key="image" type="button" class="case-gallery-thumb" :class="{ active: imageIndex === getSectionImageIndex(section) }" @click="setSectionImageIndex(section, imageIndex); playClick()" @mouseenter="playHover" :aria-label="`Voir la miniature ${imageIndex + 1}`">
                        <img :src="image" :alt="`Miniature ${imageIndex + 1} de ${stripEmojis(section.title)}`" />
                      </button>
                    </div>
                  </div>
                </div>
              </article>
            </div>
          </div>

          <section v-if="caseGalleryImages.length" class="case-gallery-section" :style="storyStyle((casePrimaryImage ? 3 : 2) + activeCaseStudy.length)">
            <strong>Galerie d'images</strong>
            <p>Quelques vues supplémentaires pour explorer le contexte, les écrans ou les certificats associés.</p>
            <div class="case-gallery-grid">
              <button v-for="(image, imageIndex) in caseGalleryImages" :key="image" type="button" class="case-gallery-card case-gallery-tile" @click="openImageViewer(caseDetailImages, imageIndex + (casePrimaryImage ? 1 : 0), stripEmojis(caseStudyItem.title)); playClick()" @mouseenter="playHover" :aria-label="`Ouvrir l'image ${imageIndex + 1}`">
                <img :src="image" :alt="`Galerie ${imageIndex + 1} de ${stripEmojis(caseStudyItem.title)}`" data-hide-on-error="1" @error="handleImgError" />
              </button>
            </div>
          </section>

          <div v-if="caseStudyItem.github_url || caseStudyItem.demo_url || casePdfUrl" class="case-resources" :style="storyStyle((casePrimaryImage ? 4 : 3) + activeCaseStudy.length + (caseGalleryImages.length ? 1 : 0))">
            <strong>Ressources du projet</strong>
            <div style="display: flex; gap: 1rem; margin-top: 1rem; flex-wrap: wrap;">
               <a v-if="caseStudyItem.github_url" :href="caseStudyItem.github_url" target="_blank" rel="noreferrer" class="button secondary" @click="playClick" @mouseenter="playHover">Code source (GitHub)</a>
               <a v-if="casePdfUrl" :href="casePdfUrl" target="_blank" rel="noreferrer" class="button secondary" @click="playClick" @mouseenter="playHover">Documentation PDF</a>
               <a v-if="caseStudyItem.demo_url" :href="caseStudyItem.demo_url" target="_blank" rel="noreferrer" class="button primary" @click="playClick" @mouseenter="playHover">Démonstration en ligne</a>
            </div>
          </div>
        </template>
      </section>
    </div>

    <ImageLightbox
      v-model="imageViewerOpen"
      :images="imageViewerImages"
      :start-index="imageViewerIndex"
      :title="imageViewerTitle"
    />

    <div v-if="showLogin" class="modal-backdrop" role="presentation" @click.self="showLogin = false; playClick()">
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

    <div v-if="showTestimonialForm" class="modal-backdrop" role="presentation" @click.self="closeTestimonialModal(); playClick()">
      <section class="modal" role="dialog" aria-modal="true" aria-labelledby="testimonial-form-title">
        <template v-if="!showTestimonialSuccess">
          <h2 id="testimonial-form-title">Laisser un témoignage</h2>
          <form @submit.prevent="handleCreateTestimonial">
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
            <div class="form-actions">
              <button class="button secondary" type="button" @click="closeTestimonialModal(); playClick()" @mouseenter="playHover">Annuler</button>
              <button class="button primary" type="submit" @mouseenter="playHover">
                <span v-if="testimonialStatus === 'sending'">Envoi en cours...</span>
                <span v-else>Envoyer</span>
              </button>
            </div>
          </form>
        </template>
        <template v-else>
          <div class="success-view">
            <div class="success-icon-wrapper">
              <CheckCircle class="success-icon" :size="64" />
            </div>
            <h2>Merci beaucoup, {{ testimonialDraft.client_name }} !</h2>
            <p>Votre témoignage a bien été reçu. Il sera examiné et publié très bientôt. Cela me fait énormément plaisir !</p>
            <button class="button primary" type="button" @click="closeTestimonialModal(); playClick()" @mouseenter="playHover">Fermer</button>
          </div>
        </template>
      </section>
    </div>
    <footer class="footer footer-compact">
      <div class="footer-brand">
        <strong>Mon portfolio</strong>
        <p>Administrateur réseau & sécurité | IT Consultant | SOC Analyst Junior</p>
      </div>
      <div class="footer-right">
        <span class="footer-clock">{{ clockLabel }}</span>
        <div class="footer-socials">
          <a href="https://www.linkedin.com/in/aubinbiga" target="_blank" rel="noreferrer">LinkedIn</a>
          <a href="https://github.com/Biga14-samuel" target="_blank" rel="noreferrer">GitHub</a>
          <a href="mailto:samuelbiga10@gmail.com">Email</a>
        </div>
      </div>
      <p class="footer-copy">© 2026 Raoul BIGA. Tous droits réservés.</p>
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
import { LockKeyhole, Plus, ArrowLeft, ArrowUp, ArrowRight, ArrowDown, CheckCircle, FileDown, FileText, ExternalLink, Github, X, SearchX } from 'lucide-vue-next';
import { Toaster, toast } from 'vue-sonner';
import ContentSection from './components/ContentSection.vue';
import ItemCard from './components/ItemCard.vue';
import RealisationsSection from './components/RealisationsSection.vue';
import ProjectGallery from './components/ProjectGallery.vue';
import ProjectTimeline from './components/ProjectTimeline.vue';
import ImageLightbox from './components/ImageLightbox.vue';
import DynamicLogo from './components/DynamicLogo.vue';
import Preloader from './components/Preloader.vue';
import { toggleSound, isSoundEnabled, playHover, playClick, playSuccess, playError } from './services/sounds';
import Lenis from '@studio-freight/lenis';
import ItemForm from './components/ItemForm.vue';
import PillBadge from './components/PillBadge.vue';
import StackToolsSection from './components/StackToolsSection.vue';
import TagManager from './components/TagManager.vue';
import { authState, clearToken, setToken } from './store/auth';
import { createItem, deleteItem, getItems, login, resolveAssetUrl, updateItem, getTestimonials, createTestimonial, updateTestimonial, deleteTestimonial as apiDeleteTestimonial, sendContactMessage, getVeille } from './services/api';
import TestimonialSection from './components/TestimonialSection.vue';
import { tagTone } from './services/tags';
import NotFound from './components/NotFound.vue';
import { stripEmojis } from './utils/sanitize';

const FALLBACK_IMAGE = 'data:image/gif;base64,R0lGODlhAQABAIAAAAUEBAAAACwAAAAAAQABAAACAkQBADs=';

function handleImgError(e) {
  try {
    const img = e.target;
    if (img?.dataset?.hideOnError === '1') {
      img.style.display = 'none';
      return;
    }
    if (!img.dataset.errored) {
      img.dataset.errored = '1';
      img.src = FALLBACK_IMAGE;
    }
  } catch (err) {
    // noop
  }
}

const currentPath = ref(window.location.pathname);
const hasError = ref(false);

function notifySuccess(msg) {
  playSuccess();
  toast.success(msg);
}

function notifyError(msg) {
  playError();
  toast.error(msg);
}

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
const suggestedQuestions = [
  'Êtes-vous disponible pour une opportunité ?',
  'Quels sont vos tarifs pour une mission ?',
  'Pouvez-vous configurer un firewall Fortinet ?',
  'Quel est votre niveau en Python et automatisation ?',
  'Intervenez-vous sur les réseaux et systèmes Linux/Windows ?',
];

const filters = [
  { label: 'Tous', value: '' },
  { label: 'Réalisations', value: 'realisation' },
  { label: 'Parcours', value: 'parcours' },
  { label: 'Stack & Outils', value: 'competence' },
  { label: 'Blog', value: 'blog' },
];

const categoryIcons = {
  'web': '',
  'data': '',
  'cyber': '',
  'system': '',
  'design': '',
  'mobile': '',
  'cloud': '',
  'réseau': '',
  'default': ''
};

function getCategoryIcon(cat) {
  const lowerCat = cat.toLowerCase();
  for (const [key, icon] of Object.entries(categoryIcons)) {
    if (lowerCat.includes(key)) return icon;
  }
  return '';
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
const showTestimonialSuccess = ref(false);
const testimonialStatus = ref('');
const testimonialDraft = reactive({ client_name: '', client_company: '', linkedin_url: '', content: '' });
const testimonialError = ref('');
const contactDraft = reactive({ email: '', subject: '', message: '' });
const contactStatus = ref('');
const contactError = ref('');
const clockLabel = ref('');
const veilleItems = ref([]);
const veilleSourceUrl = ref('https://www.cisa.gov/known-exploited-vulnerabilities-catalog');
const veilleUpdatedAtLabel = ref('');
const loading = ref(false);
const loadError = ref('');
const editing = ref(null);
const caseStudyItem = ref(null);
const caseModal = ref(null);
const caseProgress = ref(0);
const caseHeroImageFailed = ref(false);
const caseHeroImageLoaded = ref(false);
const caseHeroImageIndex = ref(0);
const caseSectionImageIndexes = reactive({});
const imageViewerOpen = ref(false);
const imageViewerImages = ref([]);
const imageViewerIndex = ref(0);
const imageViewerTitle = ref('');
const activeCaseStepIndex = ref(-1);
const emailCopied = ref(false);
const credentials = reactive({ username: '', password: '' });
const showScrollToTop = ref(false);
const cursorPosition = reactive({ x: -100, y: -100 });
const cursorStyle = computed(() => ({ transform: `translate3d(${cursorPosition.x - 18}px, ${cursorPosition.y - 18}px, 0)` }));

let revealObserver;
let prefersReducedMotion;
let clockTimer;
let veilleTimer;

function normalizeType(type) {
  if (!type) return '';
  return String(type)
    .toLowerCase()
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .trim();
}

const typeFilteredItems = computed(() =>
  selectedType.value
    ? items.value.filter((item) => normalizeType(item.type) === normalizeType(selectedType.value))
    : items.value
);

function getChronologyRank(item) {
  const raw = `${item?.subtitle || ''} ${item?.title || ''}`;
  const matches = raw.match(/\b(19|20)\d{2}\b/g);
  const year = matches?.length ? Number(matches[0]) : 9999;
  const monthMatch = raw.toLowerCase().match(/jan|fev|fév|mar|avr|mai|jun|jui|aou|aoû|sep|oct|nov|dec|déc/);
  const monthOrder = {
    jan: 1, fev: 2, fév: 2, mar: 3, avr: 4, mai: 5, jun: 6, jui: 7, aou: 8, aoû: 8, sep: 9, oct: 10, nov: 11, dec: 12, déc: 12,
  };
  return {
    year,
    month: monthMatch ? monthOrder[monthMatch[0].slice(0, 3)] || 0 : 0,
    order: Number(item?.display_order || 0),
    title: item?.title || '',
  };
}

function sortChronologically(list) {
  return [...list].sort((a, b) => {
    const ra = getChronologyRank(a);
    const rb = getChronologyRank(b);
    return ra.year - rb.year || ra.month - rb.month || ra.order - rb.order || ra.title.localeCompare(rb.title);
  });
}

function splitImageSources(raw) {
  if (!raw) return [];
  const values = Array.isArray(raw) ? raw : String(raw).split(/[\n,;|]+/);
  return values.map((value) => stripEmojis(String(value).trim())).filter(Boolean);
}

function updateClock() {
  const now = new Date();
  const mm = String(now.getMonth() + 1).padStart(2, '0');
  const dd = String(now.getDate()).padStart(2, '0');
  const yyyy = now.getFullYear();
  const hh = String(now.getHours()).padStart(2, '0');
  const min = String(now.getMinutes()).padStart(2, '0');
  const sec = String(now.getSeconds()).padStart(2, '0');
  clockLabel.value = `${mm}/${dd}/${yyyy} ${hh}:${min}:${sec}`;
}

function handlePointerMove(e) {
  cursorPosition.x = e.clientX;
  cursorPosition.y = e.clientY;
}

async function loadVeille() {
  try {
    const data = await getVeille(8);
    veilleItems.value = data.items || [];
    veilleSourceUrl.value = data.sourceUrl || veilleSourceUrl.value;
    if (data.updatedAt) {
      veilleUpdatedAtLabel.value = new Date(data.updatedAt * 1000).toLocaleString('fr-FR');
    }
  } catch (error) {
    console.error(error);
  }
}

function getSectionGalleryKey(section) {
  return `${section.number}-${section.title}`;
}

function getSectionImageIndex(section) {
  return caseSectionImageIndexes[getSectionGalleryKey(section)] ?? 0;
}

function setSectionImageIndex(section, index) {
  if (!section?.images?.length) return;
  const key = getSectionGalleryKey(section);
  const total = section.images.length;
  const normalized = ((index % total) + total) % total;
  caseSectionImageIndexes[key] = normalized;
}

function resetCaseImageIndexes() {
  Object.keys(caseSectionImageIndexes).forEach((key) => {
    delete caseSectionImageIndexes[key];
  });
  caseHeroImageIndex.value = 0;
}

function openImageViewer(images, startIndex = 0, title = '') {
  const normalized = (images || []).filter(Boolean);
  if (!normalized.length) return;
  imageViewerImages.value = normalized;
  imageViewerIndex.value = Math.min(Math.max(startIndex, 0), normalized.length - 1);
  imageViewerTitle.value = title;
  imageViewerOpen.value = true;
}

function closeImageViewer() {
  imageViewerOpen.value = false;
}

function nextImage() {
  if (!imageViewerImages.value.length) return;
  imageViewerIndex.value = (imageViewerIndex.value + 1) % imageViewerImages.value.length;
}

function previousImage() {
  if (!imageViewerImages.value.length) return;
  imageViewerIndex.value = (imageViewerIndex.value - 1 + imageViewerImages.value.length) % imageViewerImages.value.length;
}

function handleGlobalKeydown(e) {
  if (!imageViewerOpen.value) return;
  if (e.key === 'Escape') {
    e.preventDefault();
    closeImageViewer();
    return;
  }
  if (e.key === 'ArrowRight') {
    e.preventDefault();
    nextImage();
  }
  if (e.key === 'ArrowLeft') {
    e.preventDefault();
    previousImage();
  }
}

const caseStudyStack = computed(() => {
  if (!caseStudyItem.value) return [];
  const list = [];
  if (caseStudyItem.value.subtitle && caseStudyItem.value.type !== 'parcours') {
    list.push(...caseStudyItem.value.subtitle.split(',').map((e) => stripEmojis(e.trim())).filter(Boolean));
  }
  const tools = caseStudyItem.value.content?.tools;
  if (tools) {
    list.push(...tools.split(',').map((e) => stripEmojis(e.trim())).filter(Boolean));
  }
  return list;
});

const caseDetailImages = computed(() => {
  if (!caseStudyItem.value) return [];
  const coverImages = splitImageSources(caseStudyItem.value?.image_url).map((image) => resolveAssetUrl(image));
  const contentGallery = splitImageSources(caseStudyItem.value?.content?.gallery_images).map((image) => resolveAssetUrl(image));
  return [...new Set([...coverImages, ...contentGallery].filter(Boolean))];
});

const casePrimaryImage = computed(() => caseDetailImages.value[0] || '');
const caseGalleryImages = computed(() => caseDetailImages.value.slice(1));
const casePdfUrl = computed(() => resolveAssetUrl(caseStudyItem.value?.content?.pdf_url || ''));

// Identifies SOC projects: item whose category, title, description or tools contains "soc", "wazuh" or "siem"
const isSocProject = computed(() => {
  const item = caseStudyItem.value;
  if (!item || item.type !== 'realisation') return false;
  const tools = item.content?.tools || '';
  const haystack = `${item.category || ''} ${item.title || ''} ${item.description || ''} ${tools}`.toLowerCase();
  return haystack.includes('soc') || haystack.includes('wazuh') || haystack.includes('siem');
});

// Build timeline steps for the SOC project from the activeCaseStudy sections
const socTimelineSteps = computed(() => {
  if (!isSocProject.value) return [];
  return activeCaseStudy.value.map((section) => {
    // Infer criticality from keywords in title/body
    const raw = `${section.title} ${section.body}`.toLowerCase();
    let criticality = 'info';
    if (raw.includes('malware') || raw.includes('attaque') || raw.includes('alert') || raw.includes('critical')) criticality = 'critical';
    else if (raw.includes('yara') || raw.includes('fim') || raw.includes('detect') || raw.includes('warn')) criticality = 'warning';

    // Infer tool from title
    const toolMap = [
      ['fim', 'FIM / Wazuh'], ['yara', 'YARA'], ['deepseek', 'DeepSeek AI'],
      ['shuffle', 'Shuffle SOAR'], ['iris', 'IRIS'], ['telegram', 'Telegram'],
      ['wazuh', 'Wazuh'], ['siem', 'SIEM'], ['soc', 'SOC'],
    ];
    let tool = '';
    for (const [kw, label] of toolMap) {
      if (section.title.toLowerCase().includes(kw) || section.body.toLowerCase().includes(kw)) {
        tool = label;
        break;
      }
    }

    return {
      number: section.number,
      title: section.title,
      body: section.body || '',
      criticality,
      tool,
      images: section.images || [],
    };
  });
});

watch(caseHeroImageIndex, () => {
  caseHeroImageLoaded.value = false;
});

const activeCaseStudy = computed(() => {
  if (!caseStudyItem.value) return [];
  const c = caseStudyItem.value.content || {};
  const type = caseStudyItem.value.type;
  const sections = [];
  let num = 1;

  if (type !== 'parcours') {
    sections.push({
      number: String(num++).padStart(2, '0'),
      title: 'Présentation & Contexte',
      body: caseStudyItem.value.description,
    });
  }

  if (c.objective) {
    sections.push({
      number: String(num++).padStart(2, '0'),
      title: type === 'realisation' ? 'Objectif' : type === 'parcours' ? 'Objectifs de la formation' : 'Contexte & Utilisation',
      body: c.objective,
    });
  }

  const archImages = c.architecture_image ? [resolveAssetUrl(c.architecture_image)].filter(Boolean) : [];

  if (c.architecture) {
    sections.push({
      number: String(num++).padStart(2, '0'),
      title: type === 'realisation' ? 'Architecture / méthode' : type === 'parcours' ? 'Programme & apprentissages' : 'Détails techniques & Niveau',
      body: c.architecture,
      image: archImages[0] || '',
      images: archImages,
    });
  } else if (archImages.length) {
    sections.push({
      number: String(num++).padStart(2, '0'),
      title: 'Illustration / Document',
      body: '',
      image: archImages[0] || '',
      images: archImages,
    });
  }

  if (c.alert_flow && type !== 'parcours') {
    sections.push({
      number: String(num++).padStart(2, '0'),
      title: type === 'realisation' ? 'Flux d\'alerte' : type === 'parcours' ? 'Cadre de formation' : 'Cas d\'usage & Projets liés',
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
      title: type === 'realisation' ? 'Impact' : type === 'parcours' ? 'Résultat' : 'Certifications / Attestation',
      body: c.impact,
    });
  }

  if (sections.length === 1) {
    sections.push({
      number: String(num++).padStart(2, '0'),
      title: 'Détails complémentaires',
      body: 'Les informations détaillées seront ajoutées prochainement.',
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
  parcours: sortChronologically(visibleItems.value.filter((item) => normalizeType(item.type) === 'parcours')),
  competence: visibleItems.value.filter((item) => normalizeType(item.type) === 'competence'),
  realisation: visibleItems.value.filter((item) => normalizeType(item.type) === 'realisation'),
  blog: visibleItems.value.filter((item) => normalizeType(item.type) === 'blog'),
}));

const featuredProject = computed(() => items.value.find((item) => normalizeType(item.type) === 'realisation' && item.featured));

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
  document.addEventListener('keydown', handleGlobalKeydown);

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
  updateClock();
  loadVeille();
  clockTimer = window.setInterval(updateClock, 1000);
  veilleTimer = window.setInterval(loadVeille, 60000);
  window.addEventListener('scroll', handleScroll, { passive: true });
  window.addEventListener('pointermove', handlePointerMove, { passive: true });
});

onUnmounted(() => {
  if (rafId) cancelAnimationFrame(rafId);
  if (lenis) lenis.destroy();
  if (clockTimer) window.clearInterval(clockTimer);
  if (veilleTimer) window.clearInterval(veilleTimer);
  revealObserver?.disconnect();
  window.removeEventListener('scroll', updatePhotoParallax);
  window.removeEventListener('scroll', handleScroll);
  window.removeEventListener('pointermove', handlePointerMove);
  document.removeEventListener('keydown', handleGlobalKeydown);
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
    const rawItems = await getItems();
    items.value = (rawItems || []).map((item) => ({
      ...item,
      type: normalizeType(item.type),
    }));
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
  playClick();
  authState.loading = true;
  try {
    const data = await login(credentials.username, credentials.password);
    setToken(data.access_token);
    credentials.password = '';
    showLogin.value = false;
    notifySuccess('Connexion réussie');
    await loadItems();
  } catch (error) {
    notifyError(error.message);
  } finally {
    authState.loading = false;
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
  showLogin.value = true;
  notifyError('Session expirée. Veuillez vous reconnecter.');
}

function openCreate(type = 'parcours') {
  editing.value = { type, category: '', featured: false, title: '', subtitle: '', description: '' };
}

function openEdit(item) {
  editing.value = { ...item };
}

function openCaseStudy(item) {
  caseHeroImageFailed.value = false;
  caseHeroImageLoaded.value = false;
  activeCaseStepIndex.value = -1;
  caseStudyItem.value = item;
  caseProgress.value = 0;
  resetCaseImageIndexes();
  nextTick(updateCaseProgress);
}

function closeCaseStudy() {
  caseStudyItem.value = null;
  caseProgress.value = 0;
  caseHeroImageFailed.value = false;
  caseHeroImageLoaded.value = false;
  activeCaseStepIndex.value = -1;
  closeImageViewer();
  resetCaseImageIndexes();
}

function handleCaseHeroImageLoad(e) {
  const figure = e?.target?.closest?.('.case-hero-visual');
  if (figure) {
    figure.classList.add('is-loaded');
  }
  caseHeroImageLoaded.value = true;
}

function handleCaseHeroImageError(e) {
  caseHeroImageFailed.value = true;
  handleImgError(e);
}

function storyStyle(index) {
  return { '--story-delay': `${120 + Math.max(index, 0) * 140}ms` };
}

function markImageLoaded(e) {
  const figure = e?.target?.closest?.('.case-section-image-wrapper');
  if (figure) {
    figure.classList.add('is-loaded');
  }
}

function setupScrollReveal() {
  revealObserver?.disconnect();
  const revealTargets = document.querySelectorAll('.reveal-on-scroll');

  // Toujours afficher les éléments qui n'auraient pas été révélés après 1.5s (filet de sécurité)
  window.setTimeout(() => {
    document.querySelectorAll('.reveal-on-scroll:not(.is-visible)').forEach((el) => {
      el.classList.add('is-visible');
    });
  }, 1500);

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
    { threshold: 0.02, rootMargin: '0px 0px 60px 0px' },
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

  const steps = modal.querySelectorAll('.case-step');
  if (!steps.length) {
    activeCaseStepIndex.value = -1;
    return;
  }

  const marker = modal.getBoundingClientRect().top + modal.clientHeight * 0.42;
  let currentIndex = -1;

  steps.forEach((step, index) => {
    const rect = step.getBoundingClientRect();
    if (rect.top <= marker) {
      currentIndex = index;
    }
  });

  activeCaseStepIndex.value = currentIndex;
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
    notifySuccess('Élément enregistré avec succès');
    await loadItems();
  } catch (error) {
    if (error.status === 401 || error.status === 403) {
      clearToken();
      showLogin.value = true;
      notifyError('Session expirée. Veuillez vous reconnecter.');
    } else {
      notifyError(error.message);
    }
  }
}

async function remove(item) {
  if (!confirm(`Supprimer "${item.title}" du portfolio ?`)) return;
  try {
    await deleteItem(item.id, authState.token);
    notifySuccess('Élément supprimé');
    await loadItems();
  } catch (error) {
    if (error.status === 401 || error.status === 403) {
      clearToken();
      showLogin.value = true;
      notifyError('Session expirée. Veuillez vous reconnecter.');
    } else {
      notifyError(error.message);
    }
  }
}
async function handleDeleteTestimonial(t) {
  if (!confirm(`Supprimer le témoignage de "${t.client_name}" ?`)) return;
  try {
    await apiDeleteTestimonial(t.id, authState.token);
    notifySuccess('Témoignage supprimé');
    await loadItems();
  } catch (error) {
    notifyError(error.message);
  }
}

async function handleToggleTestimonialVisibility(t, is_visible) {
  try {
    await updateTestimonial(t.id, is_visible, authState.token);
    notifySuccess('Visibilité mise à jour');
    await loadItems();
  } catch (error) {
    notifyError(error.message);
  }
}

function closeTestimonialModal() {
  showTestimonialForm.value = false;
  setTimeout(() => {
    showTestimonialSuccess.value = false;
    testimonialDraft.client_name = '';
    testimonialDraft.client_company = '';
    testimonialDraft.linkedin_url = '';
    testimonialDraft.content = '';
  }, 300);
}

async function handleCreateTestimonial() {
  playClick();
  testimonialStatus.value = 'sending';
  try {
    await createTestimonial(testimonialDraft);
    testimonialStatus.value = '';
    showTestimonialSuccess.value = true;
    notifySuccess('Témoignage envoyé avec succès !');
    await loadItems();
  } catch (error) {
    testimonialStatus.value = '';
    notifyError("Oups, impossible d'envoyer le témoignage. Veuillez vérifier votre connexion et réessayer.");
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
  playClick();
  contactStatus.value = 'sending';
  try {
    await sendContactMessage(contactDraft.email, contactDraft.subject, contactDraft.message);
    contactStatus.value = '';
    contactDraft.email = '';
    contactDraft.subject = '';
    contactDraft.message = '';
    notifySuccess('Votre message a bien été envoyé !');
  } catch (error) {
    contactStatus.value = '';
    notifyError("Oups, notre serveur semble faire une pause. Veuillez vérifier votre connexion et réessayer.");
  }
}
</script>

<style scoped>

.case-section-gallery {
  display: grid;
  gap: 0.9rem;
  margin-top: 1.5rem;
}

.case-gallery-card {
  position: relative;
}

.case-section-image-wrapper {
  position: relative;
  margin-top: 0;
  border-radius: var(--radius-lg);
  overflow: hidden;
  border: 1px solid rgba(119, 33, 111, 0.12);
  background: #ffffff;
  box-shadow: 0 14px 28px rgba(44, 0, 30, 0.08);
}

.case-section-image-wrapper--interactive {
  cursor: zoom-in;
  transition: transform 220ms ease, box-shadow 220ms ease, border-color 220ms ease;
}

.case-section-image-wrapper--interactive:hover {
  transform: translateY(-2px);
  border-color: rgba(233, 84, 32, 0.25);
  box-shadow: 0 18px 36px rgba(44, 0, 30, 0.12);
}

.case-section-image-wrapper img {
  width: 100%;
  height: auto;
  display: block;
}

.case-section-image-wrapper .case-gallery-hint,
.case-gallery-caption {
  position: absolute;
  left: 14px;
  bottom: 14px;
  padding: 7px 12px;
  border-radius: 999px;
  background: rgba(37, 12, 34, 0.72);
  color: #fff;
  font-size: 0.78rem;
  letter-spacing: 0.02em;
  backdrop-filter: blur(10px);
}

.case-gallery-thumbs {
  display: flex;
  gap: 0.6rem;
  flex-wrap: wrap;
}

.case-gallery-thumb {
  width: 72px;
  height: 54px;
  padding: 0;
  border: 2px solid transparent;
  border-radius: 14px;
  overflow: hidden;
  background: rgba(255,255,255,0.9);
  box-shadow: 0 6px 14px rgba(44, 0, 30, 0.08);
  cursor: pointer;
  transition: transform 180ms ease, border-color 180ms ease, box-shadow 180ms ease;
}

.case-gallery-thumb:hover {
  transform: translateY(-2px);
}

.case-gallery-thumb.active {
  border-color: var(--ubuntu-orange);
  box-shadow: 0 10px 20px rgba(233, 84, 32, 0.16);
}

.case-gallery-thumb img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.case-gallery-nav {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  width: 38px;
  height: 38px;
  border: none;
  border-radius: 50%;
  background: rgba(255,255,255,0.9);
  color: var(--aubergine-dark);
  box-shadow: 0 10px 24px rgba(44, 0, 30, 0.16);
  display: grid;
  place-items: center;
  cursor: pointer;
  z-index: 2;
}

.case-gallery-nav:hover {
  background: #fff;
}

.case-gallery-nav:disabled {
  opacity: 0.35;
  cursor: default;
}

.case-gallery-nav--prev { left: 12px; }
.case-gallery-nav--next { right: 12px; }

.image-viewer-backdrop {
  position: fixed;
  inset: 0;
  z-index: 2500;
  display: grid;
  place-items: center;
  padding: 18px;
  background: rgba(31, 14, 27, 0.78);
  backdrop-filter: blur(18px);
}

.image-viewer {
  width: min(1120px, 100%);
  max-height: min(92vh, 980px);
  display: grid;
  grid-template-rows: auto 1fr auto;
  gap: 18px;
  padding: 18px;
  border-radius: 28px;
  background: #ffffff;
  box-shadow: 0 30px 80px rgba(0, 0, 0, 0.35);
}

.image-viewer-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
}

.image-viewer-kicker {
  display: block;
  margin-bottom: 4px;
  color: var(--ubuntu-orange-dark);
  font-size: 0.78rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.12em;
}

.image-viewer-header strong {
  color: var(--aubergine-dark);
  font-size: 1.1rem;
}

.image-viewer-close {
  width: 44px;
  height: 44px;
  border: none;
  border-radius: 50%;
  background: rgba(119, 33, 111, 0.08);
  color: var(--aubergine-dark);
  cursor: pointer;
  display: grid;
  place-items: center;
}

.image-viewer-body {
  display: grid;
  grid-template-columns: auto minmax(0, 1fr) auto;
  gap: 16px;
  align-items: center;
}

.image-viewer-nav {
  width: 48px;
  height: 48px;
  border: none;
  border-radius: 50%;
  background: rgba(119, 33, 111, 0.08);
  color: var(--aubergine-dark);
  cursor: pointer;
  display: grid;
  place-items: center;
  box-shadow: 0 10px 24px rgba(44, 0, 30, 0.12);
}

.image-viewer-figure {
  margin: 0;
  display: grid;
  gap: 12px;
  justify-items: center;
}

.image-viewer-figure img {
  max-width: 100%;
  max-height: calc(92vh - 220px);
  object-fit: contain;
  border-radius: 20px;
  background: rgba(255,255,255,0.94);
  box-shadow: 0 18px 40px rgba(44, 0, 30, 0.16);
  cursor: zoom-out;
}

.image-viewer-figure figcaption {
  color: var(--muted);
  font-size: 0.92rem;
}

.image-viewer-thumbs {
  display: flex;
  gap: 0.75rem;
  overflow-x: auto;
  padding-bottom: 2px;
}

.image-viewer-thumb {
  width: 88px;
  height: 62px;
  padding: 0;
  border: 2px solid transparent;
  border-radius: 14px;
  overflow: hidden;
  background: rgba(255,255,255,0.92);
  cursor: pointer;
  flex: 0 0 auto;
}

.image-viewer-thumb.active {
  border-color: var(--ubuntu-orange);
}

.image-viewer-thumb img {
  width: 100%;
  height: 100%;
  object-fit: cover;
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
  background: rgba(255, 255, 255, 0.12);
  border: 1px solid rgba(255, 255, 255, 0.26);
  color: #fff;
  padding: 0.4rem 0.8rem;
  border-radius: 20px;
  font-size: 0.85rem;
  cursor: pointer;
  transition: background 0.2s, color 0.2s;
}

.chip-button:hover {
  background: var(--ubuntu-orange);
  border-color: var(--ubuntu-orange);
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
  .form-row {
    flex-direction: column;
    align-items: flex-start;
    padding: 1rem 0;
    gap: 0.5rem;
  }
  .row-label {
    width: 100%;
    font-size: 0.95rem;
  }
  .row-input, .row-static-text {
    width: 100%;
    font-size: 1rem;
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

