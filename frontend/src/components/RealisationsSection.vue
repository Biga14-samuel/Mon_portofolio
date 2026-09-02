<template>
  <section class="content-section" id="realisations" aria-labelledby="realisations-title">
    <!-- Heading -->
    <div class="section-heading">
      <h2 id="realisations-title">Mes réalisations</h2>
    </div>

    <!-- État de chargement (Skeleton style YouTube / Média) -->
    <div v-if="loading" class="cards-grid" aria-label="Chargement des réalisations...">
      <div v-for="n in 3" :key="n" class="skeleton-card" style="border-radius: 20px; overflow: hidden;">
        <!-- Miniature / Thumbnail -->
        <div class="skeleton-img skeleton-shimmer" style="height: 190px; width: 100%;"></div>
        <!-- Contenu -->
        <div class="skeleton-content" style="padding: 20px; gap: 14px;">
          <div style="display: flex; gap: 8px;">
            <div class="skeleton-pill skeleton-shimmer" style="width: 80px; height: 22px;"></div>
            <div class="skeleton-pill skeleton-shimmer" style="width: 60px; height: 22px;"></div>
          </div>
          <div class="skeleton-pill skeleton-shimmer" style="width: 75%; height: 22px;"></div>
          <div style="display: flex; flex-direction: column; gap: 8px;">
            <div class="skeleton-pill skeleton-shimmer" style="width: 100%; height: 14px;"></div>
            <div class="skeleton-pill skeleton-shimmer" style="width: 80%; height: 14px;"></div>
            <div class="skeleton-pill skeleton-shimmer" style="width: 50%; height: 14px;"></div>
          </div>
        </div>
      </div>
    </div>

    <!-- Grid -->
    <div v-else-if="items.length" class="cards-grid" aria-label="Grille des projets">
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
  loading:  { type: Boolean, default: false },
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
