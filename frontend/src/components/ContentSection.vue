<template>
  <section class="content-section" :id="id" :aria-labelledby="`${id}-title`">
    <div class="section-heading">
      <h2 :id="`${id}-title`">{{ title }}</h2>
    </div>

    <!-- État de chargement (Skeleton style moderne) -->
    <div v-if="loading" :class="layout === 'zig-zag' ? 'zig-zag-grid' : 'cards-grid'" aria-label="Chargement...">
      <div v-for="n in 3" :key="n" class="skeleton-card" style="padding: 24px; gap: 16px;">
        <div style="display: flex; gap: 14px; align-items: center;">
          <div class="skeleton-circle skeleton-shimmer" style="width: 44px; height: 44px;"></div>
          <div style="flex: 1; display: flex; flex-direction: column; gap: 8px;">
            <div class="skeleton-pill skeleton-shimmer" style="width: 50%; height: 18px;"></div>
            <div class="skeleton-pill skeleton-shimmer" style="width: 30%; height: 12px;"></div>
          </div>
        </div>
        <div style="display: flex; flex-direction: column; gap: 8px; margin-top: 4px;">
          <div class="skeleton-pill skeleton-shimmer" style="width: 100%; height: 14px;"></div>
          <div class="skeleton-pill skeleton-shimmer" style="width: 85%; height: 14px;"></div>
          <div class="skeleton-pill skeleton-shimmer" style="width: 55%; height: 14px;"></div>
        </div>
      </div>
    </div>

    <!-- Données chargées -->
    <div v-else-if="items.length" :class="layout === 'zig-zag' ? 'zig-zag-grid' : 'cards-grid'">
      <ItemCard
        v-for="item in items"
        :key="item.id"
        :item="item"
        :editable="editable"
        @edit="$emit('edit', $event)"
        @delete="$emit('delete', $event)"
        @view-case="$emit('view-case', $event)"
      />
    </div>

    <!-- État vide -->
    <div v-else class="empty-state-card">
      <SearchX class="empty-icon" :size="48" />
      <p>{{ empty || 'Aucun élément trouvé pour cette catégorie.' }}</p>
    </div>
  </section>
</template>

<script setup>
import { SearchX } from 'lucide-vue-next';
import ItemCard from './ItemCard.vue';

defineProps({
  id: { type: String, required: true },
  title: { type: String, required: true },
  items: { type: Array, required: true },
  empty: { type: String, required: true },
  loading: { type: Boolean, default: false },
  editable: { type: Boolean, default: false },
  layout: { type: String, default: 'grid' },
});

defineEmits(['edit', 'delete', 'view-case']);
</script>
