<template>
  <div class="project-gallery" aria-label="Galerie moodboard du projet">
    <!-- Heading -->
    <div class="project-gallery__heading">
      <span class="project-gallery__count">{{ images.length }} capture{{ images.length > 1 ? 's' : '' }}</span>
      <p class="project-gallery__hint">Survolez une image pour plus de détails · Cliquez pour agrandir</p>
    </div>

    <!-- Masonry grid -->
    <div class="project-gallery__masonry">
      <button
        v-for="(img, idx) in images"
        :key="img"
        class="project-gallery__tile"
        :class="`project-gallery__tile--${tileSize(idx)}`"
        type="button"
        :aria-label="`Agrandir la capture ${idx + 1}`"
        @click="$emit('open-lightbox', idx)"
      >
        <!-- Image -->
        <img
          :src="img"
          :alt="`Capture ${idx + 1} — ${projectTitle}`"
          class="project-gallery__img"
          loading="lazy"
          @error="handleImgError"
        />

        <!-- Overlay -->
        <div class="project-gallery__tile-overlay">
          <div class="project-gallery__tile-content">
            <p class="project-gallery__tile-title">{{ projectTitle }}</p>
            <div v-if="tools.length" class="project-gallery__tile-tools">
              <span v-for="t in tools.slice(0, 4)" :key="t" class="project-gallery__tool">{{ t }}</span>
            </div>
            <span class="project-gallery__tile-open">
              <ZoomIn :size="16" /> Agrandir
            </span>
          </div>
        </div>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ZoomIn } from 'lucide-vue-next';

const props = defineProps({
  images:       { type: Array,  required: true },
  projectTitle: { type: String, default: '' },
  tools:        { type: Array,  default: () => [] },
});

defineEmits(['open-lightbox']);

/**
 * Pattern de tailles pour les tuiles masonry :
 * Creates a varied, Pinterest-like layout
 */
const TILE_PATTERN = ['wide', 'tall', 'normal', 'normal', 'wide', 'normal', 'tall', 'normal'];

function tileSize(idx) {
  return TILE_PATTERN[idx % TILE_PATTERN.length];
}

function handleImgError(e) {
  e.target.style.opacity = '0.3';
}
</script>

<style scoped>
.project-gallery {
  width: 100%;
}

.project-gallery__heading {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 20px;
  padding-bottom: 14px;
  border-bottom: 1px solid var(--outline);
}

.project-gallery__count {
  font-size: 0.8rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--ubuntu-orange-dark);
}

.project-gallery__hint {
  font-size: 0.78rem;
  color: var(--muted);
  margin: 0;
}

/* Masonry grid */
.project-gallery__masonry {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
  grid-auto-rows: 140px;
  gap: 10px;
}

/* Tile base */
.project-gallery__tile {
  position: relative;
  border-radius: 14px;
  overflow: hidden;
  background: var(--surface-soft);
  border: none;
  padding: 0;
  cursor: zoom-in;
  transition: transform 0.3s cubic-bezier(0.23, 1, 0.32, 1), box-shadow 0.3s ease;
}

.project-gallery__tile:hover {
  transform: scale(1.03) translateY(-3px);
  box-shadow: 0 16px 40px rgba(119, 33, 111, 0.18);
  z-index: 2;
}

/* Tile size variants */
.project-gallery__tile--wide {
  grid-column: span 2;
}

.project-gallery__tile--tall {
  grid-row: span 2;
}

.project-gallery__tile--normal {
  grid-column: span 1;
  grid-row: span 1;
}

/* Image */
.project-gallery__img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
  transition: transform 0.4s ease;
}

.project-gallery__tile:hover .project-gallery__img {
  transform: scale(1.06);
}

/* Overlay */
.project-gallery__tile-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(
    160deg,
    rgba(44, 0, 30, 0.0) 30%,
    rgba(8, 3, 14, 0.88) 100%
  );
  display: flex;
  align-items: flex-end;
  padding: 14px;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.project-gallery__tile:hover .project-gallery__tile-overlay {
  opacity: 1;
}

.project-gallery__tile-content {
  color: #fff;
  width: 100%;
}

.project-gallery__tile-title {
  font-size: 0.78rem;
  font-weight: 700;
  margin: 0 0 6px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.project-gallery__tile-tools {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
  margin-bottom: 8px;
}

.project-gallery__tool {
  padding: 2px 7px;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.12);
  border: 1px solid rgba(255, 255, 255, 0.2);
  font-size: 0.66rem;
  font-weight: 600;
}

.project-gallery__tile-open {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  font-size: 0.73rem;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.75);
  text-transform: uppercase;
  letter-spacing: 0.06em;
}

@media (max-width: 640px) {
  .project-gallery__masonry {
    grid-template-columns: repeat(2, 1fr);
    grid-auto-rows: 110px;
  }
}
</style>
