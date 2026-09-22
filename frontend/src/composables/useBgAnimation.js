import { ref, watchEffect } from 'vue';

const STORAGE_KEY = 'portfolio-bg-animation';

function getInitialState() {
  try {
    const stored = localStorage.getItem(STORAGE_KEY);
    if (stored === 'false') return false;
  } catch {}
  return true; // activée par défaut
}

const bgEnabled = ref(getInitialState());

watchEffect(() => {
  try {
    localStorage.setItem(STORAGE_KEY, String(bgEnabled.value));
  } catch {}
});

function toggleBgAnimation() {
  bgEnabled.value = !bgEnabled.value;
}

export function useBgAnimation() {
  return { bgEnabled, toggleBgAnimation };
}
