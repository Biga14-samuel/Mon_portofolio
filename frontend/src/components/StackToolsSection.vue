<template>
  <section class="stack-section blueprint-bg" :id="id" :aria-labelledby="`${id}-title`">
    <div class="stack-heading">
      <div>
        <PillBadge tone="aubergine">Stack configurable</PillBadge>
        <h2 :id="`${id}-title`">
          <span>Stack</span>
          <span class="animated-word">& outils</span>
        </h2>
      </div>
      <p v-if="editable">
        Les domaines ci-dessous sont alimentés par les compétences ajoutées en mode administration.
      </p>
    </div>

    <div v-if="stackGroups.length" class="stack-board">
      <article v-for="group in stackGroups" :key="group.category" class="stack-column" :class="tagTone(group.category)">
        <div class="stack-column__head">
          <PillBadge :tone="tagTone(group.category)">{{ group.category }}</PillBadge>
          <span>{{ group.items.length }} élément{{ group.items.length > 1 ? 's' : '' }}</span>
        </div>

        <div class="bento-grid">
          <article v-for="(item, index) in group.items" :key="item.id" class="bento-card stack-tool" :class="getRandomBentoSize(index)">
            <div>
              <h3>{{ item.title }}</h3>
              <small>{{ item.subtitle }}</small>
              <p>{{ item.description }}</p>
              <button class="case-link" type="button" style="margin-top: 0.5rem;" @click="$emit('view-case', item)">
                Voir le détail
              </button>
            </div>
            <div v-if="editable" class="card-actions stack-actions" aria-label="Actions administrateur">
              <button class="icon-button" type="button" :aria-label="`Modifier ${item.title}`" @click="$emit('edit', item)">
                <Pencil :size="18" aria-hidden="true" />
              </button>
              <button class="icon-button danger" type="button" :aria-label="`Supprimer ${item.title}`" @click="$emit('delete', item)">
                <Trash2 :size="18" aria-hidden="true" />
              </button>
            </div>
          </article>
        </div>
      </article>
    </div>

    <p v-else class="empty-state">{{ empty }}</p>
  </section>
</template>

<script setup>
import { computed } from 'vue';
import { Pencil, Trash2 } from 'lucide-vue-next';
import PillBadge from './PillBadge.vue';
import { tagTone } from '../services/tags';

const props = defineProps({
  id: { type: String, required: true },
  items: { type: Array, required: true },
  empty: { type: String, required: true },
  editable: { type: Boolean, default: false },
});

defineEmits(['edit', 'delete', 'view-case']);

const categoryOrder = [
  'Détection',
  'Threat Intel',
  'Incident Response',
  'Sécurité / Cybersécurité',
  'Administration réseau',
  'Réseau',
  'Administration système',
  'Systèmes',
  'Dev / Scripting',
  'Programmation web',
  'DB',
  'Base de données',
  'Cloud / Virtualisation',
  'Méthodologie / Gestion de projet',
];

const stackGroups = computed(() => {
  const byCategory = props.items.reduce((groups, item) => {
    const category = item.category || 'Autres';
    groups[category] = [...(groups[category] || []), item];
    return groups;
  }, {});

  return Object.entries(byCategory)
    .map(([category, items]) => ({
      category,
      items: [...items].sort((a, b) => a.title.localeCompare(b.title)),
      order: categoryOrder.indexOf(category),
    }))
    .sort((a, b) => {
      const orderA = a.order === -1 ? Number.MAX_SAFE_INTEGER : a.order;
      const orderB = b.order === -1 ? Number.MAX_SAFE_INTEGER : b.order;
      return orderA - orderB || a.category.localeCompare(b.category);
    });
});

const getRandomBentoSize = (index) => {
  if (index % 5 === 0) return 'span-2 col-span-2 row-span-2';
  if (index % 3 === 0) return 'span-wide col-span-2 row-span-1';
  return 'span-1 col-span-1 row-span-1';
};
</script>
