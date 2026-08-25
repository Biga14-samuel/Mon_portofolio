<template>
  <div class="skill-detail-container">
    <!-- En-tête Fiche Technique Spécifique -->
    <div class="skill-tech-header glass-card">
      <div class="skill-header-meta">
        <div class="skill-badge-group">
          <PillBadge :tone="tagTone(item.category)">{{ item.category }}</PillBadge>
          <span class="skill-status-indicator">
            <span class="skill-pulse-dot"></span>
            Compétence Validée en Conditions Réelles
          </span>
        </div>
        <span v-if="item.subtitle" class="skill-level-tag">
          {{ item.subtitle }}
        </span>
      </div>

      <h2 class="skill-main-title">{{ item.title }}</h2>
      <p class="skill-main-desc">{{ item.description }}</p>

      <!-- Puces des technologies et outils associés -->
      <div v-if="stack.length" class="skill-stack-pills">
        <span class="stack-pills-label">Outils &amp; Protocoles liés :</span>
        <div class="pills-wrapper">
          <span v-for="tool in stack" :key="tool" class="skill-tool-chip">
            <CheckCircle2 :size="13" class="chip-icon" />
            {{ tool }}
          </span>
        </div>
      </div>
    </div>

    <!-- Grille Bento Interactive des Domaines d'application -->
    <div class="skill-bento-grid">
      <!-- 1. Contexte d'application & Cas d'usage -->
      <div class="skill-bento-card bento-card--context glass-card">
        <div class="bento-card-header">
          <div class="bento-icon-box icon-orange">
            <Workflow :size="20" />
          </div>
          <div>
            <h3 class="bento-card-title">Cas d'usage &amp; Déploiement</h3>
            <span class="bento-card-subtitle">Contexte opérationnel</span>
          </div>
        </div>
        <div class="bento-card-body">
          <p v-if="contextSection">{{ contextSection.body }}</p>
          <p v-else>Compétence exploitée transversalement dans la sécurisation, l'automatisation et l'administration des infrastructures.</p>
        </div>
      </div>

      <!-- 2. Maîtrise Technique & Réalisations concrètes -->
      <div class="skill-bento-card bento-card--mastery glass-card">
        <div class="bento-card-header">
          <div class="bento-icon-box icon-purple">
            <Cpu :size="20" />
          </div>
          <div>
            <h3 class="bento-card-title">Savoir-faire &amp; Mécanismes</h3>
            <span class="bento-card-subtitle">Détails d'implémentation</span>
          </div>
        </div>
        <div class="bento-card-body">
          <p v-if="masterySection" style="white-space: pre-wrap;">{{ masterySection.body }}</p>
          <p v-else>{{ item.description }}</p>
        </div>
      </div>

      <!-- 3. Résultats & Impact -->
      <div class="skill-bento-card bento-card--impact glass-card">
        <div class="bento-card-header">
          <div class="bento-icon-box icon-green">
            <ShieldCheck :size="20" />
          </div>
          <div>
            <h3 class="bento-card-title">Impact &amp; Résultats</h3>
            <span class="bento-card-subtitle">Bénéfices et livrables</span>
          </div>
        </div>
        <div class="bento-card-body">
          <p v-if="impactSection">{{ impactSection.body }}</p>
          <p v-else>Amélioration continue de la réactivité opérationnelle, réduction des erreurs manuelles et renforcement de la posture de sécurité.</p>
        </div>
      </div>
    </div>

    <!-- Visuel / Diagramme ou capture si présente -->
    <div v-if="primaryImage || detailImages.length" class="skill-visuals-panel glass-card">
      <div class="visuals-header">
        <div class="bento-icon-box icon-blue">
          <FileText :size="20" />
        </div>
        <div>
          <h3 class="bento-card-title">Preuves techniques &amp; Illustrations</h3>
          <span class="bento-card-subtitle">Captures d'écran, logs ou schémas associés</span>
        </div>
      </div>

      <div class="skill-images-grid">
        <figure 
          v-for="(img, idx) in allImages" 
          :key="img" 
          class="skill-image-card"
          @click="$emit('open-lightbox', allImages, idx, item.title)"
        >
          <img :src="img" :alt="`Illustration ${item.title}`" loading="lazy" />
          <div class="skill-image-overlay">
            <ExternalLink :size="18" />
            <span>Agrandir</span>
          </div>
        </figure>
      </div>
    </div>

    <!-- Boutons de ressources (PDF, GitHub, Démo) -->
    <div v-if="item.github_url || item.demo_url || pdfUrl" class="skill-actions-bar glass-card">
      <span class="actions-bar-title">Ressources &amp; Références :</span>
      <div class="actions-btns-row">
        <a v-if="item.github_url" :href="item.github_url" target="_blank" rel="noreferrer" class="button secondary">
          <Github :size="16" />
          Code source / Scripts
        </a>
        <a v-if="pdfUrl" :href="pdfUrl" target="_blank" rel="noreferrer" class="button secondary">
          <FileText :size="16" />
          Documentation technique (PDF)
        </a>
        <a v-if="item.demo_url" :href="item.demo_url" target="_blank" rel="noreferrer" class="button primary">
          <ExternalLink :size="16" />
          Voir la démonstration
        </a>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { 
  ShieldCheck, 
  Cpu, 
  Workflow, 
  FileText, 
  CheckCircle2, 
  ExternalLink, 
  Github 
} from 'lucide-vue-next';
import PillBadge from './PillBadge.vue';
import { tagTone } from '../services/tags';

const props = defineProps({
  item: { type: Object, required: true },
  sections: { type: Array, default: () => [] },
  stack: { type: Array, default: () => [] },
  pdfUrl: { type: String, default: '' },
  primaryImage: { type: String, default: '' },
  detailImages: { type: Array, default: () => [] },
});

defineEmits(['open-lightbox', 'close']);

const allImages = computed(() => {
  const list = [];
  if (props.primaryImage) list.push(props.primaryImage);
  if (props.detailImages?.length) {
    props.detailImages.forEach((img) => {
      if (!list.includes(img)) list.push(img);
    });
  }
  return list;
});

const contextSection = computed(() => {
  return props.sections.find((s) => {
    const t = s.title.toLowerCase();
    return t.includes('contexte') || t.includes('cadre') || t.includes('cas') || t.includes('projet');
  }) || props.sections[1];
});

const masterySection = computed(() => {
  return props.sections.find((s) => {
    const t = s.title.toLowerCase();
    return t.includes('technique') || t.includes('maîtrise') || t.includes('apprentissage') || t.includes('flux') || t.includes('compétence');
  }) || props.sections[2] || props.sections[0];
});

const impactSection = computed(() => {
  return props.sections.find((s) => {
    const t = s.title.toLowerCase();
    return t.includes('impact') || t.includes('résultat') || t.includes('attestation') || t.includes('certif');
  }) || props.sections[3];
});
</script>

<style scoped>
.skill-detail-container {
  display: flex;
  flex-direction: column;
  gap: 1.75rem;
  width: 100%;
  padding: 0.5rem 0;
}

/* En-tête fiche technique */
.skill-tech-header {
  padding: 2rem 2.25rem;
  border-radius: 1.4rem;
  background: var(--surface-card);
  border: 1px solid var(--outline);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
}

.skill-header-meta {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  flex-wrap: wrap;
  margin-bottom: 1.25rem;
}

.skill-badge-group {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  flex-wrap: wrap;
}

.skill-status-indicator {
  display: inline-flex;
  align-items: center;
  gap: 0.45rem;
  font-size: 0.82rem;
  font-weight: 700;
  color: #15803d;
  background: rgba(22, 163, 74, 0.1);
  border: 1px solid rgba(22, 163, 74, 0.25);
  padding: 0.25rem 0.75rem;
  border-radius: 999px;
}

.skill-pulse-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: #16a34a;
  box-shadow: 0 0 0 3px rgba(22, 163, 74, 0.25);
}

.skill-level-tag {
  font-size: 0.88rem;
  font-weight: 700;
  color: var(--ubuntu-orange);
  background: rgba(233, 84, 32, 0.08);
  padding: 0.3rem 0.8rem;
  border-radius: 8px;
  border: 1px solid rgba(233, 84, 32, 0.2);
}

.skill-main-title {
  margin: 0 0 0.75rem;
  font-size: clamp(1.8rem, 3.5vw, 2.5rem);
  font-weight: 800;
  color: var(--aubergine-dark);
  line-height: 1.2;
}

.skill-main-desc {
  margin: 0 0 1.5rem;
  color: var(--muted);
  font-size: 1.05rem;
  line-height: 1.6;
}

.skill-stack-pills {
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
  padding-top: 1.25rem;
  border-top: 1px solid var(--border);
}

.stack-pills-label {
  font-size: 0.82rem;
  font-weight: 700;
  color: var(--muted);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.pills-wrapper {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.skill-tool-chip {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  padding: 0.35rem 0.75rem;
  border-radius: 8px;
  background: rgba(119, 33, 111, 0.08);
  border: 1px solid rgba(119, 33, 111, 0.18);
  font-size: 0.85rem;
  font-weight: 700;
  color: var(--aubergine-dark);
}

.chip-icon {
  color: var(--ubuntu-orange);
}

/* Grille Bento */
.skill-bento-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.25rem;
}

.skill-bento-card {
  padding: 1.5rem 1.6rem;
  border-radius: 1.25rem;
  background: var(--surface-card);
  border: 1px solid var(--outline);
  display: flex;
  flex-direction: column;
  gap: 1rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
  transition: transform 0.22s ease, box-shadow 0.22s ease;
}

.skill-bento-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}

.bento-card--mastery {
  grid-column: span 2;
}

.bento-card-header {
  display: flex;
  align-items: center;
  gap: 0.85rem;
}

.bento-icon-box {
  width: 42px;
  height: 42px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.icon-orange {
  background: rgba(233, 84, 32, 0.12);
  color: var(--ubuntu-orange);
}

.icon-purple {
  background: rgba(119, 33, 111, 0.12);
  color: var(--aubergine);
}

.icon-green {
  background: rgba(22, 163, 74, 0.12);
  color: #16a34a;
}

.icon-blue {
  background: rgba(56, 189, 248, 0.15);
  color: #0284c7;
}

.bento-card-title {
  margin: 0;
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--aubergine-dark);
}

.bento-card-subtitle {
  font-size: 0.8rem;
  color: var(--muted);
  font-weight: 600;
}

.bento-card-body p {
  margin: 0;
  color: var(--muted);
  font-size: 0.94rem;
  line-height: 1.6;
}

/* Visuels & Preuves */
.skill-visuals-panel {
  padding: 1.75rem 2rem;
  border-radius: 1.25rem;
  background: var(--surface-card);
  border: 1px solid var(--outline);
}

.visuals-header {
  display: flex;
  align-items: center;
  gap: 0.85rem;
  margin-bottom: 1.25rem;
}

.skill-images-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 1rem;
}

.skill-image-card {
  position: relative;
  border-radius: 12px;
  overflow: hidden;
  border: 1px solid var(--border);
  aspect-ratio: 16 / 10;
  margin: 0;
  cursor: pointer;
}

.skill-image-card img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.skill-image-card:hover img {
  transform: scale(1.04);
}

.skill-image-overlay {
  position: absolute;
  inset: 0;
  background: rgba(44, 0, 30, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  color: #ffffff;
  font-weight: 700;
  font-size: 0.9rem;
  opacity: 0;
  transition: opacity 0.2s ease;
}

.skill-image-card:hover .skill-image-overlay {
  opacity: 1;
}

/* Actions & Liens */
.skill-actions-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  padding: 1.25rem 2rem;
  border-radius: 1.25rem;
  background: var(--surface-card);
  border: 1px solid var(--outline);
  flex-wrap: wrap;
}

.actions-bar-title {
  font-size: 0.95rem;
  font-weight: 700;
  color: var(--aubergine-dark);
}

.actions-btns-row {
  display: flex;
  gap: 0.75rem;
  flex-wrap: wrap;
}

@media (max-width: 900px) {
  .skill-bento-grid {
    grid-template-columns: 1fr;
  }
  .bento-card--mastery {
    grid-column: span 1;
  }
}
</style>
