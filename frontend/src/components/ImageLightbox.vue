<template>
  <Teleport to="body">
    <Transition name="lightbox-fade">
      <div
        v-if="modelValue"
        class="lightbox-backdrop"
        role="presentation"
        @click.self="close"
        @keydown.esc="close"
        @keydown.left="prev"
        @keydown.right="next"
        tabindex="-1"
        ref="backdropEl"
      >
        <!-- Close button -->
        <button class="lightbox-close" @click="close" aria-label="Fermer la lightbox" type="button">
          <X :size="20" />
        </button>

        <!-- Counter -->
        <div class="lightbox-counter" v-if="images.length > 1" aria-live="polite">
          {{ currentIndex + 1 }} / {{ images.length }}
        </div>

        <!-- Title -->
        <div class="lightbox-title-pill" v-if="title">
          <span>{{ title }}</span>
        </div>

        <!-- Main image stage -->
        <div class="lightbox-stage">
          <button
            v-if="images.length > 1"
            class="lightbox-nav lightbox-nav--prev"
            @click="prev"
            aria-label="Image précédente"
            type="button"
          >
            <ChevronLeft :size="28" />
          </button>

          <Transition :name="slideDir" mode="out-in">
            <div
              :key="currentIndex"
              class="lightbox-3d-frame"
              :style="frameStyle"
              @mousedown="startDrag"
              @touchstart.passive="startTouchDrag"
            >
              <img
                class="lightbox-image"
                :src="images[currentIndex]"
                :alt="`${title || 'Image'} — ${currentIndex + 1} / ${images.length}`"
                @error="handleImgError"
                @load="onImageLoad"
                draggable="false"
              />
              <div class="lightbox-image-glow" aria-hidden="true"></div>
            </div>
          </Transition>

          <button
            v-if="images.length > 1"
            class="lightbox-nav lightbox-nav--next"
            @click="next"
            aria-label="Image suivante"
            type="button"
          >
            <ChevronRight :size="28" />
          </button>
        </div>

        <!-- Thumbnails strip -->
        <div v-if="images.length > 1" class="lightbox-thumbs" role="tablist" :aria-label="`Miniatures — ${title}`">
          <button
            v-for="(img, idx) in images"
            :key="img"
            class="lightbox-thumb"
            :class="{ active: idx === currentIndex }"
            type="button"
            role="tab"
            :aria-selected="idx === currentIndex"
            :aria-label="`Voir l'image ${idx + 1}`"
            @click="goTo(idx)"
          >
            <img :src="img" :alt="`Miniature ${idx + 1}`" @error="handleImgError" />
          </button>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import { ref, watch, computed, nextTick, onMounted, onBeforeUnmount } from 'vue';
import { X, ChevronLeft, ChevronRight } from 'lucide-vue-next';

const props = defineProps({
  modelValue: { type: Boolean, default: false },
  images: { type: Array, default: () => [] },
  startIndex: { type: Number, default: 0 },
  title: { type: String, default: '' },
});

const emit = defineEmits(['update:modelValue']);

const backdropEl = ref(null);
const currentIndex = ref(0);
const slideDir = ref('slide-right');
const rotateX = ref(0);
const rotateY = ref(0);
const isDragging = ref(false);
let dragStartX = 0;
let dragStartY = 0;
let dragRotX = 0;
let dragRotY = 0;
let resetTimeout = null;

const frameStyle = computed(() => ({
  transform: `perspective(1200px) rotateX(${rotateX.value}deg) rotateY(${rotateY.value}deg)`,
  transition: isDragging.value ? 'none' : 'transform 0.5s cubic-bezier(0.23, 1, 0.32, 1)',
}));

watch(() => props.modelValue, (val) => {
  if (val) {
    currentIndex.value = props.startIndex ?? 0;
    nextTick(() => {
      backdropEl.value?.focus();
      document.body.style.overflow = 'hidden';
    });
  } else {
    document.body.style.overflow = '';
    rotateX.value = 0;
    rotateY.value = 0;
  }
});

watch(() => props.startIndex, (val) => {
  if (props.modelValue) currentIndex.value = val ?? 0;
});

function close() {
  emit('update:modelValue', false);
}

function prev() {
  if (!props.images.length) return;
  slideDir.value = 'slide-right';
  currentIndex.value = (currentIndex.value - 1 + props.images.length) % props.images.length;
  resetRotation();
}

function next() {
  if (!props.images.length) return;
  slideDir.value = 'slide-left';
  currentIndex.value = (currentIndex.value + 1) % props.images.length;
  resetRotation();
}

function goTo(idx) {
  slideDir.value = idx > currentIndex.value ? 'slide-left' : 'slide-right';
  currentIndex.value = idx;
  resetRotation();
}

function resetRotation() {
  rotateX.value = 0;
  rotateY.value = 0;
}

// Mouse drag rotation
function startDrag(e) {
  isDragging.value = true;
  dragStartX = e.clientX;
  dragStartY = e.clientY;
  dragRotX = rotateX.value;
  dragRotY = rotateY.value;

  const onMove = (ev) => {
    if (!isDragging.value) return;
    const dx = ev.clientX - dragStartX;
    const dy = ev.clientY - dragStartY;
    rotateY.value = Math.max(-18, Math.min(18, dragRotY + dx * 0.12));
    rotateX.value = Math.max(-12, Math.min(12, dragRotX - dy * 0.08));
  };

  const onUp = () => {
    isDragging.value = false;
    clearTimeout(resetTimeout);
    resetTimeout = setTimeout(resetRotation, 800);
    window.removeEventListener('mousemove', onMove);
    window.removeEventListener('mouseup', onUp);
  };

  window.addEventListener('mousemove', onMove);
  window.addEventListener('mouseup', onUp);
}

// Touch swipe + drag
let touchStartX = 0;
let touchStartY = 0;

function startTouchDrag(e) {
  if (!e.touches?.[0]) return;
  touchStartX = e.touches[0].clientX;
  touchStartY = e.touches[0].clientY;
  dragRotX = rotateX.value;
  dragRotY = rotateY.value;
  isDragging.value = true;

  const onTouchMove = (ev) => {
    if (!isDragging.value || !ev.touches?.[0]) return;
    const dx = ev.touches[0].clientX - touchStartX;
    const dy = ev.touches[0].clientY - touchStartY;
    rotateY.value = Math.max(-12, Math.min(12, dragRotY + dx * 0.08));
    rotateX.value = Math.max(-8, Math.min(8, dragRotX - dy * 0.06));
  };

  const onTouchEnd = (ev) => {
    isDragging.value = false;
    const dx = (ev.changedTouches?.[0]?.clientX ?? touchStartX) - touchStartX;
    if (Math.abs(dx) > 50) {
      dx < 0 ? next() : prev();
    } else {
      clearTimeout(resetTimeout);
      resetTimeout = setTimeout(resetRotation, 600);
    }
    window.removeEventListener('touchmove', onTouchMove);
    window.removeEventListener('touchend', onTouchEnd);
  };

  window.addEventListener('touchmove', onTouchMove, { passive: true });
  window.addEventListener('touchend', onTouchEnd, { passive: true });
}

function onImageLoad() {
  // could trigger a subtle animation
}

function handleImgError(e) {
  e.target.style.opacity = '0.3';
}

function handleKeydown(e) {
  if (!props.modelValue) return;
  if (e.key === 'Escape') { e.preventDefault(); close(); }
  if (e.key === 'ArrowLeft') { e.preventDefault(); prev(); }
  if (e.key === 'ArrowRight') { e.preventDefault(); next(); }
}

onMounted(() => {
  document.addEventListener('keydown', handleKeydown);
});
onBeforeUnmount(() => {
  document.removeEventListener('keydown', handleKeydown);
  document.body.style.overflow = '';
  if (resetTimeout) clearTimeout(resetTimeout);
});
</script>

<style scoped>
/* Backdrop */
.lightbox-backdrop {
  position: fixed;
  inset: 0;
  z-index: 3000;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 20px;
  padding: 24px 16px 16px;
  background: rgba(8, 3, 14, 0.88);
  backdrop-filter: blur(28px) saturate(1.4);
  -webkit-backdrop-filter: blur(28px) saturate(1.4);
  outline: none;
}

/* Close */
.lightbox-close {
  position: absolute;
  top: 20px;
  right: 20px;
  width: 44px;
  height: 44px;
  border: 1px solid rgba(255, 255, 255, 0.14);
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.08);
  color: rgba(255, 255, 255, 0.8);
  cursor: pointer;
  display: grid;
  place-items: center;
  transition: background 0.2s, color 0.2s, transform 0.2s;
  z-index: 10;
  backdrop-filter: blur(10px);
}
.lightbox-close:hover {
  background: rgba(233, 84, 32, 0.8);
  color: #fff;
  transform: rotate(90deg) scale(1.08);
}

/* Counter */
.lightbox-counter {
  position: absolute;
  top: 24px;
  left: 50%;
  transform: translateX(-50%);
  font-size: 0.8rem;
  color: rgba(255, 255, 255, 0.5);
  letter-spacing: 0.1em;
  font-weight: 500;
}

/* Title pill */
.lightbox-title-pill {
  position: absolute;
  bottom: 130px;
  left: 50%;
  transform: translateX(-50%);
  padding: 6px 16px;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(12px);
  color: rgba(255, 255, 255, 0.85);
  font-size: 0.82rem;
  font-weight: 600;
  white-space: nowrap;
  max-width: 90vw;
  overflow: hidden;
  text-overflow: ellipsis;
  pointer-events: none;
}

/* Stage */
.lightbox-stage {
  display: flex;
  align-items: center;
  gap: 20px;
  flex: 1;
  width: 100%;
  max-width: 1100px;
  min-height: 0;
}

/* 3D frame */
.lightbox-3d-frame {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: grab;
  user-select: none;
  will-change: transform;
  transform-style: preserve-3d;
}
.lightbox-3d-frame:active { cursor: grabbing; }

.lightbox-image {
  max-width: 100%;
  max-height: calc(100vh - 240px);
  object-fit: contain;
  border-radius: 18px;
  box-shadow:
    0 0 0 1px rgba(255, 255, 255, 0.06),
    0 40px 80px rgba(0, 0, 0, 0.7),
    0 0 120px rgba(119, 33, 111, 0.15);
  display: block;
  background: rgba(20, 10, 20, 0.5);
  pointer-events: none;
}

.lightbox-image-glow {
  position: absolute;
  inset: 10%;
  border-radius: 50%;
  background: radial-gradient(ellipse, rgba(196, 138, 188, 0.08) 0%, transparent 70%);
  pointer-events: none;
  filter: blur(40px);
}

/* Nav buttons */
.lightbox-nav {
  flex-shrink: 0;
  width: 52px;
  height: 52px;
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.06);
  color: rgba(255, 255, 255, 0.75);
  cursor: pointer;
  display: grid;
  place-items: center;
  transition: background 0.2s, color 0.2s, transform 0.2s, border-color 0.2s;
  backdrop-filter: blur(12px);
}
.lightbox-nav:hover {
  background: rgba(233, 84, 32, 0.7);
  border-color: rgba(233, 84, 32, 0.5);
  color: #fff;
  transform: scale(1.1);
}

/* Thumbs */
.lightbox-thumbs {
  display: flex;
  gap: 8px;
  overflow-x: auto;
  padding: 4px 0 8px;
  max-width: min(900px, 90vw);
  scrollbar-width: thin;
  scrollbar-color: rgba(255,255,255,0.15) transparent;
}

.lightbox-thumb {
  flex-shrink: 0;
  width: 72px;
  height: 50px;
  padding: 0;
  border: 2px solid transparent;
  border-radius: 10px;
  overflow: hidden;
  background: rgba(255, 255, 255, 0.06);
  cursor: pointer;
  transition: border-color 0.2s, transform 0.2s, box-shadow 0.2s;
  opacity: 0.55;
}
.lightbox-thumb:hover {
  opacity: 0.85;
  transform: translateY(-2px);
}
.lightbox-thumb.active {
  border-color: var(--ubuntu-orange);
  opacity: 1;
  box-shadow: 0 0 14px rgba(233, 84, 32, 0.4);
}
.lightbox-thumb img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

/* Transitions */
.lightbox-fade-enter-active,
.lightbox-fade-leave-active {
  transition: opacity 0.28s ease, backdrop-filter 0.28s ease;
}
.lightbox-fade-enter-from,
.lightbox-fade-leave-to {
  opacity: 0;
}

.slide-left-enter-active,
.slide-left-leave-active,
.slide-right-enter-active,
.slide-right-leave-active {
  transition: all 0.32s cubic-bezier(0.25, 0.46, 0.45, 0.94);
  position: absolute;
  width: 100%;
}
.slide-left-enter-from { opacity: 0; transform: perspective(800px) translateX(60px) rotateY(-8deg); }
.slide-left-leave-to   { opacity: 0; transform: perspective(800px) translateX(-60px) rotateY(8deg); }
.slide-right-enter-from { opacity: 0; transform: perspective(800px) translateX(-60px) rotateY(8deg); }
.slide-right-leave-to   { opacity: 0; transform: perspective(800px) translateX(60px) rotateY(-8deg); }

@media (max-width: 640px) {
  .lightbox-nav { width: 40px; height: 40px; }
  .lightbox-thumb { width: 56px; height: 40px; }
  .lightbox-title-pill { bottom: 110px; font-size: 0.75rem; }
}
</style>
