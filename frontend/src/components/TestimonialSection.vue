<template>
  <section id="temoignages" class="testimonials-section reveal-on-scroll" aria-labelledby="testimonials-title">
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

    <div v-else class="carousel-container">
      <div class="testimonials-carousel">
        <article v-for="t in testimonials" :key="t.id" class="testimonial-card" :class="{ 'not-visible': editable && !t.is_visible }">
          <div class="testimonial-content">
            <p>« {{ t.content }} »</p>
          </div>
          <div class="testimonial-author">
            <div class="author-info">
              <span v-if="t.client_company">{{ t.client_company }}</span>
              <strong v-else>{{ t.client_name }}</strong>
              <a v-if="t.linkedin_url" :href="t.linkedin_url" target="_blank" rel="noreferrer" title="Profil LinkedIn" class="linkedin-link">
                in
              </a>
            </div>
            <div class="author-avatar" :title="t.client_name">
              {{ t.client_name.charAt(0) }}
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
import { Trash2, MessageSquarePlus } from 'lucide-vue-next';

defineProps({
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
</script>

<style scoped>
.testimonials-section {
  margin: 6rem 0;
  position: relative;
  overflow: hidden;
}

.section-heading {
  max-width: 1200px;
  margin: 0 auto 2rem auto;
  padding: 0 1.5rem;
}

.carousel-container {
  position: relative;
  max-width: 1200px;
  margin: 0 auto;
}

.testimonials-carousel {
  display: flex;
  gap: 1.5rem;
  overflow-x: auto;
  padding: 0 1.5rem 2rem 1.5rem;
  scroll-snap-type: x mandatory;
  scrollbar-width: none; /* Firefox */
  -ms-overflow-style: none; /* IE/Edge */
}
.testimonials-carousel::-webkit-scrollbar {
  display: none; /* Chrome/Safari */
}

.testimonial-card {
  flex: 0 0 calc(100% - 3rem);
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
  transition: transform 0.2s, box-shadow 0.2s;
  border: 1px solid var(--outline);
  box-shadow: var(--shadow);
}

@media (min-width: 768px) {
  .testimonial-card {
    flex: 0 0 400px;
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
  align-items: center;
  gap: 0.5rem;
}

.author-info span {
  font-size: 1.1rem;
  font-weight: 500;
  color: var(--muted);
}

.author-info strong {
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--aubergine-dark);
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

.author-avatar {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  background: rgba(233, 84, 32, 0.13);
  color: #a92e07;
  border-radius: 50%;
  font-size: 1rem;
  font-weight: 700;
  text-transform: uppercase;
}

.carousel-fade {
  position: absolute;
  top: 0;
  right: 0;
  bottom: 0;
  width: 150px;
  background: rgba(255, 255, 255, 0.95);
  pointer-events: none;
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
</style>
