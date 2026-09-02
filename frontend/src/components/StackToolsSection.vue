<template>
  <section class="content-section stack-section blueprint-bg reveal-on-scroll" :id="id" :aria-labelledby="`${id}-title`">
    <!-- Header & Titre épuré -->
    <div class="stack-heading">
      <div>
        <span class="stack-badge">
          <Terminal :size="14" aria-hidden="true" />
          Compétences par Réalisation
        </span>
        <h2 :id="`${id}-title`">
          <span>Stack &amp; Outils</span>
        </h2>
      </div>
      <p class="stack-intro">
        Savoir-faire et technologies validés en conditions opérationnelles, classés par réalisation. Cliquez sur une compétence pour consulter sa fiche détaillée.
      </p>
    </div>

    <!-- Barre de recherche rapide -->
    <div class="stack-search-bar-wrapper">
      <div class="stack-search-bar">
        <Search :size="16" class="search-icon" aria-hidden="true" />
        <input
          v-model.trim="searchQuery"
          type="text"
          placeholder="Filtrer une compétence ou un outil (Wazuh, Suricata, Docker, Python, Linux...)..."
          aria-label="Recherche de compétences"
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

    <!-- État de chargement (Skeleton Dashboard & Outils) -->
    <div v-if="loading" class="stack-active-container" aria-label="Chargement des compétences...">
      <div v-for="n in 2" :key="n" class="skeleton-card" style="padding: 24px; margin-bottom: 20px;">
        <div style="display: flex; gap: 14px; align-items: center; margin-bottom: 20px;">
          <div class="skeleton-circle skeleton-shimmer" style="width: 40px; height: 40px;"></div>
          <div style="flex: 1; display: flex; flex-direction: column; gap: 8px;">
            <div class="skeleton-pill skeleton-shimmer" style="width: 35%; height: 20px;"></div>
            <div class="skeleton-pill skeleton-shimmer" style="width: 20%; height: 12px;"></div>
          </div>
          <div class="skeleton-pill skeleton-shimmer" style="width: 80px; height: 24px;"></div>
        </div>
        <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 14px;">
          <div v-for="k in 6" :key="k" class="skeleton-shimmer" style="height: 64px; border-radius: 12px; padding: 12px; display: flex; flex-direction: column; justify-content: center; gap: 6px;">
            <div class="skeleton-pill" style="width: 70%; height: 14px; background: rgba(255,255,255,0.12);"></div>
            <div class="skeleton-pill" style="width: 40%; height: 10px; background: rgba(255,255,255,0.08);"></div>
          </div>
        </div>
      </div>
    </div>

    <!-- Groupes dynamiques structurés par Réalisation -->
    <div v-else-if="filteredRealizationGroups.length" class="stack-active-container">
      <div 
        v-for="group in filteredRealizationGroups" 
        :key="group.id" 
        class="stack-group-block"
      >
        <!-- En-tête de la réalisation -->
        <div class="stack-realization-banner">
          <div class="realization-banner-title">
            <component :is="group.icon || ShieldAlert" :size="20" class="realization-icon" aria-hidden="true" />
            <div>
              <h3 class="realization-title-text">{{ group.title }}</h3>
              <span class="realization-badge-pill">{{ group.badge }}</span>
            </div>
          </div>
          <span class="realization-count-badge">
            {{ group.items.length }} compétence{{ group.items.length > 1 ? 's' : '' }}
          </span>
        </div>

        <!-- Grille compacte de mini-cartes ultra-épurées (sans badges redondants) -->
        <div class="stack-compact-grid">
          <div 
            v-for="item in group.items" 
            :key="item.id" 
            class="stack-compact-card-wrapper"
          >
            <button 
              class="stack-compact-card"
              type="button"
              :aria-label="`Consulter la fiche technique : ${item.title}`"
              @click="$emit('view-case', item)"
            >
              <div class="compact-card-main">
                <div class="compact-card-top">
                  <h4 class="compact-card-title">{{ item.title }}</h4>
                  <span class="pulse-dot"></span>
                </div>
                
                <span v-if="item.subtitle" class="compact-card-subtitle">{{ item.subtitle }}</span>
              </div>

              <div class="compact-card-action">
                <span>Fiche détaillée</span>
                <ArrowUpRight :size="14" aria-hidden="true" />
              </div>
            </button>

            <!-- Actions admin en mode admin -->
            <div v-if="editable" class="compact-admin-actions" aria-label="Actions administrateur">
              <button 
                class="icon-button small" 
                type="button" 
                :aria-label="`Modifier ${item.title}`" 
                @click.stop="$emit('edit', item)"
              >
                <Pencil :size="13" aria-hidden="true" />
              </button>
              <button 
                class="icon-button small danger" 
                type="button" 
                :aria-label="`Supprimer ${item.title}`" 
                @click.stop="$emit('delete', item)"
              >
                <Trash2 :size="13" aria-hidden="true" />
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- État vide si recherche sans résultat -->
    <div v-else class="stack-no-results glass-card">
      <Search :size="32" class="empty-search-icon" />
      <h3>Aucune compétence trouvée pour "{{ searchQuery }}"</h3>
      <button type="button" class="button secondary" @click="searchQuery = ''">
        Réinitialiser la recherche
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
  Search, 
  X, 
  ShieldAlert, 
  Server, 
  Cpu, 
  FileCode2, 
  Layers
} from 'lucide-vue-next';

const props = defineProps({
  id: { type: String, required: true },
  items: { type: Array, required: true },
  realisations: { type: Array, default: () => [] },
  empty: { type: String, required: true },
  loading: { type: Boolean, default: false },
  editable: { type: Boolean, default: false },
});

defineEmits(['edit', 'delete', 'view-case']);

const searchQuery = ref('');

// Groupes par réalisation dynamique (prend en compte toutes les réalisations du portfolio)
const realizationGroups = computed(() => {
  const realisationsList = props.realisations || [];
  const groupsMap = new Map();

  // 1. Initialiser les groupes pour chaque réalisation réelle
  realisationsList.forEach((r) => {
    const isCyber = (r.category || '').toLowerCase().includes('cyber');
    const isNetwork = (r.category || '').toLowerCase().includes('réseau') || (r.category || '').toLowerCase().includes('network');
    
    groupsMap.set(r.title.toLowerCase().trim(), {
      id: `real-${r.id}`,
      title: r.title,
      badge: r.category || 'Réalisation',
      icon: isCyber ? ShieldAlert : isNetwork ? Cpu : Server,
      items: [],
    });
  });

  // Groupe pour les compétences transversales / de base
  const generalGroup = {
    id: 'general',
    title: 'Compétences Transversales & Environnements Systèmes',
    badge: 'Socle Technique',
    icon: Layers,
    items: [],
  };

  props.items.forEach((item) => {
    // A. Lien explicite via item.content.realisation_title
    const explicitReal = item.content?.realisation_title?.toLowerCase().trim();
    if (explicitReal && groupsMap.has(explicitReal)) {
      groupsMap.get(explicitReal).items.push(item);
      return;
    }

    // B. Correspondance par mot-clé avec les titres des réalisations existantes
    const itemText = `${item.title} ${item.subtitle || ''} ${item.description || ''} ${item.category || ''} ${item.content?.tools || ''}`.toLowerCase();
    
    let matchedGroup = null;
    for (const [key, group] of groupsMap.entries()) {
      const keyWords = key.split(/[\s,;:–—\-_]+/).filter((w) => w.length > 3);
      if (keyWords.some((w) => itemText.includes(w))) {
        matchedGroup = group;
        break;
      }
    }

    if (matchedGroup) {
      matchedGroup.items.push(item);
    } else {
      if (groupsMap.size > 0 && (itemText.includes('soc') || itemText.includes('wazuh') || itemText.includes('yara') || itemText.includes('suricata') || itemText.includes('shuffle') || itemText.includes('iris') || itemText.includes('misp') || itemText.includes('fim') || itemText.includes('auditd') || itemText.includes('sysmon'))) {
        const firstGroup = Array.from(groupsMap.values())[0];
        firstGroup.items.push(item);
      } else {
        generalGroup.items.push(item);
      }
    }
  });

  const result = Array.from(groupsMap.values()).filter((g) => g.items.length > 0);
  if (generalGroup.items.length > 0) {
    result.push(generalGroup);
  }

  // Si aucune réalisation n'est encore enregistrée, afficher un groupe de secours avec les compétences
  if (result.length === 0 && props.items.length > 0) {
    result.push({
      id: 'default',
      title: 'Compétences & Outils Techniques',
      badge: 'Général',
      icon: Terminal,
      items: [...props.items],
    });
  }

  return result;
});

// Filtrage par texte de recherche
const filteredRealizationGroups = computed(() => {
  const query = searchQuery.value.toLowerCase().trim();
  if (!query) return realizationGroups.value;

  return realizationGroups.value
    .map((group) => {
      const matched = group.items.filter((item) => {
        const haystack = `${item.title} ${item.subtitle || ''} ${item.description || ''} ${item.category || ''} ${item.content?.tools || ''}`.toLowerCase();
        return haystack.includes(query);
      });
      if (!matched.length) return null;
      return {
        ...group,
        items: matched,
      };
    })
    .filter(Boolean);
});
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
  margin-bottom: 1.75rem;
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
  font-size: 1.02rem;
  line-height: 1.55;
  max-width: 760px;
}

.stack-search-bar-wrapper {
  margin-bottom: 2rem;
}

.stack-search-bar {
  position: relative;
  width: 100%;
}

.search-icon {
  position: absolute;
  left: 1.2rem;
  top: 50%;
  transform: translateY(-50%);
  color: rgba(255, 255, 255, 0.75);
  pointer-events: none;
}

.stack-search-bar input {
  width: 100%;
  padding: 0.9rem 2.8rem 0.9rem 3rem;
  background: rgba(44, 0, 30, 0.45);
  border: 1px solid rgba(255, 255, 255, 0.25);
  border-radius: 14px;
  color: #fff;
  font-size: 0.95rem;
  outline: none;
  backdrop-filter: blur(10px);
  transition: background 0.2s, border-color 0.2s;
}

.stack-search-bar input:focus {
  background: rgba(44, 0, 30, 0.65);
  border-color: #ffffff;
}

.stack-search-bar input::placeholder {
  color: rgba(255, 255, 255, 0.65);
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
  gap: 1.75rem;
}

.stack-group-block {
  background: rgba(255, 255, 255, 0.96);
  border: 1px solid rgba(255, 255, 255, 0.7);
  border-radius: 1.3rem;
  padding: 1.5rem 1.75rem;
  box-shadow: 0 10px 32px rgba(44, 0, 30, 0.14);
}

/* En-tête de chaque Réalisation */
.stack-realization-banner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  padding-bottom: 1rem;
  margin-bottom: 1.25rem;
  border-bottom: 1px solid rgba(119, 33, 111, 0.12);
  flex-wrap: wrap;
}

.realization-banner-title {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.realization-icon {
  color: var(--ubuntu-orange-dark);
  flex-shrink: 0;
}

.realization-title-text {
  margin: 0 0 0.2rem;
  font-size: 1.15rem;
  font-weight: 800;
  color: var(--aubergine-dark);
  line-height: 1.25;
}

.realization-badge-pill {
  display: inline-block;
  font-size: 0.78rem;
  font-weight: 700;
  color: var(--muted);
  letter-spacing: 0.02em;
}

.realization-count-badge {
  font-size: 0.8rem;
  font-weight: 800;
  color: #15803d;
  background: rgba(22, 163, 74, 0.1);
  padding: 0.25rem 0.65rem;
  border-radius: 999px;
  border: 1px solid rgba(22, 163, 74, 0.2);
}

/* Grille compacte */
.stack-compact-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 0.85rem;
}

.stack-compact-card-wrapper {
  position: relative;
}

.stack-compact-card {
  width: 100%;
  text-align: left;
  background: #ffffff;
  border: 1px solid rgba(119, 33, 111, 0.14);
  border-radius: 12px;
  padding: 0.9rem 1.1rem;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  gap: 0.65rem;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.03);
  cursor: pointer;
  font-family: inherit;
  transition: transform 0.2s cubic-bezier(0.16, 1, 0.3, 1), border-color 0.2s, box-shadow 0.2s;
}

.stack-compact-card:hover {
  transform: translateY(-3px);
  border-color: var(--ubuntu-orange);
  box-shadow: 0 6px 18px rgba(233, 84, 32, 0.18);
}

.compact-card-main {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.compact-card-top {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 0.5rem;
}

.compact-card-title {
  margin: 0;
  font-size: 1rem;
  font-weight: 800;
  color: var(--aubergine-dark);
  line-height: 1.3;
}

.compact-card-subtitle {
  font-size: 0.8rem;
  font-weight: 700;
  color: var(--ubuntu-orange-dark);
  line-height: 1.3;
}

.pulse-dot {
  display: block;
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: #10b981;
  box-shadow: 0 0 0 2px rgba(16, 185, 129, 0.25);
  margin-top: 4px;
  flex-shrink: 0;
}

.compact-card-action {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 0.35rem;
  font-size: 0.8rem;
  font-weight: 800;
  color: var(--ubuntu-orange-dark);
  padding-top: 0.35rem;
  border-top: 1px dashed rgba(119, 33, 111, 0.1);
}

.stack-compact-card:hover .compact-card-action {
  color: #a92e07;
}

.compact-admin-actions {
  position: absolute;
  top: 8px;
  right: 8px;
  display: flex;
  gap: 4px;
  z-index: 2;
}

.icon-button.small {
  width: 24px;
  height: 24px;
  padding: 0;
  display: grid;
  place-items: center;
  border-radius: 6px;
  background: rgba(255, 255, 255, 0.9);
  border: 1px solid rgba(0, 0, 0, 0.1);
  cursor: pointer;
}

.icon-button.small.danger:hover {
  background: #fee2e2;
  color: #dc2626;
}

/* Pas de résultats */
.stack-no-results {
  text-align: center;
  padding: 3rem 2rem;
  background: #ffffff;
  border-radius: 1.25rem;
  color: var(--text);
}

.empty-search-icon {
  color: var(--muted);
  margin-bottom: 1rem;
}
</style>
