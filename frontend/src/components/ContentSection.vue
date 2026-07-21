<template>
  <section class="content-section" :id="id" :aria-labelledby="`${id}-title`">
    <div class="section-heading">
      <h2 :id="`${id}-title`">{{ title }}</h2>
    </div>
    <div v-if="items.length" class="cards-grid">
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
    <p v-else class="empty-state">{{ empty }}</p>
  </section>
</template>

<script setup>
import ItemCard from './ItemCard.vue';

defineProps({
  id: { type: String, required: true },
  title: { type: String, required: true },
  items: { type: Array, required: true },
  empty: { type: String, required: true },
  editable: { type: Boolean, default: false },
});

defineEmits(['edit', 'delete', 'view-case']);
</script>
