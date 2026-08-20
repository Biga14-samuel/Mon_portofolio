<template>
  <article class="item-card bento-card" :class="item.type">
    <div v-if="imagesList.length" class="item-card__image-container">
      <Transition name="fade" mode="out-in">
        <img
          :key="imagesList[currentImageIndex]"
          :src="imagesList[currentImageIndex]"
          :alt="`Image de ${item.title}`"
          loading="lazy"
          @error="handleImageError"
        />
      </Transition>
      <div v-if="imagesList.length > 1" class="slideshow-dots">
        <span
          v-for="(_, idx) in imagesList"
          :key="idx"
          class="slideshow-dot"
          :class="{ active: idx === currentImageIndex }"
          @click.stop="currentImageIndex = idx"
        ></span>
      </div>
    </div>
    
    <div class="item-card__body">
      <div class="item-card__meta">
        <PillBadge :tone="item.type === 'realisation' ? 'orange' : 'aubergine'">{{ labels[item.type] }}</PillBadge>
        <PillBadge :tone="tagTone(props.item.category)">{{ sanitizedCategory }}</PillBadge>
        <span>{{ sanitizedSubtitle }}</span>
      </div>
      <h3>{{ sanitizedTitle }}</h3>
      <p>{{ sanitizedDescription }}</p>
      
      <div class="item-card__links" v-if="item.github_url || item.demo_url || pdfUrl">
        <a v-if="item.github_url" :href="item.github_url" target="_blank" rel="noreferrer" class="external-link">
          <Github :size="16" aria-hidden="true" /> Code
        </a>
        <a v-if="item.demo_url" :href="item.demo_url" target="_blank" rel="noreferrer" class="external-link">
          <ExternalLink :size="16" aria-hidden="true" /> Démo
        </a>
        <a v-if="pdfUrl" :href="pdfUrl" target="_blank" rel="noreferrer" class="external-link">
          <FileText :size="16" aria-hidden="true" /> PDF
        </a>
      </div>

      <button class="button button-pill" type="button" @click="$emit('view-case', item)">
        {{ item.type === 'realisation' ? "Voir l'étude de cas" : "Voir le détail" }}
        <span class="icon-circle"><ArrowUpRight :size="16" /></span>
      </button>
      
      <div v-if="editable" class="card-actions" aria-label="Actions administrateur">
        <button class="icon-button" type="button" :aria-label="`Modifier ${item.title}`" @click="$emit('edit', item)">
          <Pencil :size="18" aria-hidden="true" />
        </button>
        <button class="icon-button danger" type="button" :aria-label="`Supprimer ${item.title}`" @click="$emit('delete', item)">
          <Trash2 :size="18" aria-hidden="true" />
        </button>
      </div>
    </div>
  </article>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue';
import { Pencil, Trash2, Github, ExternalLink, ArrowUpRight, FileText } from 'lucide-vue-next';
import PillBadge from './PillBadge.vue';
import { tagTone } from '../services/tags';
import { stripEmojis } from '../utils/sanitize';
import { resolveAssetUrl } from '../services/api';

const props = defineProps({
  item: {
    type: Object,
    required: true,
  },
  editable: {
    type: Boolean,
    default: false,
  },
});

defineEmits(['edit', 'delete', 'view-case']);

const labels = {
  parcours: 'Parcours',
  competence: 'Competence',
  realisation: 'Realisation',
  blog: 'Blog',
};

const currentImageIndex = ref(0);
let timer = null;

const imagesList = computed(() => {
  if (!props.item.image_url) return [];
  return props.item.image_url.split(/[\n,]+/).map(resolveAssetUrl).filter(Boolean);
});

const sanitizedTitle = computed(() => stripEmojis(props.item.title));
const sanitizedSubtitle = computed(() => stripEmojis(props.item.subtitle));
const sanitizedDescription = computed(() => stripEmojis(props.item.description));
const sanitizedCategory = computed(() => stripEmojis(props.item.category));
const pdfUrl = computed(() => resolveAssetUrl(props.item.content?.pdf_url || ''));

onMounted(() => {
  if (imagesList.value.length > 1) {
    timer = setInterval(() => {
      currentImageIndex.value = (currentImageIndex.value + 1) % imagesList.value.length;
    }, 3200);
  }
});

onBeforeUnmount(() => {
  if (timer) clearInterval(timer);
});

const FALLBACK_IMAGE = 'data:image/gif;base64,R0lGODlhAQABAIAAAAUEBAAAACwAAAAAAQABAAACAkQBADs=';

function handleImageError(e) {
  try {
    const img = e.target;
    if (!img.dataset.errored) {
      img.dataset.errored = '1';
      img.src = FALLBACK_IMAGE;
    }
  } catch (err) {
    // noop
  }
}
</script>

<style scoped>
.item-card__image-container {
  position: relative;
  width: 100%;
  height: 180px;
  overflow: hidden;
  border-radius: var(--radius-sm);
  margin-bottom: 1rem;
}

.item-card__image-container img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.slideshow-dots {
  position: absolute;
  bottom: 8px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 6px;
  z-index: 2;
}

.slideshow-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.5);
  cursor: pointer;
  transition: background 0.3s, transform 0.3s;
}

.slideshow-dot.active {
  background: #ffffff;
  transform: scale(1.25);
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.4s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.item-card:hover .item-card__image-container img {
  transform: scale(1.05) rotate(5deg);
}

.item-card__links {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
  flex-wrap: wrap;
}

.external-link {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.9rem;
  color: var(--text-muted);
  text-decoration: none;
  font-weight: 500;
  transition: color 0.2s;
}

.external-link:hover {
  color: var(--accent);
}
</style>
