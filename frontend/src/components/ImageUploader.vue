<template>
  <div 
    class="image-uploader" 
    :class="{ 'is-dragover': isDragover, 'is-loading': loading }"
    @dragover.prevent="isDragover = true"
    @dragleave.prevent="isDragover = false"
    @drop.prevent="handleDrop"
    @click="triggerFileSelect"
  >
    <input 
      type="file" 
      ref="fileInput" 
      class="hidden-input" 
      accept="image/*" 
      @change="handleFileSelect"
    />
    
    <div v-if="loading" class="uploader-content">
      <div class="spinner"></div>
      <p>Envoi en cours...</p>
    </div>
    <div v-else-if="modelValue" class="uploader-content has-image">
      <img :src="previewUrl" alt="Aperçu" class="preview-image" @error="handleImgError" />
      <button 
        type="button" 
        class="uploader-delete-btn" 
        title="Retirer complètement cette image" 
        aria-label="Retirer cette image"
        @click.stop="removeImage"
      >
        <Trash2 :size="15" aria-hidden="true" />
        <span>Supprimer</span>
      </button>
      <div class="uploader-overlay">
        <p>Cliquer pour changer d'image</p>
      </div>
    </div>
    <div v-else class="uploader-content empty">
      <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="upload-icon"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="17 8 12 3 7 8"></polyline><line x1="12" y1="3" x2="12" y2="15"></line></svg>
      <p>Glissez une image ici ou <strong>cliquez pour choisir</strong></p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { Trash2 } from 'lucide-vue-next';
import { uploadImage } from '../services/api';
import { authState } from '../store/auth';

const props = defineProps({
  modelValue: {
    type: String,
    default: ''
  }
});

const emit = defineEmits(['update:modelValue', 'upload-error']);

const isDragover = ref(false);
const loading = ref(false);
const fileInput = ref(null);

const previewUrl = computed(() => {
  if (!props.modelValue) return '';
  if (props.modelValue.startsWith('http') || props.modelValue.startsWith('data:')) return props.modelValue;
  // If it's a relative path from the backend
  return import.meta.env.VITE_API_URL 
    ? `${import.meta.env.VITE_API_URL.replace(/\/$/, '')}${props.modelValue}`
    : `http://localhost:8000${props.modelValue}`;
});

const FALLBACK_IMAGE = 'data:image/gif;base64,R0lGODlhAQABAIAAAAUEBAAAACwAAAAAAQABAAACAkQBADs=';

function handleImgError(e) {
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

function triggerFileSelect() {
  if (fileInput.value && !loading.value) {
    fileInput.value.click();
  }
}

async function handleDrop(e) {
  isDragover.value = false;
  const files = e.dataTransfer.files;
  if (files && files.length > 0) {
    await processFile(files[0]);
  }
}

async function handleFileSelect(e) {
  const files = e.target.files;
  if (files && files.length > 0) {
    await processFile(files[0]);
  }
  // Reset input so the same file can be selected again if needed
  e.target.value = '';
}

async function processFile(file) {
  if (!file.type.startsWith('image/')) {
    emit('upload-error', 'Le fichier doit être une image.');
    return;
  }
  
  loading.value = true;
  try {
    const data = await uploadImage(file, authState.token);
    if (data && data.url) {
      emit('update:modelValue', data.url);
    }
  } catch (error) {
    emit('upload-error', error.message || "Erreur lors de l'envoi de l'image.");
  } finally {
    loading.value = false;
  }
}

function removeImage() {
  emit('update:modelValue', '');
  if (fileInput.value) {
    fileInput.value.value = '';
  }
}
</script>

<style scoped>
.image-uploader {
  border: 2px dashed var(--border);
  border-radius: var(--radius-md);
  background: var(--surface-2);
  min-height: 140px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s;
  overflow: hidden;
  position: relative;
}

.image-uploader:hover, .image-uploader.is-dragover {
  border-color: var(--ubuntu-orange);
  background: var(--surface-card);
}

.hidden-input {
  display: none;
}

.uploader-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0.8rem;
  padding: 1.5rem;
  width: 100%;
  height: 100%;
  color: var(--muted);
  text-align: center;
}

.uploader-content.has-image {
  padding: 0;
  position: relative;
}

.upload-icon {
  color: var(--accent);
}

.preview-image {
  width: 100%;
  height: 140px;
  object-fit: cover;
  display: block;
}

.uploader-delete-btn {
  position: absolute;
  top: 8px;
  right: 8px;
  z-index: 10;
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 5px 10px;
  background: rgba(220, 38, 38, 0.9);
  color: #ffffff;
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 6px;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
  transition: all 0.2s ease;
}

.uploader-delete-btn:hover {
  background: rgb(239, 68, 68);
  transform: scale(1.05);
  box-shadow: 0 4px 16px rgba(239, 68, 68, 0.4);
}

.uploader-overlay {
  position: absolute;
  inset: 0;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.2s;
}

.uploader-overlay p {
  color: white;
  font-weight: 600;
  margin: 0;
}

.image-uploader:hover .uploader-overlay {
  opacity: 1;
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
