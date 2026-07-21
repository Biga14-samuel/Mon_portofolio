<template>
  <article class="item-card" :class="item.type">
    <div class="item-card__meta">
      <PillBadge :tone="item.type === 'realisation' ? 'orange' : 'aubergine'">{{ labels[item.type] }}</PillBadge>
      <PillBadge :tone="tagTone(item.category)">{{ item.category }}</PillBadge>
      <span>{{ item.subtitle }}</span>
    </div>
    <h3>{{ item.title }}</h3>
    <p>{{ item.description }}</p>
    <button v-if="item.type === 'realisation'" class="case-link" type="button" @click="$emit('view-case', item)">
      Voir l'étude de cas
    </button>
    <div v-if="editable" class="card-actions" aria-label="Actions administrateur">
      <button class="icon-button" type="button" :aria-label="`Modifier ${item.title}`" @click="$emit('edit', item)">
        <Pencil :size="18" aria-hidden="true" />
      </button>
      <button class="icon-button danger" type="button" :aria-label="`Supprimer ${item.title}`" @click="$emit('delete', item)">
        <Trash2 :size="18" aria-hidden="true" />
      </button>
    </div>
  </article>
</template>

<script setup>
import { Pencil, Trash2 } from 'lucide-vue-next';
import PillBadge from './PillBadge.vue';
import { tagTone } from '../services/tags';

defineProps({
  item: {
    type: Object,
    required: true,
  },
  editable: {
    type: Boolean,
    default: false,
  },
});

defineEmits(['edit', 'delete', 'view-case']);

const labels = {
  parcours: 'Parcours',
  competence: 'Competence',
  realisation: 'Realisation',
};
</script>
