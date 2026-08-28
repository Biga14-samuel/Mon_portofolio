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
        Savoir-faire et technologies validés en conditions opérationnelles, classés par projet. Cliquez sur une compétence pour consulter sa fiche détaillée.
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

    <!-- Groupes structurés par Réalisation -->
    <div v-if="filteredRealizationGroups.length" class="stack-active-container">
      <div 
        v-for="group in filteredRealizationGroups" 
        :key="group.id" 
        class="stack-group-block"
      >
        <!-- En-tête de la réalisation -->
        <div class="stack-realization-banner">
          <div class="realization-banner-title">
            <component :is="group.icon" :size="20" class="realization-icon" aria-hidden="true" />
            <div>
              <h3 class="realization-title-text">{{ group.title }}</h3>
              <span class="realization-badge-pill">{{ group.badge }}</span>
            </div>
          </div>
          <span class="realization-count-badge">
            {{ group.items.length }} compétence{{ group.items.length > 1 ? 's' : '' }}
          </span>
        </div>

        <!-- Grille compacte de mini-cartes épurées (pas de pavé de texte redondant) -->
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
                
                <!-- Puces outils succinctes -->
                <div v-if="getToolsList(item).length" class="compact-card-tools">
                  <span v-for="t in getToolsList(item)" :key="t" class="compact-tool-chip">{{ t }}</span>
                </div>
              </div>

              <div class="compact-card-action">
                <span>Fiche détaillée</span>
                <ArrowUpRight :size="14" aria-hidden="true" />
              </div>
            </button>

            <!-- Actions admin en survol/mode admin -->
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
  empty: { type: String, required: true },
  editable: { type: Boolean, default: false },
});

defineEmits(['edit', 'delete', 'view-case']);

const searchQuery = ref('');

// Groupes par réalisation concrète
const realizationGroups = computed(() => {
  const groups = {
    soc: {
      id: 'soc',
      title: 'Conception & Déploiement SOC Open-Source (PANESS IT)',
      badge: 'Projet SOC SIEM / SOAR',
      icon: ShieldAlert,
      items: [],
    },
    lab: {
      id: 'lab',
      title: 'Infrastructure Réseau & Virtualisation Multi-OS',
      badge: 'Lab 5 VMs VirtualBox',
      icon: Server,
      items: [],
    },
    network: {
      id: 'network',
      title: 'Détection Réseau & Analyse de Flux (NIDS)',
      badge: 'Suricata / Wireshark / Nmap',
      icon: Cpu,
      items: [],
    },
    automation: {
      id: 'automation',
      title: 'Automatisation, Scripting & Pipelines de Réponse',
      badge: 'Python / Bash / Webhooks API',
      icon: FileCode2,
      items: [],
    },
    other: {
      id: 'other',
      title: 'Autres Compétences Techniques & Méthodologies',
      badge: 'Transversal',
      icon: Layers,
      items: [],
    }
  };

  props.items.forEach((item) => {
    const text = `${item.title} ${item.subtitle || ''} ${item.description || ''} ${item.category || ''} ${item.content?.tools || ''}`.toLowerCase();
    
    if (text.includes('wazuh') || text.includes('yara') || text.includes('shuffle') || text.includes('iris') || text.includes('misp') || text.includes('fim') || text.includes('deepseek') || text.includes('telegram')) {
      groups.soc.items.push(item);
    } else if (text.includes('suricata') || text.includes('wireshark') || text.includes('nmap') || text.includes('cisco') || text.includes('protocole') || text.includes('nids')) {
      groups.network.items.push(item);
    } else if (text.includes('python') || text.includes('bash') || text.includes('script') || text.includes('api') || text.includes('webhook')) {
      groups.automation.items.push(item);
    } else if (text.includes('docker') || text.includes('virtualbox') || text.includes('linux') || text.includes('windows') || text.includes('debian') || text.includes('multi-os') || text.includes('auditd') || text.includes('sysmon')) {
      groups.lab.items.push(item);
    } else {
      groups.other.items.push(item);
    }
  });

  return Object.values(groups).filter(g => g.items.length > 0);
});

// Filtrage par texte de recherche
const filteredRealizationGroups = computed(() => {
  const query = searchQuery.value.toLowerCase().trim();
  if (!query) return realizationGroups.value;

  return realizationGroups.value
    .map((group) => {
      const matched = group.items.filter((item) => {
        const haystack = `${item.title} ${item.subtitle || ''} ${item.description || ''} ${item.content?.tools || ''}`.toLowerCase();
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
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 1rem;
}

.stack-compact-card-wrapper {
  position: relative;
}

.stack-compact-card {
  width: 100%;
  text-align: left;
  background: #ffffff;
  border: 1px solid rgba(119, 33, 111, 0.14);
  border-radius: 14px;
  padding: 1rem 1.15rem;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  gap: 0.85rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.03);
  cursor: pointer;
  font-family: inherit;
  transition: transform 0.2s cubic-bezier(0.16, 1, 0.3, 1), border-color 0.2s, box-shadow 0.2s;
}

.stack-compact-card:hover {
  transform: translateY(-3px);
  border-color: var(--ubuntu-orange);
  box-shadow: 0 8px 20px rgba(233, 84, 32, 0.18);
}

.compact-card-main {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
}

.compact-card-top {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 0.5rem;
}

.compact-card-title {
  margin: 0;
  font-size: 1.02rem;
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

.compact-card-tools {
  display: flex;
  flex-wrap: wrap;
  gap: 0.35rem;
  margin-top: 0.4rem;
}

.compact-tool-chip {
  padding: 0.18rem 0.45rem;
  border-radius: 6px;
  background: rgba(119, 33, 111, 0.06);
  border: 1px solid rgba(119, 33, 111, 0.12);
  color: var(--aubergine-dark);
  font-size: 0.74rem;
  font-weight: 700;
}

.compact-card-action {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 0.35rem;
  font-size: 0.82rem;
  font-weight: 800;
  color: var(--ubuntu-orange-dark);
  padding-top: 0.4rem;
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
