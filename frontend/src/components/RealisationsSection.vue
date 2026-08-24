<template>
  <section class="realisations-section" id="realisations" aria-labelledby="realisations-title">
    <!-- Heading -->
    <div class="realisations-section__heading">
      <span class="realisations-section__kicker">Portfolio</span>
      <h2 id="realisations-title" class="realisations-section__title">Mes réalisations</h2>
      <p class="realisations-section__subtitle">
        Projets techniques réalisés en réseau, sécurité, systèmes et SOC.
      </p>
    </div>

    <!-- Masonry grid -->
    <div v-if="items.length" class="realisations-masonry" aria-label="Grille des projets">
      <ProjectCard
        v-for="(item, idx) in items"
        :key="item.id"
        :item="item"
        :editable="editable"
        :card-size="cardSizeFor(idx)"
        class="realisations-masonry__item"
        @edit="$emit('edit', $event)"
        @delete="$emit('delete', $event)"
        @view-case="$emit('view-case', $event)"
      />
    </div>

    <!-- Empty state -->
    <div v-else class="realisations-empty">
      <div class="realisations-empty__icon">
        <SearchX :size="40" />
      </div>
      <p>Aucune réalisation publiée pour le moment.</p>
      <button
        v-if="editable"
        class="button primary"
        type="button"
        @click="$emit('add')"
      >
        Ajouter un projet
      </button>
    </div>
  </section>
</template>

<script setup>
import { SearchX } from 'lucide-vue-next';
import ProjectCard from './ProjectCard.vue';

const props = defineProps({
  items:    { type: Array,   required: true },
  editable: { type: Boolean, default: false },
});

defineEmits(['edit', 'delete', 'view-case', 'add']);

/**
 * Distribue les tailles de cartes pour créer un rythme masonry asymétrique :
 * - Projet vedette (featured) → toujours large
 * - Pattern cyclique : large, medium, small, medium, medium, small...
 */
function cardSizeFor(idx) {
  const item = props.items[idx];
  if (item?.featured) return 'large';
  const pattern = ['medium', 'small', 'medium', 'large', 'small', 'medium'];
  return pattern[idx % pattern.length];
}
</script>

<style scoped>
.realisations-section {
  padding: 5rem 0 3rem;
}

/* Heading */
.realisations-section__heading {
  text-align: center;
  margin-bottom: 3.5rem;
}

.realisations-section__kicker {
  display: inline-block;
  padding: 4px 14px;
  border-radius: 999px;
  background: rgba(233, 84, 32, 0.1);
  color: var(--ubuntu-orange-dark);
  font-size: 0.75rem;
  font-weight: 800;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  margin-bottom: 12px;
}

.realisations-section__title {
  font-size: clamp(1.8rem, 4vw, 2.6rem);
  font-weight: 800;
  margin: 0 0 10px;
  color: var(--text);
  letter-spacing: -0.025em;
  line-height: 1.15;
}

.realisations-section__subtitle {
  color: var(--muted);
  font-size: 1rem;
  margin: 0;
}

/* Masonry grid using CSS columns */
.realisations-masonry {
  columns: 3 320px;
  column-gap: 1.5rem;
}

.realisations-masonry__item {
  display: inline-block;
  width: 100%;
  margin-bottom: 1.5rem;
  vertical-align: top;
}

/* Force large cards to break across columns (span full width on 2-col) */
@media (min-width: 960px) {
  .realisations-masonry {
    columns: 3 280px;
  }
}

@media (max-width: 768px) {
  .realisations-masonry {
    columns: 1;
  }
}

/* Empty state */
.realisations-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
  padding: 4rem 2rem;
  text-align: center;
  color: var(--muted);
  background: var(--surface-soft);
  border-radius: 20px;
  border: 1px dashed var(--outline);
}

.realisations-empty__icon {
  width: 72px;
  height: 72px;
  border-radius: 50%;
  background: var(--surface-card);
  display: grid;
  place-items: center;
  color: var(--outline);
  box-shadow: var(--shadow);
}
</style>
