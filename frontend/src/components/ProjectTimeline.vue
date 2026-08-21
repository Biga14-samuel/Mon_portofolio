<template>
  <div class="soc-timeline" ref="timelineEl">
    <!-- Dashboard header -->
    <header class="soc-dashboard-header">
      <div class="soc-dashboard-header__left">
        <div class="soc-status-dot" aria-label="SOC actif"></div>
        <div>
          <span class="soc-dashboard-label">SOC Open-Source</span>
          <span class="soc-dashboard-subtitle">Incident Response Timeline</span>
        </div>
      </div>
      <div class="soc-dashboard-header__stats">
        <div class="soc-stat" v-for="stat in stats" :key="stat.label">
          <span class="soc-stat__value" :style="{ color: stat.color }">{{ stat.value }}</span>
          <span class="soc-stat__label">{{ stat.label }}</span>
        </div>
      </div>
    </header>

    <!-- Terminal prompt line -->
    <div class="soc-terminal-bar" aria-hidden="true">
      <span class="soc-terminal-bar__prompt">root@soc-lab:~#</span>
      <span class="soc-terminal-bar__cmd" ref="terminalCmd">incident_response --timeline --verbose</span>
      <span class="soc-terminal-bar__cursor">▋</span>
    </div>

    <!-- Timeline steps -->
    <div class="soc-timeline__track" role="list">
      <div
        v-for="(step, idx) in steps"
        :key="step.number"
        class="soc-step"
        :class="[
          `soc-step--${step.criticality || 'info'}`,
          { 'soc-step--visible': visibleSteps.has(idx) },
          { 'soc-step--active': activeStepIndex === idx },
        ]"
        :data-step-idx="idx"
        role="listitem"
        ref="stepEls"
      >
        <!-- Connector line -->
        <div class="soc-step__line" aria-hidden="true">
          <div class="soc-step__line-fill" :class="{ filled: visibleSteps.has(idx) }"></div>
        </div>

        <!-- Marker -->
        <button
          class="soc-step__marker"
          :class="`soc-step__marker--${step.criticality || 'info'}`"
          type="button"
          :aria-label="`Étape ${step.number} — ${step.title}`"
          @click="openStepDetail(step)"
        >
          <component :is="getStepIcon(step)" :size="16" />
        </button>

        <!-- Content card -->
        <div class="soc-step__card">
          <!-- Card header -->
          <div class="soc-step__card-header">
            <div class="soc-step__number-badge">{{ step.number }}</div>
            <div class="soc-step__card-meta">
              <span
                class="soc-step__criticality-badge"
                :class="`soc-step__criticality-badge--${step.criticality || 'info'}`"
              >
                {{ criticalityLabels[step.criticality || 'info'] }}
              </span>
              <span class="soc-step__tool-tag" v-if="step.tool">{{ step.tool }}</span>
            </div>
          </div>

          <h3 class="soc-step__title">{{ step.title }}</h3>

          <!-- Terminal-style body -->
          <div class="soc-step__terminal" aria-label="Détail technique">
            <div class="soc-step__terminal-header" aria-hidden="true">
              <span></span><span></span><span></span>
              <span class="soc-step__terminal-label">output</span>
            </div>
            <p class="soc-step__body" ref="stepBodyEls">{{ step.body }}</p>
          </div>

          <!-- Image -->
          <div v-if="step.images?.length" class="soc-step__screenshots">
            <button
              v-for="(img, imgIdx) in step.images.slice(0, 3)"
              :key="img"
              class="soc-step__screenshot"
              type="button"
              :aria-label="`Agrandir la capture ${imgIdx + 1} de l'étape ${step.number}`"
              @click.stop="$emit('open-lightbox', step.images, imgIdx, step.title)"
            >
              <img :src="img" :alt="`Capture ${imgIdx + 1} — ${step.title}`" @error="handleImgError" />
              <span class="soc-step__screenshot-zoom"><ZoomIn :size="14" /></span>
            </button>
          </div>

          <!-- Detail button -->
          <button
            class="soc-step__detail-btn"
            type="button"
            @click="openStepDetail(step)"
          >
            <FileText :size="14" /> Voir les logs et playbooks
          </button>
        </div>
      </div>
    </div>

    <!-- Step detail modal -->
    <Teleport to="body">
      <Transition name="soc-detail-fade">
        <div
          v-if="activeStep"
          class="soc-detail-backdrop"
          role="presentation"
          @click.self="activeStep = null"
        >
          <div class="soc-detail-modal" role="dialog" aria-modal="true" :aria-labelledby="`soc-detail-title-${activeStep.number}`">
            <div class="soc-detail-modal__header">
              <div>
                <span class="soc-detail-modal__number">{{ activeStep.number }}</span>
                <span
                  class="soc-step__criticality-badge"
                  :class="`soc-step__criticality-badge--${activeStep.criticality || 'info'}`"
                >{{ criticalityLabels[activeStep.criticality || 'info'] }}</span>
              </div>
              <button class="lightbox-close-btn" type="button" @click="activeStep = null" aria-label="Fermer">
                <X :size="18" />
              </button>
            </div>

            <h3 :id="`soc-detail-title-${activeStep.number}`" class="soc-detail-modal__title">
              {{ activeStep.title }}
            </h3>

            <div class="soc-detail-modal__terminal">
              <div class="soc-step__terminal-header" aria-hidden="true">
                <span></span><span></span><span></span>
                <span class="soc-step__terminal-label">logs / playbook</span>
              </div>
              <pre class="soc-detail-modal__logs">{{ activeStep.body }}</pre>
            </div>

            <div v-if="activeStep.images?.length" class="soc-detail-modal__gallery">
              <button
                v-for="(img, imgIdx) in activeStep.images"
                :key="img"
                class="soc-step__screenshot"
                type="button"
                @click="$emit('open-lightbox', activeStep.images, imgIdx, activeStep.title)"
              >
                <img :src="img" :alt="`Capture ${imgIdx + 1}`" @error="handleImgError" />
                <span class="soc-step__screenshot-zoom"><ZoomIn :size="14" /></span>
              </button>
            </div>
          </div>
        </div>
      </Transition>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue';
import {
  Shield, AlertTriangle, Activity, Zap, MessageSquare, FileText,
  Eye, Bug, Cpu, ZoomIn, X,
} from 'lucide-vue-next';

const props = defineProps({
  steps: {
    type: Array,
    default: () => [],
    // Each step: { number, title, body, criticality: 'info'|'warning'|'critical', tool, images: [] }
  },
});

defineEmits(['open-lightbox']);

const timelineEl = ref(null);
const stepEls = ref([]);
const activeStep = ref(null);
const activeStepIndex = ref(-1);
const visibleSteps = ref(new Set());

const criticalityLabels = {
  info:     'INFO',
  warning:  'WARN',
  critical: 'CRITICAL',
};

const stats = computed(() => {
  const total    = props.steps.length;
  const critical = props.steps.filter(s => s.criticality === 'critical').length;
  const warning  = props.steps.filter(s => s.criticality === 'warning').length;
  return [
    { label: 'Étapes', value: total,    color: 'var(--text)' },
    { label: 'Critiques', value: critical, color: '#e95420' },
    { label: 'Avertissements', value: warning, color: '#f59e0b' },
  ];
});

// Map step tools to icons
function getStepIcon(step) {
  const tool = (step.tool || step.title || '').toLowerCase();
  if (tool.includes('fim') || tool.includes('wazuh'))           return Shield;
  if (tool.includes('yara'))                                    return Bug;
  if (tool.includes('deepseek') || tool.includes('ai') || tool.includes('ia')) return Cpu;
  if (tool.includes('shuffle') || tool.includes('soar'))        return Zap;
  if (tool.includes('iris') || tool.includes('incident'))       return Activity;
  if (tool.includes('telegram') || tool.includes('notif'))      return MessageSquare;
  if (tool.includes('detect') || tool.includes('alerte'))       return AlertTriangle;
  return Eye;
}

function openStepDetail(step) {
  activeStep.value = step;
}

function handleImgError(e) {
  e.target.style.opacity = '0.3';
}

// Intersection observer to reveal steps
let observer;
onMounted(() => {
  observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const idx = parseInt(entry.target.dataset.stepIdx, 10);
        if (!isNaN(idx)) {
          setTimeout(() => {
            visibleSteps.value = new Set([...visibleSteps.value, idx]);
          }, idx * 120);
        }
      }
    });
  }, { threshold: 0.15, rootMargin: '0px 0px -60px 0px' });

  document.querySelectorAll('.soc-step').forEach(el => observer.observe(el));
});

onBeforeUnmount(() => {
  observer?.disconnect();
});
</script>

<style scoped>
/* === SOC DASHBOARD HEADER === */
.soc-timeline {
  width: 100%;
  font-family: 'Ubuntu Mono', 'Courier New', monospace;
}

.soc-dashboard-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 16px;
  padding: 20px 24px;
  border-radius: 16px;
  background: rgba(8, 3, 14, 0.96);
  border: 1px solid rgba(233, 84, 32, 0.22);
  margin-bottom: 16px;
  box-shadow: 0 0 40px rgba(233, 84, 32, 0.06), inset 0 1px 0 rgba(255,255,255,0.04);
}

.soc-dashboard-header__left {
  display: flex;
  align-items: center;
  gap: 14px;
}

.soc-status-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: #10b981;
  flex-shrink: 0;
  box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7);
  animation: soc-pulse 2s ease-out infinite;
}

@keyframes soc-pulse {
  0%   { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); }
  70%  { box-shadow: 0 0 0 10px rgba(16, 185, 129, 0); }
  100% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
}

.soc-dashboard-label {
  display: block;
  color: #fff;
  font-size: 0.95rem;
  font-weight: 700;
  letter-spacing: 0.04em;
}

.soc-dashboard-subtitle {
  display: block;
  color: rgba(255,255,255,0.45);
  font-size: 0.75rem;
  letter-spacing: 0.06em;
}

.soc-dashboard-header__stats {
  display: flex;
  gap: 24px;
}

.soc-stat {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
}

.soc-stat__value {
  font-size: 1.4rem;
  font-weight: 800;
  line-height: 1;
}

.soc-stat__label {
  font-size: 0.65rem;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: rgba(255,255,255,0.4);
  margin-top: 2px;
}

/* === TERMINAL BAR === */
.soc-terminal-bar {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 16px;
  border-radius: 10px;
  background: rgba(8, 3, 14, 0.8);
  border: 1px solid rgba(255,255,255,0.06);
  font-size: 0.82rem;
  margin-bottom: 28px;
  overflow: hidden;
}

.soc-terminal-bar__prompt {
  color: #10b981;
  font-weight: 700;
  white-space: nowrap;
}

.soc-terminal-bar__cmd {
  color: rgba(255,255,255,0.75);
  flex: 1;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.soc-terminal-bar__cursor {
  color: var(--ubuntu-orange);
  animation: blink 1s step-end infinite;
}

@keyframes blink {
  0%, 100% { opacity: 1; }
  50%       { opacity: 0; }
}

/* === TIMELINE TRACK === */
.soc-timeline__track {
  position: relative;
  display: flex;
  flex-direction: column;
  gap: 0;
}

/* === STEP === */
.soc-step {
  display: grid;
  grid-template-columns: 24px 52px 1fr;
  gap: 0 16px;
  align-items: start;
  opacity: 0;
  transform: translateY(30px) translateX(-10px);
  transition: opacity 0.5s ease, transform 0.5s cubic-bezier(0.23, 1, 0.32, 1);
}

.soc-step--visible {
  opacity: 1;
  transform: translateY(0) translateX(0);
}

/* Connector line (col 1) */
.soc-step__line {
  grid-column: 1;
  display: flex;
  justify-content: center;
  height: 100%;
  padding-top: 52px;
  padding-bottom: 0;
}

.soc-step__line-fill {
  width: 2px;
  min-height: 40px;
  background: var(--outline);
  border-radius: 2px;
  transition: background 0.5s ease;
}

.soc-step__line-fill.filled {
  background: linear-gradient(180deg, rgba(233,84,32,0.6), var(--outline));
}

.soc-step:last-child .soc-step__line {
  display: none;
}

/* Marker (col 2) */
.soc-step__marker {
  grid-column: 2;
  width: 48px;
  height: 48px;
  border-radius: 50%;
  display: grid;
  place-items: center;
  cursor: pointer;
  transition: transform 0.3s, box-shadow 0.3s;
  border: 2px solid;
  flex-shrink: 0;
  margin-top: 2px;
}

.soc-step__marker--info {
  background: rgba(0, 90, 156, 0.1);
  border-color: rgba(0, 90, 156, 0.35);
  color: #005a9c;
}

.soc-step__marker--warning {
  background: rgba(245, 158, 11, 0.1);
  border-color: rgba(245, 158, 11, 0.4);
  color: #f59e0b;
}

.soc-step__marker--critical {
  background: rgba(233, 84, 32, 0.1);
  border-color: rgba(233, 84, 32, 0.45);
  color: #e95420;
  box-shadow: 0 0 20px rgba(233, 84, 32, 0.12);
}

.soc-step__marker:hover {
  transform: scale(1.12);
  box-shadow: 0 8px 24px rgba(0,0,0,0.15);
}

/* Card (col 3) */
.soc-step__card {
  grid-column: 3;
  padding: 0 0 32px;
}

.soc-step__card-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 10px;
}

.soc-step__number-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  border-radius: 8px;
  background: var(--surface-soft);
  border: 1px solid var(--outline);
  font-size: 0.7rem;
  font-weight: 800;
  color: var(--muted);
  font-family: 'Ubuntu Mono', monospace;
}

.soc-step__card-meta {
  display: flex;
  align-items: center;
  gap: 6px;
  flex-wrap: wrap;
}

/* Criticality badges */
.soc-step__criticality-badge {
  display: inline-block;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 0.62rem;
  font-weight: 800;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  font-family: 'Ubuntu Mono', monospace;
}

.soc-step__criticality-badge--info {
  background: rgba(0, 90, 156, 0.1);
  color: #005a9c;
}

.soc-step__criticality-badge--warning {
  background: rgba(245, 158, 11, 0.12);
  color: #d97706;
}

.soc-step__criticality-badge--critical {
  background: rgba(233, 84, 32, 0.12);
  color: #e95420;
}

.soc-step__tool-tag {
  display: inline-block;
  padding: 2px 8px;
  border-radius: 4px;
  background: rgba(119, 33, 111, 0.08);
  color: var(--aubergine-dark);
  font-size: 0.68rem;
  font-weight: 600;
}

.soc-step__title {
  font-size: 1.05rem;
  font-weight: 700;
  color: var(--text);
  margin: 0 0 12px;
  line-height: 1.3;
  font-family: 'Ubuntu Sans', Ubuntu, system-ui, sans-serif;
}

/* Terminal block */
.soc-step__terminal {
  background: rgba(8, 3, 14, 0.94);
  border: 1px solid rgba(255,255,255,0.07);
  border-radius: 12px;
  overflow: hidden;
  margin-bottom: 12px;
}

.soc-step__terminal-header {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 14px;
  background: rgba(255,255,255,0.03);
  border-bottom: 1px solid rgba(255,255,255,0.05);
}

.soc-step__terminal-header span:nth-child(1) { width: 10px; height: 10px; border-radius: 50%; background: #ff5f57; }
.soc-step__terminal-header span:nth-child(2) { width: 10px; height: 10px; border-radius: 50%; background: #febc2e; }
.soc-step__terminal-header span:nth-child(3) { width: 10px; height: 10px; border-radius: 50%; background: #28c840; }

.soc-step__terminal-label {
  margin-left: 6px;
  font-size: 0.68rem;
  color: rgba(255,255,255,0.3);
  letter-spacing: 0.06em;
}

.soc-step__body {
  padding: 14px 16px;
  margin: 0;
  font-size: 0.82rem;
  color: rgba(255,255,255,0.75);
  line-height: 1.7;
  white-space: pre-wrap;
  font-family: 'Ubuntu Mono', 'Courier New', monospace;
  max-height: 200px;
  overflow-y: auto;
}

/* Screenshots */
.soc-step__screenshots {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  margin-bottom: 12px;
}

.soc-step__screenshot {
  position: relative;
  width: 100px;
  height: 68px;
  border-radius: 8px;
  overflow: hidden;
  border: 1px solid var(--outline);
  cursor: zoom-in;
  padding: 0;
  background: var(--surface-soft);
  transition: transform 0.2s, box-shadow 0.2s;
}

.soc-step__screenshot:hover {
  transform: scale(1.05);
  box-shadow: 0 8px 20px rgba(0,0,0,0.15);
}

.soc-step__screenshot img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.soc-step__screenshot-zoom {
  position: absolute;
  inset: 0;
  display: grid;
  place-items: center;
  background: rgba(8, 3, 14, 0.55);
  color: #fff;
  opacity: 0;
  transition: opacity 0.2s;
}

.soc-step__screenshot:hover .soc-step__screenshot-zoom {
  opacity: 1;
}

/* Detail button */
.soc-step__detail-btn {
  display: inline-flex;
  align-items: center;
  gap: 7px;
  padding: 6px 14px;
  border-radius: 8px;
  border: 1px solid var(--outline);
  background: transparent;
  color: var(--muted);
  font-size: 0.78rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s, color 0.2s, border-color 0.2s;
}

.soc-step__detail-btn:hover {
  background: rgba(119, 33, 111, 0.08);
  color: var(--aubergine-dark);
  border-color: rgba(119, 33, 111, 0.25);
}

/* === DETAIL MODAL === */
.soc-detail-backdrop {
  position: fixed;
  inset: 0;
  z-index: 4000;
  display: grid;
  place-items: center;
  padding: 24px;
  background: rgba(8, 3, 14, 0.75);
  backdrop-filter: blur(20px);
}

.soc-detail-modal {
  width: min(680px, 100%);
  max-height: 85vh;
  overflow-y: auto;
  border-radius: 20px;
  background: var(--surface-card);
  border: 1px solid rgba(233, 84, 32, 0.2);
  box-shadow: 0 40px 80px rgba(0,0,0,0.4);
  padding: 28px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.soc-detail-modal__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 8px;
}

.lightbox-close-btn {
  width: 36px;
  height: 36px;
  border: 1px solid var(--outline);
  border-radius: 50%;
  background: var(--surface-soft);
  color: var(--muted);
  cursor: pointer;
  display: grid;
  place-items: center;
  transition: background 0.2s, color 0.2s, transform 0.2s;
}

.lightbox-close-btn:hover {
  background: rgba(233,84,32,0.1);
  color: #e95420;
  transform: rotate(90deg);
}

.soc-detail-modal__number {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border-radius: 10px;
  background: var(--surface-soft);
  border: 1px solid var(--outline);
  font-size: 0.78rem;
  font-weight: 800;
  color: var(--muted);
  margin-right: 8px;
  font-family: 'Ubuntu Mono', monospace;
}

.soc-detail-modal__title {
  font-size: 1.2rem;
  font-weight: 700;
  margin: 0;
  color: var(--text);
}

.soc-detail-modal__terminal {
  border-radius: 12px;
  overflow: hidden;
  background: rgba(8, 3, 14, 0.96);
  border: 1px solid rgba(255,255,255,0.07);
}

.soc-detail-modal__logs {
  padding: 16px;
  margin: 0;
  font-size: 0.82rem;
  color: rgba(255,255,255,0.8);
  line-height: 1.7;
  white-space: pre-wrap;
  font-family: 'Ubuntu Mono', 'Courier New', monospace;
  max-height: 300px;
  overflow-y: auto;
}

.soc-detail-modal__gallery {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

/* Transitions */
.soc-detail-fade-enter-active,
.soc-detail-fade-leave-active {
  transition: opacity 0.25s ease;
}
.soc-detail-fade-enter-from,
.soc-detail-fade-leave-to {
  opacity: 0;
}

@media (max-width: 640px) {
  .soc-dashboard-header {
    flex-direction: column;
    gap: 16px;
  }

  .soc-step {
    grid-template-columns: 20px 40px 1fr;
    gap: 0 10px;
  }

  .soc-stat {
    align-items: flex-start;
  }
}
</style>
