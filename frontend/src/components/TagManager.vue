<template>
  <div class="tag-manager">
    <div class="tag-filters">
      <button 
        v-for="type in types" 
        :key="type.value" 
        class="filter-pill small" 
        :class="{ active: selectedType === type.value }"
        @click="selectedType = type.value"
      >
        {{ type.label }}
      </button>
    </div>

    <form class="tag-form" @submit.prevent="addTag">
      <input v-model.trim="newTagName" placeholder="Nom du nouveau tag..." required maxlength="80" />
      <button class="button primary small" type="submit" :disabled="loading">Ajouter</button>
    </form>

    <p v-if="error" class="form-error" role="alert">{{ error }}</p>

    <ul class="tag-list">
      <li v-for="tag in filteredTags" :key="tag.id" class="tag-item">
        <PillBadge :tone="tagTone(tag.name)">{{ tag.name }}</PillBadge>
        <button class="icon-button danger small" type="button" @click="removeTag(tag)" aria-label="Supprimer ce tag" :disabled="loading">
          <Trash2 :size="16" aria-hidden="true" />
        </button>
      </li>
    </ul>
    <p v-if="filteredTags.length === 0 && !loading" class="empty-state">Aucun tag pour cette catégorie.</p>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { Trash2 } from 'lucide-vue-next';
import PillBadge from './PillBadge.vue';
import { tagTone } from '../services/tags';
import { getTags, createTag, deleteTag } from '../services/api';
import { authState, clearToken } from '../store/auth';

const props = defineProps({
  onSessionExpired: Function
});

const types = [
  { label: 'Parcours', value: 'parcours' },
  { label: 'Compétences', value: 'competence' },
  { label: 'Réalisations', value: 'realisation' },
];

const selectedType = ref('parcours');
const newTagName = ref('');
const tags = ref([]);
const loading = ref(false);
const error = ref('');

const filteredTags = computed(() => tags.value.filter(t => t.type === selectedType.value));

onMounted(() => {
  fetchTags();
});

async function fetchTags() {
  loading.value = true;
  error.value = '';
  try {
    tags.value = await getTags();
  } catch (err) {
    error.value = 'Erreur lors du chargement des tags.';
  } finally {
    loading.value = false;
  }
}

async function addTag() {
  if (!newTagName.value) return;
  loading.value = true;
  error.value = '';
  try {
    const newTag = await createTag({ type: selectedType.value, name: newTagName.value }, authState.token);
    tags.value.push(newTag);
    newTagName.value = '';
  } catch (err) {
    handleError(err);
  } finally {
    loading.value = false;
  }
}

async function removeTag(tag) {
  if (!confirm(`Voulez-vous supprimer le tag "${tag.name}" ?`)) return;
  loading.value = true;
  error.value = '';
  try {
    await deleteTag(tag.id, authState.token);
    tags.value = tags.value.filter(t => t.id !== tag.id);
  } catch (err) {
    handleError(err);
  } finally {
    loading.value = false;
  }
}

function handleError(err) {
  if (err.status === 401 || err.status === 403) {
    clearToken();
    if (props.onSessionExpired) props.onSessionExpired();
  } else if (err.status === 409) {
    error.value = err.message || 'Ce tag existe déjà ou est actuellement utilisé par un élément.';
  } else {
    error.value = err.message || 'Une erreur est survenue.';
  }
}
</script>

<style scoped>
.tag-manager {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.tag-filters {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.tag-form {
  display: flex;
  gap: 0.5rem;
}

.tag-form input {
  flex: 1;
}

.tag-form button {
  padding: 0 1rem;
}

.tag-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  max-height: 300px;
  overflow-y: auto;
}

.tag-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.5rem;
  background: var(--surface-2);
  border-radius: 6px;
}

.tag-item button {
  padding: 0.25rem;
}
</style>
