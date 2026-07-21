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
        <option v-for="category in categoriesByType[form.type]" :key="category" :value="category">
          {{ category }}
        </option>
      </select>
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
    <label v-if="form.type === 'realisation'" class="checkbox-row">
      <input v-model="form.featured" type="checkbox" />
      <span>Mettre cette réalisation à la une</span>
    </label>
    <p v-if="error" class="form-error" role="alert">{{ error }}</p>
    <div class="form-actions">
      <button type="button" class="button secondary" @click="$emit('cancel')">Annuler</button>
      <button type="submit" class="button primary">{{ item?.id ? 'Mettre a jour' : 'Ajouter' }}</button>
    </div>
  </form>
</template>

<script setup>
import { reactive, ref, watch } from 'vue';

const props = defineProps({
  item: {
    type: Object,
    default: null,
  },
});

const emit = defineEmits(['submit', 'cancel']);
const error = ref('');
const form = reactive({
  type: 'parcours',
  category: 'Cursus',
  featured: false,
  title: '',
  subtitle: '',
  description: '',
});

const categoriesByType = {
  parcours: ['Cursus', 'Diplôme', 'Certification', 'Formation', 'Stage', 'Expérience professionnelle'],
  competence: [
    'Sécurité / Cybersécurité',
    'Administration réseau',
    'Administration système',
    'Méthodologie / Gestion de projet',
    'Base de données',
    'Compétences transversales',
    'Infographie',
    'Programmation web',
    'Automatisation / Scripting',
    'Virtualisation',
  ],
  realisation: [
    'Réseau sécurité',
    'Cybersécurité',
    'Fibre optique',
    'Maintenance',
    'Conception',
    'Administration système',
    'Programmation web',
    'Base de données',
  ],
};

watch(
  () => props.item,
  (item) => {
    form.type = item?.type || 'parcours';
    form.category = item?.category || categoriesByType[form.type][0];
    form.featured = Boolean(item?.featured);
    form.title = item?.title || '';
    form.subtitle = item?.subtitle || '';
    form.description = item?.description || '';
    error.value = '';
  },
  { immediate: true },
);

function submit() {
  if (form.title.length < 2 || form.subtitle.length < 2 || form.description.length < 10) {
    error.value = 'Veuillez renseigner un titre, un sous-titre et une description suffisamment detailles.';
    return;
  }

  emit('submit', { ...form });
}

watch(
  () => form.type,
  (type) => {
    if (!categoriesByType[type].includes(form.category)) {
      form.category = categoriesByType[type][0];
    }
    if (type !== 'realisation') {
      form.featured = false;
    }
  },
);
</script>
