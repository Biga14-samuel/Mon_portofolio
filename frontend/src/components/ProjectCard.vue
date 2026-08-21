<template>
  <article
    class="project-card"
    :class="[`project-card--${cardSize}`, { 'project-card--featured': item.featured }]"
    @mouseenter="handleHover(true)"
    @mouseleave="handleHover(false)"
  >
    <!-- Image -->
    <div class="project-card__visual">
      <Transition name="card-img-fade" mode="out-in">
        <img
          :key="currentImageIndex"
          :src="imagesList[currentImageIndex] || fallback"
          :alt="`Visuel du projet ${sanitizedTitle}`"
          class="project-card__image"
          loading="lazy"
          @error="handleImageError"
        />
      </Transition>

      <!-- Overlay au survol -->
      <div class="project-card__overlay" aria-hidden="true">
        <div class="project-card__overlay-inner">
          <p class="project-card__overlay-desc">{{ sanitizedDescription }}</p>
          <div v-if="techBadges.length" class="project-card__overlay-tools">
            <span v-for="t in techBadges.slice(0, 5)" :key="t" class="project-card__tool-chip">{{ t }}</span>
          </div>
        </div>
      </div>

      <!-- Badge featured -->
      <div v-if="item.featured" class="project-card__featured-ribbon" aria-label="Projet à la une">
        <span>★ Projet vedette</span>
      </div>

      <!-- Criticality glow pour SOC -->
      <div v-if="isSocProject" class="project-card__soc-pulse" aria-hidden="true"></div>

      <!-- Dots slideshow -->
      <div v-if="imagesList.length > 1" class="project-card__dots" aria-hidden="true">
        <span
          v-for="(_, idx) in imagesList"
          :key="idx"
          class="project-card__dot"
          :class="{ active: idx === currentImageIndex }"
          @click.stop="currentImageIndex = idx"
        ></span>
      </div>
    </div>

    <!-- Body -->
    <div class="project-card__body">
      <!-- Meta badges -->
      <div class="project-card__meta">
        <span class="project-card__category-badge" :style="categoryBadgeStyle">
          {{ sanitizedCategory }}
        </span>
        <span v-if="sanitizedSubtitle" class="project-card__subtitle">{{ sanitizedSubtitle }}</span>
      </div>

      <h3 class="project-card__title">{{ sanitizedTitle }}</h3>

      <!-- Tech badges flottants -->
      <div v-if="techBadges.length" class="project-card__tech-badges" aria-label="Technologies utilisées">
        <span
          v-for="(tech, i) in techBadges.slice(0, 6)"
          :key="tech"
          class="tech-badge"
          :style="{ '--badge-delay': `${i * 60}ms` }"
        >{{ tech }}</span>
      </div>

      <!-- Actions -->
      <div class="project-card__actions">
        <div class="project-card__links" v-if="item.github_url || item.demo_url || pdfUrl">
          <a v-if="item.github_url" :href="item.github_url" target="_blank" rel="noreferrer" class="project-card__link" @click.stop>
            <Github :size="14" /> Code
          </a>
          <a v-if="item.demo_url" :href="item.demo_url" target="_blank" rel="noreferrer" class="project-card__link" @click.stop>
            <ExternalLink :size="14" /> Démo
          </a>
          <a v-if="pdfUrl" :href="pdfUrl" target="_blank" rel="noreferrer" class="project-card__link" @click.stop>
            <FileText :size="14" /> PDF
          </a>
        </div>

        <button
          class="project-card__cta"
          type="button"
          @click="$emit('view-case', item)"
        >
          <span>{{ isSocProject ? 'Voir la timeline SOC' : "Étude de cas" }}</span>
          <span class="project-card__cta-icon">
            <ArrowUpRight :size="14" />
          </span>
        </button>
      </div>

      <!-- Admin actions -->
      <div v-if="editable" class="project-card__admin" aria-label="Actions administrateur">
        <button class="icon-button" type="button" :aria-label="`Modifier ${sanitizedTitle}`" @click.stop="$emit('edit', item)">
          <Pencil :size="16" />
        </button>
        <button class="icon-button danger" type="button" :aria-label="`Supprimer ${sanitizedTitle}`" @click.stop="$emit('delete', item)">
          <Trash2 :size="16" />
        </button>
      </div>
    </div>
  </article>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue';
import { Pencil, Trash2, Github, ExternalLink, ArrowUpRight, FileText } from 'lucide-vue-next';
import { tagTone } from '../services/tags';
import { stripEmojis } from '../utils/sanitize';
import { resolveAssetUrl } from '../services/api';

const props = defineProps({
  item:     { type: Object, required: true },
  editable: { type: Boolean, default: false },
  cardSize: { type: String, default: 'medium' }, // 'small' | 'medium' | 'large'
});

defineEmits(['edit', 'delete', 'view-case']);

const fallback = 'data:image/gif;base64,R0lGODlhAQABAIAAAAUEBAAAACwAAAAAAQABAAACAkQBADs=';
const currentImageIndex = ref(0);
const hovered = ref(false);
let timer = null;

const imagesList = computed(() => {
  if (!props.item.image_url) return [];
  // Même séparateur que App.vue splitImageSources pour garantir la cohérence entre la card et la modal
  return props.item.image_url.split(/[\n,;|]+/).map(s => resolveAssetUrl(s.trim())).filter(Boolean);
});

const sanitizedTitle       = computed(() => stripEmojis(props.item.title));
const sanitizedSubtitle    = computed(() => stripEmojis(props.item.subtitle));
const sanitizedDescription = computed(() => stripEmojis(props.item.description));
const sanitizedCategory    = computed(() => stripEmojis(props.item.category));
const pdfUrl               = computed(() => resolveAssetUrl(props.item.content?.pdf_url || ''));

const isSocProject = computed(() => {
  const item = props.item;
  if (!item || item.type !== 'realisation') return false;
  const tools = item.content?.tools || '';
  const haystack = `${item.category || ''} ${item.title || ''} ${item.description || ''} ${tools}`.toLowerCase();
  return haystack.includes('soc') || haystack.includes('wazuh') || haystack.includes('siem');
});

// Tech badges: subtitle (comma-split) + content.tools
const techBadges = computed(() => {
  const parts = [];
  if (props.item.content?.tools) {
    parts.push(...props.item.content.tools.split(',').map(s => stripEmojis(s.trim())).filter(Boolean));
  }
  if (props.item.subtitle) {
    const subs = props.item.subtitle.split(',').map(s => stripEmojis(s.trim())).filter(Boolean);
    subs.forEach(s => { if (!parts.includes(s)) parts.push(s); });
  }
  return parts.slice(0, 8);
});

// Dynamic category badge color based on tagTone
const toneColors = {
  orange:    { bg: 'rgba(233, 84, 32, 0.12)', color: '#e95420' },
  aubergine: { bg: 'rgba(119, 33, 111, 0.12)', color: '#77216f' },
  blue:      { bg: 'rgba(0, 90, 156, 0.12)', color: '#005a9c' },
  green:     { bg: 'rgba(31, 122, 63, 0.12)', color: '#1f7a3f' },
  red:       { bg: 'rgba(176, 0, 75, 0.12)', color: '#b0004b' },
  teal:      { bg: 'rgba(0, 108, 112, 0.12)', color: '#006c70' },
  neutral:   { bg: 'rgba(110, 94, 91, 0.12)', color: '#6e5e5b' },
};

const categoryBadgeStyle = computed(() => {
  const tone = tagTone(props.item.category) || 'neutral';
  const c = toneColors[tone] || toneColors.neutral;
  return { background: c.bg, color: c.color };
});

function handleHover(val) {
  hovered.value = val;
}

function handleImageError(e) {
  if (!e.target.dataset.errored) {
    e.target.dataset.errored = '1';
    e.target.src = fallback;
  }
}

onMounted(() => {
  if (imagesList.value.length > 1) {
    timer = setInterval(() => {
      currentImageIndex.value = (currentImageIndex.value + 1) % imagesList.value.length;
    }, 3800);
  }
});

onBeforeUnmount(() => {
  if (timer) clearInterval(timer);
});
</script>

<style scoped>
/* ===========================
   PROJECT CARD — IMMERSIVE
   =========================== */
.project-card {
  position: relative;
  border-radius: 20px;
  background: var(--surface-card);
  border: 1px solid var(--outline);
  overflow: hidden;
  display: flex;
  flex-direction: column;
  transition:
    transform 0.38s cubic-bezier(0.23, 1, 0.32, 1),
    box-shadow 0.38s cubic-bezier(0.23, 1, 0.32, 1),
    border-color 0.3s ease;
  cursor: default;
  break-inside: avoid;
  margin-bottom: 0;
}

.project-card:hover {
  transform: translateY(-6px) scale(1.012);
  box-shadow: 0 24px 60px rgba(119, 33, 111, 0.16), 0 0 0 1px rgba(233, 84, 32, 0.18);
  border-color: rgba(233, 84, 32, 0.25);
}

.project-card--featured {
  border-color: rgba(233, 84, 32, 0.35);
  box-shadow: 0 8px 32px rgba(233, 84, 32, 0.1);
}

/* ---- Visual ---- */
.project-card__visual {
  position: relative;
  width: 100%;
  overflow: hidden;
  background: var(--surface-soft);
}

.project-card--small  .project-card__visual { height: 160px; }
.project-card--medium .project-card__visual { height: 220px; }
.project-card--large  .project-card__visual { height: 300px; }

.project-card__image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
  transition: transform 0.55s cubic-bezier(0.23, 1, 0.32, 1);
}

.project-card:hover .project-card__image {
  transform: scale(1.07);
}

/* ---- Overlay ---- */
.project-card__overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(
    160deg,
    rgba(44, 0, 30, 0.72) 0%,
    rgba(8, 3, 14, 0.86) 100%
  );
  display: flex;
  align-items: flex-end;
  padding: 20px;
  opacity: 0;
  transition: opacity 0.35s ease;
  backdrop-filter: blur(3px);
}

.project-card:hover .project-card__overlay {
  opacity: 1;
}

.project-card__overlay-inner {
  color: #fff;
}

.project-card__overlay-desc {
  font-size: 0.85rem;
  line-height: 1.5;
  margin: 0 0 10px;
  opacity: 0.9;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.project-card__overlay-tools {
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
}

.project-card__tool-chip {
  padding: 3px 9px;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.14);
  border: 1px solid rgba(255, 255, 255, 0.22);
  font-size: 0.72rem;
  font-weight: 600;
  color: #fff;
  letter-spacing: 0.03em;
  backdrop-filter: blur(8px);
}

/* ---- Featured ribbon ---- */
.project-card__featured-ribbon {
  position: absolute;
  top: 14px;
  left: -1px;
  padding: 4px 12px 4px 14px;
  background: linear-gradient(90deg, #e95420, #fca886);
  color: #fff;
  font-size: 0.72rem;
  font-weight: 800;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  border-radius: 0 999px 999px 0;
  box-shadow: 0 4px 12px rgba(233, 84, 32, 0.4);
}

/* ---- SOC Pulse ---- */
.project-card__soc-pulse {
  position: absolute;
  top: 12px;
  right: 12px;
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: #e95420;
  box-shadow: 0 0 0 0 rgba(233, 84, 32, 0.7);
  animation: soc-pulse 2s ease-out infinite;
}

@keyframes soc-pulse {
  0%   { box-shadow: 0 0 0 0 rgba(233, 84, 32, 0.7); }
  70%  { box-shadow: 0 0 0 10px rgba(233, 84, 32, 0); }
  100% { box-shadow: 0 0 0 0 rgba(233, 84, 32, 0); }
}

/* ---- Dots ---- */
.project-card__dots {
  position: absolute;
  bottom: 10px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 5px;
  z-index: 2;
}

.project-card__dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: rgba(255,255,255,0.45);
  cursor: pointer;
  transition: background 0.25s, transform 0.25s;
}

.project-card__dot.active {
  background: #fff;
  transform: scale(1.4);
}

/* ---- Body ---- */
.project-card__body {
  padding: 18px 20px 20px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  flex: 1;
}

/* ---- Meta ---- */
.project-card__meta {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 7px;
}

.project-card__category-badge {
  display: inline-block;
  padding: 3px 10px;
  border-radius: 999px;
  font-size: 0.72rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.07em;
}

.project-card__subtitle {
  font-size: 0.78rem;
  color: var(--muted);
  font-weight: 500;
}

/* ---- Title ---- */
.project-card__title {
  margin: 0;
  font-size: 1.05rem;
  font-weight: 700;
  color: var(--text);
  line-height: 1.35;
  letter-spacing: -0.01em;
}

/* ---- Tech badges ---- */
.project-card__tech-badges {
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
}

.tech-badge {
  display: inline-block;
  padding: 3px 10px;
  border-radius: 999px;
  background: var(--surface-soft);
  border: 1px solid var(--outline);
  font-size: 0.72rem;
  font-weight: 600;
  color: var(--muted);
  letter-spacing: 0.03em;
  transition: transform 0.2s ease, background 0.2s, color 0.2s, box-shadow 0.2s;
  animation: badge-float-in 0.4s ease both;
  animation-delay: var(--badge-delay, 0ms);
}

.project-card:hover .tech-badge {
  transform: translateY(-2px);
  background: rgba(119, 33, 111, 0.07);
  color: var(--aubergine-dark);
  box-shadow: 0 4px 10px rgba(119, 33, 111, 0.08);
}

@keyframes badge-float-in {
  from { opacity: 0; transform: translateY(6px); }
  to   { opacity: 1; transform: translateY(0); }
}

/* ---- Actions ---- */
.project-card__actions {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 4px;
}

.project-card__links {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.project-card__link {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  font-size: 0.8rem;
  font-weight: 500;
  color: var(--muted);
  text-decoration: none;
  transition: color 0.2s;
}
.project-card__link:hover { color: var(--ubuntu-orange-dark); }

/* ---- CTA ---- */
.project-card__cta {
  display: inline-flex;
  align-items: center;
  gap: 7px;
  padding: 7px 14px;
  border-radius: 999px;
  border: 1.5px solid var(--outline);
  background: transparent;
  color: var(--text);
  font-size: 0.82rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.22s, border-color 0.22s, color 0.22s, transform 0.22s;
  white-space: nowrap;
}

.project-card__cta:hover {
  background: var(--ubuntu-orange-dark);
  border-color: var(--ubuntu-orange-dark);
  color: #fff;
  transform: translateY(-1px);
}

.project-card__cta-icon {
  width: 22px;
  height: 22px;
  border-radius: 50%;
  background: rgba(233, 84, 32, 0.12);
  display: grid;
  place-items: center;
  transition: background 0.2s;
}

.project-card__cta:hover .project-card__cta-icon {
  background: rgba(255,255,255,0.2);
}

/* ---- Admin ---- */
.project-card__admin {
  display: flex;
  gap: 8px;
  margin-top: 4px;
  padding-top: 12px;
  border-top: 1px solid var(--outline);
}

/* ---- Transitions ---- */
.card-img-fade-enter-active,
.card-img-fade-leave-active {
  transition: opacity 0.45s ease;
}
.card-img-fade-enter-from,
.card-img-fade-leave-to {
  opacity: 0;
}
</style>
