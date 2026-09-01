<template>
  <section id="temoignages" class="content-section testimonials-section" aria-labelledby="testimonials-title">
    <div class="section-heading">
      <h2 id="testimonials-title">Selon leurs propres mots</h2>
    </div>

    <div v-if="loading" class="carousel-container">
      <div class="testimonials-carousel" aria-label="Chargement des témoignages...">
        <div v-for="n in 3" :key="n" class="skeleton-card" style="flex: 0 0 calc(100% - 3rem); max-width: 400px; min-width: 300px;">
          <div class="skeleton-text long"></div>
          <div class="skeleton-text long"></div>
          <div class="skeleton-text short"></div>
          <div style="margin-top: auto; display: flex; align-items: center; justify-content: space-between;">
            <div class="skeleton-title" style="width: 50%;"></div>
            <div class="skeleton-img" style="width: 36px; height: 36px; border-radius: 50%;"></div>
          </div>
        </div>
      </div>
    </div>

    <div v-else-if="testimonials.length === 0 && !editable" class="empty-state-card" style="margin: 0 2rem;">
      <MessageSquarePlus class="empty-icon" :size="48" />
      <p>Aucun témoignage pour le moment.<br>Soyez le premier à partager votre expérience !</p>
    </div>

    <div v-else class="carousel-container" :class="{ 'is-marquee': shouldMarquee }">
      <!-- Masques en dégradé sur les bords pour transition douce -->
      <div v-if="shouldMarquee" class="marquee-edge marquee-edge--left" aria-hidden="true"></div>
      <div v-if="shouldMarquee" class="marquee-edge marquee-edge--right" aria-hidden="true"></div>

      <div 
        class="testimonials-carousel" 
        :class="{ 'marquee-track': shouldMarquee }"
        :style="shouldMarquee ? { animationDuration: `${marqueeDuration}s` } : {}"
      >
        <article 
          v-for="(t, index) in displayTestimonials" 
          :key="`${t.id}-${index}`" 
          class="testimonial-card" 
          :class="{ 'not-visible': editable && !t.is_visible }"
        >
          <div class="testimonial-content">
            <p>« {{ t.content }} »</p>
          </div>
          <div class="testimonial-author">
            <div class="author-info">
              <div class="author-header">
                <strong class="author-name">{{ t.client_name }}</strong>
                <a v-if="t.linkedin_url" :href="t.linkedin_url" target="_blank" rel="noreferrer" title="Profil LinkedIn" class="linkedin-link">
                  in
                </a>
              </div>
              <span v-if="t.client_company" class="author-role">{{ t.client_company }}</span>
            </div>
          </div>

          <div v-if="editable" class="card-actions admin-controls">
            <label class="toggle-label">
              <input 
                type="checkbox" 
                :checked="t.is_visible" 
                @change="$emit('toggle-visibility', t, $event.target.checked)"
              />
              Public
            </label>
            <button class="icon-button danger" type="button" aria-label="Supprimer" @click="$emit('delete', t)">
              <Trash2 :size="18" aria-hidden="true" />
            </button>
          </div>
        </article>
      </div>
      
    </div>

    <div class="testimonials-actions" style="margin-top: 2rem; text-align: center;">
      <button class="button primary" @click="$emit('add-testimonial')">Laisser un témoignage</button>
    </div>
  </section>
</template>

<script setup>
import { computed } from 'vue';
import { Trash2, MessageSquarePlus } from 'lucide-vue-next';

const props = defineProps({
  testimonials: {
    type: Array,
    required: true
  },
  editable: {
    type: Boolean,
    default: false
  },
  loading: {
    type: Boolean,
    default: false
  }
});

defineEmits(['toggle-visibility', 'delete', 'add-testimonial']);

// Activer le défilement automatique si on a au moins 3 témoignages et qu'on n'est pas en mode édition admin
const shouldMarquee = computed(() => {
  return props.testimonials.length >= 3 && !props.editable;
});

// Dupliquer les cartes pour un défilement infini fluide
const displayTestimonials = computed(() => {
  if (shouldMarquee.value) {
    return [...props.testimonials, ...props.testimonials];
  }
  return props.testimonials;
});

// Vitesse dynamique selon le nombre de témoignages (environ 8s par carte pour une lecture confortable)
const marqueeDuration = computed(() => {
  return Math.max(25, props.testimonials.length * 9);
});
</script>

<style scoped>
.testimonials-section {
  position: relative;
  overflow: hidden;
}

.carousel-container {
  position: relative;
  max-width: 100%;
  margin: 0 auto;
  overflow: hidden;
}

.testimonials-carousel {
  display: flex;
  gap: 1.5rem;
  overflow-x: auto;
  padding: 1rem 1.5rem 2rem 1.5rem;
  scroll-snap-type: x mandatory;
  scrollbar-width: none; /* Firefox */
  -ms-overflow-style: none; /* IE/Edge */
}
.testimonials-carousel::-webkit-scrollbar {
  display: none; /* Chrome/Safari */
}

/* ── Animation de défilement continu de droite à gauche ── */
@keyframes marqueeRightToLeft {
  0% {
    transform: translate3d(0, 0, 0);
  }
  100% {
    transform: translate3d(-50%, 0, 0);
  }
}

.is-marquee .testimonials-carousel.marquee-track {
  display: flex;
  width: max-content;
  overflow: visible;
  scroll-snap-type: none;
  animation-name: marqueeRightToLeft;
  animation-timing-function: linear;
  animation-iteration-count: infinite;
  will-change: transform;
}

/* ── Pause automatique au survol (souris) ou au clic/focus ── */
.is-marquee:hover .testimonials-carousel.marquee-track,
.is-marquee .testimonials-carousel.marquee-track:hover,
.is-marquee .testimonials-carousel.marquee-track:focus-within {
  animation-play-state: paused;
}

/* ── Masques transparents sur les bords ── */
.marquee-edge {
  position: absolute;
  top: 0;
  bottom: 0;
  width: clamp(24px, 5vw, 80px);
  z-index: 5;
  pointer-events: none;
}

.marquee-edge--left {
  left: 0;
  background: linear-gradient(to right, var(--surface, #fcfbfb), transparent);
}

.marquee-edge--right {
  right: 0;
  background: linear-gradient(to left, var(--surface, #fcfbfb), transparent);
}

.testimonial-card {
  flex: 0 0 340px;
  max-width: 400px;
  min-width: 300px;
  scroll-snap-align: start;
  background: var(--surface-card);
  border-radius: 1.5rem;
  padding: 2.5rem 2rem;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  gap: 2rem;
  color: var(--text);
  transition: transform 0.25s ease, box-shadow 0.25s ease;
  border: 1px solid var(--outline);
  box-shadow: var(--shadow);
  user-select: text;
}

@media (min-width: 768px) {
  .testimonial-card {
    flex: 0 0 380px;
  }
}

.testimonial-card:hover {
  transform: translateY(-5px);
  box-shadow: var(--shadow-lift);
}

.testimonial-card.not-visible {
  opacity: 0.6;
  border-style: dashed;
}

.testimonial-content {
  flex-grow: 1;
}

.testimonial-content p {
  font-size: 1.05rem;
  line-height: 1.6;
  font-weight: 400;
  color: var(--muted);
  margin: 0;
}

.testimonial-author {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: auto;
}

.author-info {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 0.2rem;
}

.author-header {
  display: flex;
  align-items: center;
  gap: 0.45rem;
}

.author-name {
  font-size: 1.05rem;
  font-weight: 700;
  color: var(--aubergine-dark);
}

.author-role {
  font-size: 0.88rem;
  font-weight: 500;
  color: var(--muted);
  line-height: 1.35;
}

.linkedin-link {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
  background: #0a66c2;
  color: white;
  border-radius: 4px;
  text-decoration: none;
  font-size: 0.75rem;
  font-weight: bold;
  opacity: 0.85;
  transition: opacity 0.2s;
}

.linkedin-link:hover {
  opacity: 1;
}

.admin-controls {
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px dashed var(--outline);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.toggle-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.9rem;
  cursor: pointer;
  color: var(--muted);
}

@media (prefers-reduced-motion: reduce) {
  .is-marquee .testimonials-carousel.marquee-track {
    animation: none;
    overflow-x: auto;
  }
}
</style>
