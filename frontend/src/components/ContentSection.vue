<template>
  <section class="content-section" :id="id" :aria-labelledby="`${id}-title`">
    <div class="section-heading">
      <h2 :id="`${id}-title`">{{ title }}</h2>
    </div>

    <!-- État de chargement (Skeleton) -->
    <div v-if="loading" :class="layout === 'zig-zag' ? 'zig-zag-grid' : 'cards-grid'">
      <div v-for="n in 3" :key="n" class="skeleton-card" style="min-height: 170px; padding: 20px;">
        <div class="skeleton-title" style="width: 45%; height: 22px; margin-bottom: 12px;"></div>
        <div class="skeleton-text" style="width: 90%; margin-bottom: 8px;"></div>
        <div class="skeleton-text short" style="width: 60%;"></div>
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
