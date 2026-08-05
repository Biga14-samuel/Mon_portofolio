<template>
  <main class="not-found">
    <section class="hero" style="min-height: 80vh; display: flex; align-items: center; justify-content: center; text-align: center;">
      <div class="hero-copy" style="align-items: center; text-align: center; max-width: 600px;">
        <div class="availability-card" aria-label="Erreur 404">
          <span class="availability-dot" aria-hidden="true" style="background: var(--ubuntu-orange);"></span>
          <strong>Erreur 404</strong>
          <span>Page introuvable</span>
        </div>
        
        <h1 class="wave-name" style="font-size: clamp(60px, 12vw, 120px); margin: 20px 0; color: var(--ubuntu-orange);">
          404
        </h1>
        
        <h2>Oups ! Cette page n'existe pas ou est indisponible.</h2>
        
        <p style="margin-bottom: 40px;">
          Il semble que le lien que vous avez suivi soit rompu, ou que la page ait été supprimée. 
          Ne vous inquiétez pas, vous pouvez retourner à l'accueil pour découvrir mon portfolio.
        </p>
        
        <div class="hero-actions" style="justify-content: center;">
          <a class="button button-pill primary" href="/" @click.prevent="goHome">
            <span class="icon-circle" style="transform: rotate(180deg); margin-right: 12px; margin-left: 0;"><ArrowRight :size="16" /></span>
            Retour à l'accueil
          </a>
        </div>
      </div>
    </section>
  </main>
</template>

<script setup>
import { ArrowRight } from 'lucide-vue-next';

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
