import { ref, computed } from 'vue';
import fr from './fr.js';
import en from './en.js';

const STORAGE_KEY = 'portfolio-locale';

function getInitialLocale() {
  // Le français est la langue officielle par défaut du portfolio
  try {
    const stored = localStorage.getItem(STORAGE_KEY);
    // Si l'utilisateur avait 'en' stocké lors d'anciens tests, on réinitialise à 'fr'
    if (stored === 'en') {
      localStorage.setItem(STORAGE_KEY, 'fr');
    }
  } catch {}
  return 'fr';
}

const locale = ref(getInitialLocale());
const messages = { fr, en };

/**
 * Resolve a dotted key like 'nav.about' from the active locale messages.
 * Supports {name} placeholder interpolation.
 */
function t(key, vars = {}) {
  const dict = messages[locale.value] || messages.fr;
  const parts = key.split('.');
  let value = dict;
  for (const part of parts) {
    if (value && typeof value === 'object' && part in value) {
      value = value[part];
    } else {
      // Fallback to French
      const fallback = messages.fr;
      let fb = fallback;
      for (const p of parts) {
        fb = fb && typeof fb === 'object' ? fb[p] : undefined;
      }
      value = fb ?? key;
      break;
    }
  }
  if (typeof value !== 'string') return key;
  // Interpolate {var} placeholders
  return value.replace(/\{(\w+)\}/g, (_, k) => vars[k] ?? `{${k}}`);
}

function toggleLocale() {
  locale.value = locale.value === 'fr' ? 'en' : 'fr';
  try {
    localStorage.setItem(STORAGE_KEY, locale.value);
  } catch {}
  // Update <html lang> attribute for accessibility
  document.documentElement.setAttribute('lang', locale.value);
}

// Initialize lang attribute
if (typeof document !== 'undefined') {
  document.documentElement.setAttribute('lang', locale.value);
}

export function useI18n() {
  return { locale, t, toggleLocale };
}
