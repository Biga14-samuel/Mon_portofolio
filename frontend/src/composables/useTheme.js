import { ref, watchEffect } from 'vue';

const STORAGE_KEY = 'portfolio-theme';
const DARK = 'dark';
const LIGHT = 'light';

function getInitialTheme() {
  try {
    const stored = localStorage.getItem(STORAGE_KEY);
    if (stored === DARK || stored === LIGHT) return stored;
  } catch {}
  // Respect system preference
  if (typeof window !== 'undefined' && window.matchMedia('(prefers-color-scheme: dark)').matches) {
    return DARK;
  }
  return LIGHT;
}

const isDark = ref(getInitialTheme() === DARK);

// Apply theme to <html> whenever isDark changes
watchEffect(() => {
  const html = document.documentElement;
  if (isDark.value) {
    html.setAttribute('data-theme', DARK);
  } else {
    html.removeAttribute('data-theme');
  }
  try {
    localStorage.setItem(STORAGE_KEY, isDark.value ? DARK : LIGHT);
  } catch {}
});

function toggleTheme() {
  isDark.value = !isDark.value;
}

export function useTheme() {
  return { isDark, toggleTheme };
}
