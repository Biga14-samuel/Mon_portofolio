<template>
  <main class="not-found">
    <section class="hero" style="min-height: 80vh; display: flex; align-items: center; justify-content: center; text-align: center;">
      <div class="hero-copy" style="align-items: center; text-align: center; max-width: 600px;">
        <div class="availability-card" :aria-label="t('not_found.badge')">
          <span class="availability-dot" aria-hidden="true" style="background: var(--ubuntu-orange);"></span>
          <strong>{{ t('not_found.badge') }}</strong>
          <span>{{ t('not_found.not_found') }}</span>
        </div>
        
        <h1 class="wave-name" style="font-size: clamp(60px, 12vw, 120px); margin: 20px 0; color: var(--ubuntu-orange);">
          404
        </h1>
        
        <h2>{{ t('not_found.title') }}</h2>
        
        <p style="margin-bottom: 40px;">
          {{ t('not_found.body') }}
        </p>
        
        <div class="hero-actions" style="justify-content: center;">
          <a class="button button-pill primary" href="/" @click.prevent="goHome">
            <span class="icon-circle" style="transform: rotate(180deg); margin-right: 12px; margin-left: 0;"><ArrowRight :size="16" /></span>
            {{ t('not_found.home') }}
          </a>
        </div>
      </div>
    </section>
  </main>
</template>

<script setup>
import { ArrowRight } from 'lucide-vue-next';
import { useI18n } from '../i18n/index.js';
const { t } = useI18n();

const goHome = () => {
  window.location.href = '/';
};
</script>

<style scoped>
.not-found {
  width: 100%;
  animation: fadeIn 0.5s ease-out forwards;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>
