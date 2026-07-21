<template>
  <article class="item-card" :class="item.type">
    <div v-if="imagesList.length" class="item-card__image-container">
      <Transition name="fade" mode="out-in">
        <img :key="imagesList[currentImageIndex]" :src="imagesList[currentImageIndex]" :alt="`Image de ${item.title}`" loading="lazy" />
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
    <div class="item-card__meta">
      <PillBadge :tone="item.type === 'realisation' ? 'orange' : 'aubergine'">{{ labels[item.type] }}</PillBadge>
      <PillBadge :tone="tagTone(item.category)">{{ item.category }}</PillBadge>
      <span>{{ item.subtitle }}</span>
    </div>
    <h3>{{ item.title }}</h3>
    <p>{{ item.description }}</p>
    
    <div class="item-card__links" v-if="item.github_url || item.demo_url">
      <a v-if="item.github_url" :href="item.github_url" target="_blank" rel="noreferrer" class="external-link">
        <Github :size="16" aria-hidden="true" /> Code
      </a>
      <a v-if="item.demo_url" :href="item.demo_url" target="_blank" rel="noreferrer" class="external-link">
        <ExternalLink :size="16" aria-hidden="true" /> Démo
      </a>
    </div>

    <button class="case-link" type="button" @click="$emit('view-case', item)">
      {{ item.type === 'realisation' ? "Voir l'étude de cas" : "Voir le détail" }}
    </button>
    <div v-if="editable" class="card-actions" aria-label="Actions administrateur">
      <button class="icon-button" type="button" :aria-label="`Modifier ${item.title}`" @click="$emit('edit', item)">
        <Pencil :size="18" aria-hidden="true" />
      </button>
      <button class="icon-button danger" type="button" :aria-label="`Supprimer ${item.title}`" @click="$emit('delete', item)">
        <Trash2 :size="18" aria-hidden="true" />
      </button>
    </div>
  </article>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue';
import { Pencil, Trash2, Github, ExternalLink } from 'lucide-vue-next';
import PillBadge from './PillBadge.vue';
import { tagTone } from '../services/tags';

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
};

const currentImageIndex = ref(0);
let timer = null;

const imagesList = computed(() => {
  if (!props.item.image_url) return [];
  return props.item.image_url.split(/[\n,]+/).map((s) => s.trim()).filter(Boolean);
});

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
  transform: scale(1.05);
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
