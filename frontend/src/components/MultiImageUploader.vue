<template>
  <div
    class="multi-image-uploader"
    :class="{ 'is-dragover': isDragover, 'is-loading': loading }"
    @dragover.prevent="isDragover = true"
    @dragleave.prevent="isDragover = false"
    @drop.prevent="handleDrop"
    @click="triggerFileSelect"
  >
    <input
      ref="fileInput"
      type="file"
      class="hidden-input"
      accept="image/*"
      multiple
      @change="handleFileSelect"
    />

    <div class="multi-image-header">
      <div>
        <strong>Galerie d’images</strong>
        <p>Glissez plusieurs images ou cliquez pour en ajouter. Les vignettes servent de galerie dans le détail.</p>
      </div>
      <div class="multi-image-actions">
        <button v-if="normalizedImages.length" type="button" class="remove-all-button" :disabled="loading" @click.stop="removeAllImages">
          <Trash2 :size="15" aria-hidden="true" />
          Tout retirer
        </button>
        <button type="button" class="add-image-button" :disabled="loading" @click.stop="triggerFileSelect">
          <Plus :size="16" aria-hidden="true" />
          Ajouter
        </button>
      </div>
    </div>

    <div v-if="loading" class="multi-image-status">
      <div class="spinner"></div>
      <p>Envoi des images...</p>
    </div>

    <div v-else-if="normalizedImages.length" class="multi-image-grid">
      <div v-for="(image, index) in normalizedImages" :key="`${image}-${index}`" class="multi-image-item">
        <img :src="image" :alt="`Aperçu ${index + 1}`" @error="handleImgError" />
        <button type="button" class="remove-image-button" @click.stop="removeImage(index)" :aria-label="`Retirer l'image ${index + 1}`">
          <Trash2 :size="14" aria-hidden="true" />
        </button>
      </div>
    </div>

    <div v-else class="multi-image-empty">
      <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="upload-icon"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="17 8 12 3 7 8"></polyline><line x1="12" y1="3" x2="12" y2="15"></line></svg>
      <p>Glissez plusieurs images ici ou <strong>cliquez pour choisir</strong></p>
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue';
import { Plus, Trash2 } from 'lucide-vue-next';
import { uploadImage } from '../services/api';
import { authState } from '../store/auth';

const props = defineProps({
  modelValue: {
    type: Array,
    default: () => [],
  },
});

const emit = defineEmits(['update:modelValue', 'upload-error']);

const isDragover = ref(false);
const loading = ref(false);
const fileInput = ref(null);

const normalizedImages = computed(() => (Array.isArray(props.modelValue) ? props.modelValue.filter(Boolean) : []));

function resolvePreviewUrl(value) {
  if (!value) return '';
  if (value.startsWith('http') || value.startsWith('data:')) return value;
  return import.meta.env.VITE_API_URL
    ? `${import.meta.env.VITE_API_URL.replace(/\/$/, '')}${value}`
    : `http://localhost:8000${value}`;
}

const previewUrls = computed(() => normalizedImages.value.map(resolvePreviewUrl));

const FALLBACK_IMAGE = 'data:image/gif;base64,R0lGODlhAQABAIAAAAUEBAAAACwAAAAAAQABAAACAkQBADs=';

function handleImgError(e) {
  try {
    const img = e.target;
    if (!img.dataset.errored) {
      img.dataset.errored = '1';
      img.src = FALLBACK_IMAGE;
    }
  } catch {
    // noop
  }
}

function triggerFileSelect() {
  if (fileInput.value && !loading.value) {
    fileInput.value.click();
  }
}

async function handleDrop(e) {
  isDragover.value = false;
  const files = e.dataTransfer.files;
  if (files && files.length > 0) {
    await processFiles(Array.from(files));
  }
}

async function handleFileSelect(e) {
  const files = e.target.files;
  if (files && files.length > 0) {
    await processFiles(Array.from(files));
  }
  e.target.value = '';
}

function updateImages(nextImages) {
  emit('update:modelValue', nextImages.filter(Boolean));
}

async function processFiles(files) {
  const validFiles = files.filter((file) => file.type.startsWith('image/'));
  if (!validFiles.length) {
    emit('upload-error', 'Le fichier doit être une image.');
    return;
  }

  loading.value = true;
  try {
    const nextImages = [...normalizedImages.value];
    for (const file of validFiles) {
      const data = await uploadImage(file, authState.token);
      if (data?.url) nextImages.push(data.url);
    }
    updateImages(nextImages);
  } catch (error) {
    emit('upload-error', error.message || "Erreur lors de l'envoi de l'image.");
  } finally {
    loading.value = false;
  }
}

function removeImage(index) {
  const nextImages = [...normalizedImages.value];
  nextImages.splice(index, 1);
  updateImages(nextImages);
}

function removeAllImages() {
  updateImages([]);
  if (fileInput.value) {
    fileInput.value.value = '';
  }
}
</script>

<style scoped>
.multi-image-uploader {
  border: 2px dashed var(--border);
  border-radius: var(--radius-md);
  background: var(--surface-2);
  padding: 1rem;
  transition: all 0.2s;
  cursor: pointer;
}

.multi-image-uploader:hover,
.multi-image-uploader.is-dragover {
  border-color: var(--ubuntu-orange);
  background: var(--surface-card);
}

.hidden-input {
  display: none;
}

.multi-image-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 1rem;
  margin-bottom: 1rem;
}

.multi-image-header strong {
  display: block;
  color: var(--aubergine-dark);
  font-size: 0.98rem;
}

.multi-image-header p {
  margin: 0.35rem 0 0;
  color: var(--muted);
  font-size: 0.9rem;
  line-height: 1.45;
}

.multi-image-actions {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  flex-shrink: 0;
}

.remove-all-button {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  border: 1px solid rgba(220, 38, 38, 0.4);
  border-radius: 999px;
  background: rgba(220, 38, 38, 0.12);
  color: #dc2626;
  padding: 0.6rem 0.9rem;
  font-size: 0.85rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s ease;
}

.remove-all-button:hover {
  background: #dc2626;
  color: #ffffff;
}

.add-image-button {
  display: inline-flex;
  align-items: center;
  gap: 0.45rem;
  border: none;
  border-radius: 999px;
  background: var(--aubergine-dark);
  color: white;
  padding: 0.7rem 1rem;
  font-weight: 700;
  cursor: pointer;
}

.add-image-button:disabled,
.remove-all-button:disabled {
  opacity: 0.65;
  cursor: progress;
}

.multi-image-status,
.multi-image-empty {
  min-height: 140px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  gap: 0.8rem;
  text-align: center;
  color: var(--muted);
}

.multi-image-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(110px, 1fr));
  gap: 0.75rem;
}

.multi-image-item {
  position: relative;
  border-radius: 16px;
  overflow: hidden;
  border: 1px solid rgba(119, 33, 111, 0.14);
  background: #fff;
  box-shadow: 0 8px 20px rgba(44, 0, 30, 0.08);
}

.multi-image-item img {
  display: block;
  width: 100%;
  height: 120px;
  object-fit: cover;
}

.remove-image-button {
  position: absolute;
  top: 8px;
  right: 8px;
  width: 28px;
  height: 28px;
  border: none;
  border-radius: 50%;
  background: rgba(44, 0, 30, 0.82);
  color: #fff;
  display: grid;
  place-items: center;
  cursor: pointer;
}

.spinner {
  width: 30px;
  height: 30px;
  border: 3px solid rgba(233, 84, 32, 0.2);
  border-top-color: var(--ubuntu-orange);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>
