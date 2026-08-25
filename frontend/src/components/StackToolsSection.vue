<template>
  <section class="content-section stack-section blueprint-bg reveal-on-scroll" :id="id" :aria-labelledby="`${id}-title`">
    <div class="section-heading">
      <h2 :id="`${id}-title`">
        <span>Stack &amp; Outils</span>
      </h2>
      <p class="stack-intro">
        Technologies, environnements, protocoles et outils maîtrisés et validés en conditions réelles.
      </p>
    </div>

    <div v-if="stackGroups.length" class="stack-categories-container">
      <div 
        v-for="group in stackGroups" 
        :key="group.category" 
        class="stack-group-card glass-card"
      >
        <!-- En-tête de la catégorie -->
        <div class="stack-group-header">
          <div class="stack-group-title-area">
            <PillBadge :tone="tagTone(group.category)">{{ group.category }}</PillBadge>
          </div>
          <span class="stack-group-count">
            {{ group.items.length }} outil{{ group.items.length > 1 ? 's' : '' }}
          </span>
        </div>

        <!-- Grille fluide de cartes d'outils minimalistes et ultra lisibles -->
        <div class="stack-items-grid">
          <article 
            v-for="item in group.items" 
            :key="item.id" 
            class="stack-card"
          >
            <div class="stack-card-header">
              <h3 class="stack-card-title">{{ item.title }}</h3>
              <span v-if="item.subtitle" class="stack-card-subtitle">{{ item.subtitle }}</span>
            </div>

            <p class="stack-card-desc">{{ item.description }}</p>

            <!-- Outils / mots-clés associés si présents -->
            <div v-if="getToolsList(item).length" class="stack-card-tags">
              <span 
                v-for="tool in getToolsList(item)" 
                :key="tool" 
                class="stack-tool-chip"
              >
                {{ tool }}
              </span>
            </div>

            <!-- Bas de carte : Bouton détail & Actions admin -->
            <div class="stack-card-footer">
              <button 
                class="stack-detail-btn" 
                type="button" 
                @click="$emit('view-case', item)"
              >
                <span>Voir le détail</span>
                <ArrowUpRight :size="14" aria-hidden="true" />
              </button>

              <div v-if="editable" class="stack-admin-actions" aria-label="Actions administrateur">
                <button 
                  class="icon-button" 
                  type="button" 
                  :aria-label="`Modifier ${item.title}`" 
                  @click.stop="$emit('edit', item)"
                >
                  <Pencil :size="15" aria-hidden="true" />
                </button>
                <button 
                  class="icon-button danger" 
                  type="button" 
                  :aria-label="`Supprimer ${item.title}`" 
                  @click.stop="$emit('delete', item)"
                >
                  <Trash2 :size="15" aria-hidden="true" />
                </button>
              </div>
            </div>
          </article>
        </div>
      </div>
    </div>

    <p v-else class="empty-state">{{ empty }}</p>
  </section>
</template>

<script setup>
import { computed } from 'vue';
import { Pencil, Trash2, ArrowUpRight } from 'lucide-vue-next';
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

function getToolsList(item) {
  const raw = item?.content?.tools || '';
  if (!raw) return [];
  return raw
    .split(/[,;|]+/)
    .map((t) => t.trim())
    .filter(Boolean)
    .slice(0, 4);
}
</script>

<style scoped>
.stack-section.blueprint-bg {
  position: relative;
  width: min(1200px, calc(100% - 32px));
  margin: 0 auto 80px;
  padding: clamp(28px, 5vw, 44px);
  border-radius: 24px;
  background-color: var(--ubuntu-orange);
  background-image:
    linear-gradient(rgba(255, 255, 255, 0.16) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255, 255, 255, 0.16) 1px, transparent 1px);
  background-size: 28px 28px;
  border: 1px solid rgba(169, 46, 7, 0.35);
  box-shadow: 0 24px 52px rgba(169, 46, 7, 0.22);
}

.stack-section.blueprint-bg .section-heading h2 {
  color: #ffffff;
}

.stack-intro {
  margin: 0.5rem 0 2rem;
  color: rgba(255, 255, 255, 0.92);
  font-size: 1.05rem;
  line-height: 1.5;
  max-width: 720px;
}

.stack-categories-container {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.stack-group-card {
  padding: 1.75rem 2rem;
  border-radius: 1.25rem;
  background: rgba(255, 255, 255, 0.93);
  border: 1px solid rgba(255, 255, 255, 0.6);
  box-shadow: 0 8px 32px rgba(44, 0, 30, 0.14);
  backdrop-filter: blur(12px);
  transition: transform 0.25s ease, box-shadow 0.25s ease;
}

.stack-group-card:hover {
  box-shadow: 0 14px 40px rgba(44, 0, 30, 0.2);
  transform: translateY(-2px);
}

.stack-group-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  margin-bottom: 1.5rem;
  padding-bottom: 0.85rem;
  border-bottom: 1px solid rgba(119, 33, 111, 0.12);
}

.stack-group-title-area {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.stack-group-count {
  font-size: 0.88rem;
  font-weight: 700;
  color: var(--aubergine);
}

.stack-items-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(290px, 1fr));
  gap: 1.25rem;
}

.stack-card {
  background: #ffffff;
  border: 1px solid rgba(119, 33, 111, 0.14);
  border-radius: 1rem;
  padding: 1.35rem 1.4rem;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  gap: 1rem;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  transition: transform 0.22s ease, border-color 0.22s ease, box-shadow 0.22s ease;
}

.stack-card:hover {
  transform: translateY(-3px);
  border-color: var(--ubuntu-orange);
  box-shadow: 0 8px 24px rgba(233, 84, 32, 0.2);
}

.stack-card-header {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
}

.stack-card-title {
  margin: 0;
  font-size: 1.15rem;
  font-weight: 700;
  color: var(--aubergine-dark);
  line-height: 1.3;
}

.stack-card-subtitle {
  font-size: 0.88rem;
  font-weight: 600;
  color: var(--ubuntu-orange);
  line-height: 1.4;
}

.stack-card-desc {
  margin: 0;
  color: var(--muted);
  font-size: 0.94rem;
  line-height: 1.55;
  flex-grow: 1;
}

.stack-card-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.4rem;
}

.stack-tool-chip {
  padding: 0.2rem 0.55rem;
  border-radius: 6px;
  background: rgba(119, 33, 111, 0.08);
  border: 1px solid rgba(119, 33, 111, 0.15);
  font-size: 0.78rem;
  font-weight: 600;
  color: var(--aubergine);
}

.stack-card-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.75rem;
  margin-top: auto;
  padding-top: 0.6rem;
}

.stack-detail-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  background: transparent;
  border: none;
  color: var(--aubergine);
  font-size: 0.9rem;
  font-weight: 700;
  cursor: pointer;
  padding: 0.3rem 0;
  transition: color 0.2s ease, gap 0.2s ease;
}

.stack-detail-btn:hover {
  color: var(--ubuntu-orange);
  gap: 0.6rem;
}

.stack-admin-actions {
  display: flex;
  align-items: center;
  gap: 0.4rem;
}

@media (max-width: 768px) {
  .stack-group-card {
    padding: 1.25rem 1.2rem;
  }
  .stack-items-grid {
    grid-template-columns: 1fr;
  }
}
</style>
