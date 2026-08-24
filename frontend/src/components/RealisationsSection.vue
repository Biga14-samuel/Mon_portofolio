<template>
  <section class="content-section" id="realisations" aria-labelledby="realisations-title">
    <!-- Heading -->
    <div class="section-heading">
      <h2 id="realisations-title">Mes réalisations</h2>
    </div>

    <!-- Grid -->
    <div v-if="items.length" class="cards-grid" aria-label="Grille des projets">
      <ProjectCard
        v-for="(item, idx) in items"
        :key="item.id"
        :item="item"
        :editable="editable"
        :card-size="cardSizeFor(idx)"
        class="realisations-grid__item"
        @edit="$emit('edit', $event)"
        @delete="$emit('delete', $event)"
        @view-case="$emit('view-case', $event)"
      />
    </div>

    <!-- Empty state -->
    <div v-else class="empty-state-card">
      <SearchX class="empty-icon" :size="48" />
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

function cardSizeFor(idx) {
  const item = props.items[idx];
  if (item?.featured) return 'large';
  const pattern = ['medium', 'small', 'medium', 'large', 'small', 'medium'];
  return pattern[idx % pattern.length];
}
</script>

<style scoped>
.realisations-grid__item {
  width: 100%;
}
</style>
