import { ref, computed } from 'vue';
import fr from './fr.js';
import en from './en.js';

const STORAGE_KEY = 'portfolio-locale';

function getInitialLocale() {
  try {
    const stored = localStorage.getItem(STORAGE_KEY);
    if (stored === 'fr' || stored === 'en') return stored;
    // Detect browser language
    const lang = navigator.language || navigator.userLanguage || 'fr';
    return lang.startsWith('fr') ? 'fr' : 'en';
  } catch {
    return 'fr';
  }
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
