<template>
  <section class="content-section stack-section blueprint-bg reveal-on-scroll" :id="id" :aria-labelledby="`${id}-title`">
    <!-- Header & Titre -->
    <div class="stack-heading">
      <div>
        <span class="stack-badge">
          <Terminal :size="14" aria-hidden="true" />
          Console Technique &amp; Compétences
        </span>
        <h2 :id="`${id}-title`">
          <span>Stack &amp; Outils</span>
        </h2>
      </div>
      <p class="stack-intro">
        Explorez les technologies, environnements, protocoles et frameworks de sécurité maîtrisés et validés en conditions opérationnelles.
      </p>
    </div>

    <!-- Barre de contrôle interactive : Onglets de pôles + Recherche rapide -->
    <div class="stack-control-panel">
      <!-- Pôles / Domaines interactifs -->
      <div class="stack-domain-tabs" role="tablist" aria-label="Pôles d'expertise">
        <button
          class="stack-domain-tab"
          :class="{ 'is-active': activeDomain === 'all' }"
          type="button"
          role="tab"
          :aria-selected="activeDomain === 'all'"
          @click="activeDomain = 'all'"
        >
          <Layers :size="16" aria-hidden="true" />
          <span>Tous les pôles</span>
          <span class="tab-badge">{{ items.length }}</span>
        </button>

        <button
          v-for="group in stackGroups"
          :key="group.category"
          class="stack-domain-tab"
          :class="{ 'is-active': activeDomain === group.category }"
          type="button"
          role="tab"
          :aria-selected="activeDomain === group.category"
          @click="activeDomain = group.category"
        >
          <component :is="getCategoryIconComponent(group.category)" :size="16" aria-hidden="true" />
          <span>{{ formatCategoryName(group.category) }}</span>
          <span class="tab-badge">{{ group.items.length }}</span>
        </button>
      </div>

      <!-- Barre de recherche instantanée -->
      <div class="stack-search-bar">
        <Search :size="16" class="search-icon" aria-hidden="true" />
        <input
          v-model.trim="searchQuery"
          type="text"
          placeholder="Filtrer un outil, protocole, commande (ex: Wazuh, Python, Sysmon, Suricata)..."
          aria-label="Recherche d'outils"
        />
        <button 
          v-if="searchQuery" 
          type="button" 
          class="clear-search-btn" 
          @click="searchQuery = ''"
          aria-label="Effacer la recherche"
        >
          <X :size="14" />
        </button>
      </div>
    </div>

    <!-- Contenu dynamique filtré -->
    <div v-if="filteredGroups.length" class="stack-active-container">
      <TransitionGroup name="stack-fade" tag="div" class="stack-display-wrapper">
        <div 
          v-for="group in filteredGroups" 
          :key="group.category" 
          class="stack-group-block"
        >
          <!-- En-tête du pôle -->
          <div class="stack-domain-banner">
            <div class="domain-banner-left">
              <PillBadge :tone="tagTone(group.category)">{{ group.category }}</PillBadge>
              <span class="domain-banner-subtitle">{{ group.items.length }} outil{{ group.items.length > 1 ? 's' : '' }} référencé{{ group.items.length > 1 ? 's' : '' }}</span>
            </div>
            <span class="domain-status-tag">
              <ShieldCheck :size="14" /> Validé en Lab &amp; Terrain
            </span>
          </div>

          <!-- Grille de cartes d'outils interactive -->
          <div class="stack-cards-grid">
            <article 
              v-for="item in group.items" 
              :key="item.id" 
              class="stack-live-card"
            >
              <!-- En-tête de carte -->
              <div class="live-card-top">
                <div class="live-card-title-group">
                  <h3 class="live-card-title">{{ item.title }}</h3>
                  <span v-if="item.subtitle" class="live-card-subtitle">{{ item.subtitle }}</span>
                </div>
                <div class="live-card-indicator" title="Compétence opérationnelle validée">
                  <span class="pulse-dot"></span>
                </div>
              </div>

              <!-- Description -->
              <p class="live-card-desc">{{ item.description }}</p>

              <!-- Tags / Outils liés -->
              <div v-if="getToolsList(item).length" class="live-card-tags">
                <span 
                  v-for="tool in getToolsList(item)" 
                  :key="tool" 
                  class="live-tag-chip"
                >
                  {{ tool }}
                </span>
              </div>

              <!-- Pied de carte -->
              <div class="live-card-bottom">
                <button 
                  class="live-detail-link" 
                  type="button" 
                  @click="$emit('view-case', item)"
                >
                  <span>Fiche détaillée</span>
                  <ArrowUpRight :size="15" aria-hidden="true" />
                </button>

                <div v-if="editable" class="live-admin-actions" aria-label="Actions administrateur">
                  <button 
                    class="icon-button" 
                    type="button" 
                    :aria-label="`Modifier ${item.title}`" 
                    @click.stop="$emit('edit', item)"
                  >
                    <Pencil :size="14" aria-hidden="true" />
                  </button>
                  <button 
                    class="icon-button danger" 
                    type="button" 
                    :aria-label="`Supprimer ${item.title}`" 
                    @click.stop="$emit('delete', item)"
                  >
                    <Trash2 :size="14" aria-hidden="true" />
                  </button>
                </div>
              </div>
            </article>
          </div>
        </div>
      </TransitionGroup>
    </div>

    <!-- État vide si recherche sans résultat -->
    <div v-else class="stack-no-results glass-card">
      <Search :size="32" class="empty-search-icon" />
      <h3>Aucun outil trouvé pour "{{ searchQuery }}"</h3>
      <p>Essayez un autre mot-clé (ex: Linux, Wazuh, Python, Docker, Nmap, Suricata) ou réinitialisez la recherche.</p>
      <button type="button" class="button secondary" @click="searchQuery = ''; activeDomain = 'all'">
        Réinitialiser les filtres
      </button>
    </div>
  </section>
</template>

<script setup>
import { computed, ref } from 'vue';
import { 
  Pencil, 
  Trash2, 
  ArrowUpRight, 
  Terminal, 
  Layers, 
  Search, 
  X, 
  ShieldCheck, 
  ShieldAlert, 
  Server, 
  Cpu, 
  Activity, 
  FileCode2, 
  Database 
} from 'lucide-vue-next';
import PillBadge from './PillBadge.vue';
import { tagTone } from '../services/tags';

const props = defineProps({
  id: { type: String, required: true },
  items: { type: Array, required: true },
  empty: { type: String, required: true },
  editable: { type: Boolean, default: false },
});

defineEmits(['edit', 'delete', 'view-case']);

const activeDomain = ref('all');
const searchQuery = ref('');

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

const filteredGroups = computed(() => {
  const query = searchQuery.value.toLowerCase().trim();
  
  return stackGroups.value
    .map((group) => {
      // Filtrer par domaine si un domaine spécifique est sélectionné
      if (activeDomain.value !== 'all' && group.category !== activeDomain.value) {
        return null;
      }

      // Filtrer par texte de recherche
      let matchedItems = group.items;
      if (query) {
        matchedItems = group.items.filter((item) => {
          const haystack = `${item.title} ${item.subtitle || ''} ${item.description || ''} ${item.content?.tools || ''}`.toLowerCase();
          return haystack.includes(query);
        });
      }

      if (!matchedItems.length) return null;

      return {
        ...group,
        items: matchedItems,
      };
    })
    .filter(Boolean);
});

function getCategoryIconComponent(cat) {
  const c = String(cat).toLowerCase();
  if (c.includes('détect') || c.includes('siem') || c.includes('soc') || c.includes('surveill')) return Activity;
  if (c.includes('intel') || c.includes('threat') || c.includes('misp')) return ShieldAlert;
  if (c.includes('systèm') || c.includes('linux') || c.includes('window') || c.includes('serveur')) return Server;
  if (c.includes('réseau') || c.includes('cisco') || c.includes('fortinet')) return Cpu;
  if (c.includes('script') || c.includes('python') || c.includes('dev') || c.includes('code')) return FileCode2;
  if (c.includes('data') || c.includes('db') || c.includes('base')) return Database;
  return ShieldCheck;
}

function formatCategoryName(cat) {
  if (cat.length > 28) {
    return cat.slice(0, 26) + '...';
  }
  return cat;
}

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

.stack-heading {
  margin-bottom: 2rem;
}

.stack-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.45rem;
  padding: 0.35rem 0.8rem;
  background: rgba(44, 0, 30, 0.55);
  color: #fff;
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 999px;
  font-size: 0.82rem;
  font-weight: 700;
  margin-bottom: 0.6rem;
  backdrop-filter: blur(8px);
}

.stack-heading h2 {
  margin: 0 0 0.5rem;
  color: #ffffff;
  font-size: clamp(2rem, 4vw, 2.75rem);
  font-weight: 800;
  letter-spacing: -0.02em;
}

.stack-intro {
  margin: 0;
  color: rgba(255, 255, 255, 0.94);
  font-size: 1.05rem;
  line-height: 1.55;
  max-width: 760px;
}

/* Panneau de contrôle : Onglets & Recherche */
.stack-control-panel {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
  margin-bottom: 2.25rem;
}

.stack-domain-tabs {
  display: flex;
  flex-wrap: wrap;
  gap: 0.6rem;
}

.stack-domain-tab {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.6rem 1rem;
  background: rgba(255, 255, 255, 0.18);
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 999px;
  color: #ffffff;
  font-size: 0.88rem;
  font-weight: 700;
  cursor: pointer;
  backdrop-filter: blur(10px);
  transition: all 0.22s cubic-bezier(0.16, 1, 0.3, 1);
}

.stack-domain-tab:hover {
  background: rgba(255, 255, 255, 0.3);
  transform: translateY(-2px);
}

.stack-domain-tab.is-active {
  background: #ffffff;
  color: var(--aubergine-dark);
  border-color: #ffffff;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.18);
  transform: translateY(-2px);
}

.tab-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 20px;
  height: 20px;
  padding: 0 6px;
  border-radius: 10px;
  background: rgba(0, 0, 0, 0.2);
  font-size: 0.75rem;
  font-weight: 800;
}

.stack-domain-tab.is-active .tab-badge {
  background: var(--ubuntu-orange);
  color: #ffffff;
}

/* Barre de recherche instantanée */
.stack-search-bar {
  position: relative;
  width: 100%;
}

.stack-search-bar .search-icon {
  position: absolute;
  left: 1.1rem;
  top: 50%;
  transform: translateY(-50%);
  color: rgba(255, 255, 255, 0.75);
  pointer-events: none;
}

.stack-search-bar input {
  width: 100%;
  padding: 0.85rem 2.8rem 0.85rem 2.8rem;
  background: rgba(44, 0, 30, 0.45);
  border: 1px solid rgba(255, 255, 255, 0.35);
  border-radius: 14px;
  color: #ffffff;
  font-size: 0.95rem;
  backdrop-filter: blur(12px);
  transition: border-color 0.2s, background 0.2s, box-shadow 0.2s;
}

.stack-search-bar input::placeholder {
  color: rgba(255, 255, 255, 0.72);
}

.stack-search-bar input:focus {
  outline: none;
  background: rgba(44, 0, 30, 0.7);
  border-color: #ffffff;
  box-shadow: 0 0 0 3px rgba(255, 255, 255, 0.25);
}

.clear-search-btn {
  position: absolute;
  right: 1rem;
  top: 50%;
  transform: translateY(-50%);
  background: rgba(255, 255, 255, 0.2);
  border: none;
  color: #fff;
  border-radius: 50%;
  width: 22px;
  height: 22px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: background 0.2s;
}

.clear-search-btn:hover {
  background: rgba(255, 255, 255, 0.4);
}

/* Grille de cartes & Contenu */
.stack-active-container {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.stack-display-wrapper {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.stack-group-block {
  background: rgba(255, 255, 255, 0.94);
  border: 1px solid rgba(255, 255, 255, 0.6);
  border-radius: 1.4rem;
  padding: 1.75rem 2rem;
  box-shadow: 0 10px 36px rgba(44, 0, 30, 0.15);
  backdrop-filter: blur(14px);
}

.stack-domain-banner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  padding-bottom: 1.1rem;
  margin-bottom: 1.5rem;
  border-bottom: 1px solid rgba(119, 33, 111, 0.12);
}

.domain-banner-left {
  display: flex;
  align-items: center;
  gap: 0.85rem;
  flex-wrap: wrap;
}

.domain-banner-subtitle {
  font-size: 0.88rem;
  font-weight: 700;
  color: var(--aubergine);
}

.domain-status-tag {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  font-size: 0.8rem;
  font-weight: 700;
  color: #15803d;
  background: rgba(22, 163, 74, 0.1);
  padding: 0.25rem 0.65rem;
  border-radius: 6px;
  border: 1px solid rgba(22, 163, 74, 0.2);
}

.stack-cards-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(290px, 1fr));
  gap: 1.35rem;
}

.stack-live-card {
  background: #ffffff;
  border: 1px solid rgba(119, 33, 111, 0.12);
  border-radius: 1.1rem;
  padding: 1.4rem 1.5rem;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  gap: 1.1rem;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.04);
  transition: transform 0.25s cubic-bezier(0.16, 1, 0.3, 1), border-color 0.25s, box-shadow 0.25s;
}

.stack-live-card:hover {
  transform: translateY(-4px);
  border-color: var(--ubuntu-orange);
  box-shadow: 0 10px 28px rgba(233, 84, 32, 0.2);
}

.live-card-top {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 0.75rem;
}

.live-card-title-group {
  display: flex;
  flex-direction: column;
  gap: 0.3rem;
}

.live-card-title {
  margin: 0;
  font-size: 1.18rem;
  font-weight: 800;
  color: var(--aubergine-dark);
  line-height: 1.3;
}

.live-card-subtitle {
  font-size: 0.85rem;
  font-weight: 700;
  color: var(--ubuntu-orange);
  line-height: 1.35;
}

.pulse-dot {
  display: block;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #10b981;
  box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.25);
  margin-top: 5px;
}

.live-card-desc {
  margin: 0;
  color: var(--muted);
  font-size: 0.93rem;
  line-height: 1.6;
  flex-grow: 1;
}

.live-card-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.4rem;
}

.live-tag-chip {
  padding: 0.22rem 0.55rem;
  border-radius: 6px;
  background: rgba(119, 33, 111, 0.07);
  border: 1px solid rgba(119, 33, 111, 0.14);
  font-size: 0.78rem;
  font-weight: 700;
  color: var(--aubergine);
}

.live-card-bottom {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.75rem;
  margin-top: auto;
  padding-top: 0.65rem;
  border-top: 1px dashed rgba(0, 0, 0, 0.08);
}

.live-detail-link {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  background: transparent;
  border: none;
  color: var(--aubergine);
  font-size: 0.9rem;
  font-weight: 800;
  cursor: pointer;
  padding: 0.25rem 0;
  transition: color 0.2s, gap 0.2s;
}

.live-detail-link:hover {
  color: var(--ubuntu-orange);
  gap: 0.55rem;
}

.live-admin-actions {
  display: flex;
  align-items: center;
  gap: 0.35rem;
}

/* État vide recherche */
.stack-no-results {
  padding: 3rem 2rem;
  text-align: center;
  background: rgba(255, 255, 255, 0.94);
  border-radius: 1.4rem;
  color: var(--aubergine-dark);
}

.empty-search-icon {
  color: var(--ubuntu-orange);
  margin-bottom: 0.75rem;
}

.stack-no-results h3 {
  margin: 0 0 0.5rem;
  font-size: 1.3rem;
}

.stack-no-results p {
  color: var(--muted);
  margin: 0 0 1.5rem;
}

/* Transitions */
.stack-fade-enter-active,
.stack-fade-leave-active {
  transition: all 0.3s ease;
}

.stack-fade-enter-from,
.stack-fade-leave-to {
  opacity: 0;
  transform: translateY(12px);
}

@media (max-width: 768px) {
  .stack-group-block {
    padding: 1.25rem;
  }
  .stack-cards-grid {
    grid-template-columns: 1fr;
  }
  .domain-status-tag {
    display: none;
  }
}
</style>
