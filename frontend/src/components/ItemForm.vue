<template>
  <form class="item-form" @submit.prevent="submit">
    <label>
      Type
      <select v-model="form.type" required>
        <option value="parcours">Parcours</option>
        <option value="competence">Competence</option>
        <option value="realisation">Realisation</option>
      </select>
    </label>

    <label>
      Tag / catégorie
      <select v-model="form.category" required>
        <option v-for="category in availableCategories" :key="category" :value="category">
          {{ category }}
        </option>
      </select>
      <small v-if="availableCategories.length === 0" style="color: var(--accent);">Aucun tag. Veuillez en ajouter via "Gérer les tags".</small>
    </label>

    <label>
      Titre
      <input v-model.trim="form.title" required maxlength="140" placeholder="Ex: Lead Developer" />
    </label>

    <label>
      Sous-titre / date
      <input v-model.trim="form.subtitle" required maxlength="180" placeholder="Ex: 2024 - Present" />
    </label>

    <label>
      Description
      <textarea v-model.trim="form.description" required minlength="10" rows="5" placeholder="Detail de l'element"></textarea>
    </label>

    <div class="form-row">
      <label>
        Lien GitHub (optionnel)
        <input v-model.trim="form.github_url" type="url" maxlength="500" placeholder="https://github.com/..." />
      </label>
      <label>
        Lien Démo (optionnel)
        <input v-model.trim="form.demo_url" type="url" maxlength="500" placeholder="https://..." />
      </label>
    </div>

    <div class="form-row">
      <label>
        Image de couverture (Optionnel)
        <ImageUploader v-model="form.image_url" @upload-error="handleUploadError" />
      </label>
      <label>
        Ordre d'affichage
        <input v-model.number="form.display_order" type="number" min="0" max="100000" />
      </label>
    </div>

    <label v-if="form.type === 'realisation'" class="checkbox-row">
      <input v-model="form.featured" type="checkbox" />
      <span>Mettre cette réalisation à la une</span>
    </label>

    <fieldset class="rich-content-fieldset">
      <legend>Contenu détaillé (Vue zoom / Fiche complète)</legend>

      <label>
        {{ form.type === 'realisation' ? 'Objectif du projet' : form.type === 'parcours' ? 'Missions & Objectifs' : 'Contexte & Utilisation' }}
        <textarea v-model="form.content.objective" rows="3" :placeholder="form.type === 'realisation' ? 'Pourquoi ce projet ?' : 'Quelles étaient vos responsabilités / le contexte ?'"></textarea>
      </label>

      <div class="form-row">
        <label>
          {{ form.type === 'realisation' ? 'Outils intégrés' : form.type === 'parcours' ? 'Technos / Outils utilisés' : 'Outils associés' }}
          <input v-model="form.content.tools" placeholder="Ex: Wazuh, Cisco, Linux (séparés par virgules)" />
        </label>
        <label>
          Media / Illustration / Certificat
          <ImageUploader v-model="form.content.architecture_image" @upload-error="handleUploadError" />
        </label>
      </div>

      <label>
        Galerie d'images / miniatures
        <MultiImageUploader v-model="form.content.gallery_images" @upload-error="handleUploadError" />
      </label>

      <label>
        {{ form.type === 'realisation' ? 'Architecture / Méthode' : form.type === 'parcours' ? 'Activités clés & Déroulement' : 'Détails techniques & Niveau' }}
        <textarea v-model="form.content.architecture" rows="4" placeholder="Explication détaillée..."></textarea>
      </label>

      <label>
        {{ form.type === 'realisation' ? "Flux d'alerte" : form.type === 'parcours' ? 'Méthodologie & Rôle' : "Cas d'usage / Projets liés" }}
        <textarea v-model="form.content.alert_flow" rows="3" placeholder="Informations complémentaires..."></textarea>
      </label>

      <label>
        {{ form.type === 'realisation' ? "Ce que j'ai appris" : form.type === 'parcours' ? 'Compétences développées' : 'Points forts & Maîtrise' }}
        <textarea v-model="form.content.lessons" rows="3" placeholder="Acquis techniques ou méthodologiques..."></textarea>
      </label>

      <label>
        {{ form.type === 'realisation' ? 'Impact du projet' : form.type === 'parcours' ? 'Bilan / Résultat' : 'Certifications / Attestation' }}
        <textarea v-model="form.content.impact" rows="2" placeholder="Résultat final ou validation..."></textarea>
      </label>
    </fieldset>

    <p v-if="error" class="form-error" role="alert">{{ error }}</p>
    <div class="form-actions">
      <button type="button" class="button secondary" @click="$emit('cancel')">Annuler</button>
      <button type="submit" class="button primary">{{ item?.id ? 'Mettre a jour' : 'Ajouter' }}</button>
    </div>
  </form>
</template>

<script setup>
import { reactive, ref, watch, computed, onMounted } from 'vue';
import { getTags } from '../services/api';
import ImageUploader from './ImageUploader.vue';
import MultiImageUploader from './MultiImageUploader.vue';

const props = defineProps({
  item: {
    type: Object,
    default: null,
  },
});

const emit = defineEmits(['submit', 'cancel']);
const error = ref('');
const allTags = ref([]);

function handleUploadError(msg) {
  error.value = msg;
}

function normalizeImageList(value) {
  if (Array.isArray(value)) {
    return value.map((entry) => String(entry).trim()).filter(Boolean);
  }
  if (typeof value === 'string') {
    return value
      .split(/[\n,;|]+/)
      .map((entry) => entry.trim())
      .filter(Boolean);
  }
  return [];
}

const form = reactive({
  type: 'parcours',
  category: '',
  featured: false,
  title: '',
  subtitle: '',
  description: '',
  github_url: '',
  demo_url: '',
  image_url: '',
  display_order: 0,
  content: {
    objective: '',
    architecture: '',
    architecture_image: '',
    gallery_images: [],
    alert_flow: '',
    tools: '',
    lessons: '',
    impact: '',
  },
});

onMounted(async () => {
  try {
    allTags.value = await getTags();
    if (!form.category && availableCategories.value.length > 0) {
      form.category = availableCategories.value[0];
    }
  } catch (e) {
    console.error('Erreur chargement tags', e);
  }
});

const availableCategories = computed(() => {
  return allTags.value.filter((t) => t.type === form.type).map((t) => t.name);
});

watch(
  () => props.item,
  (item) => {
    form.type = item?.type || 'parcours';
    form.category = item?.category || '';
    form.featured = Boolean(item?.featured);
    form.title = item?.title || '';
    form.subtitle = item?.subtitle || '';
    form.description = item?.description || '';
    form.github_url = item?.github_url || '';
    form.demo_url = item?.demo_url || '';
    form.image_url = item?.image_url || '';
    form.display_order = item?.display_order || 0;

    if (item?.content) {
      form.content = {
        objective: '',
        architecture: '',
        architecture_image: '',
        gallery_images: [],
        alert_flow: '',
        tools: '',
        lessons: '',
        impact: '',
        ...item.content,
      };
      form.content.gallery_images = normalizeImageList(form.content.gallery_images);
    } else {
      form.content = {
        objective: '',
        architecture: '',
        architecture_image: '',
        gallery_images: [],
        alert_flow: '',
        tools: '',
        lessons: '',
        impact: '',
      };
    }

    error.value = '';
  },
  { immediate: true },
);

function submit() {
  if (form.title.length < 2 || form.subtitle.length < 2 || form.description.length < 10) {
    error.value = 'Veuillez renseigner un titre, un sous-titre et une description suffisamment detailles.';
    return;
  }
  if (!form.category) {
    error.value = 'Veuillez sélectionner un tag / catégorie.';
    return;
  }

  emit('submit', {
    ...form,
    content: {
      ...form.content,
      gallery_images: normalizeImageList(form.content.gallery_images),
    },
  });
}

watch(
  () => form.type,
  (type) => {
    if (availableCategories.value.length > 0 && !availableCategories.value.includes(form.category)) {
      form.category = availableCategories.value[0];
    }
    if (type !== 'realisation') {
      form.featured = false;
    }
  },
);
</script>

<style scoped>
.form-row {
  display: flex;
  gap: 1rem;
}
.form-row label {
  flex: 1;
}
.rich-content-fieldset {
  border: 1px solid var(--border);
  padding: 1rem;
  border-radius: var(--radius-md);
  margin-top: 1rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
  background: var(--surface-1);
}
.rich-content-fieldset legend {
  padding: 0 0.5rem;
  font-weight: 600;
  color: var(--accent);
}
</style>
