<template>
  <transition name="preloader">
    <div v-if="show" class="preloader-overlay">
      <div class="preloader-content">
        <div class="logo-text">
          <span class="brand-mark"></span>
          SAMNICK BIGA
        </div>

        <!-- Berceau de Newton — 5 boules couleurs Ubuntu -->
        <div class="newton-cradle">
          <div class="newton-cradle__dot"></div>
          <div class="newton-cradle__dot"></div>
          <div class="newton-cradle__dot"></div>
          <div class="newton-cradle__dot"></div>
          <div class="newton-cradle__dot"></div>
        </div>

        <p class="preloader-hint">Chargement…</p>
      </div>
    </div>
  </transition>
</template>

<script setup>
import { ref, onMounted } from 'vue';

const show = ref(true);

onMounted(() => {
  setTimeout(() => {
    show.value = false;
    window.dispatchEvent(new Event('preloader-done'));
  }, 2400);
});
</script>

<style scoped>
/* ── Fond ────────────────────────────────────────────────── */
.preloader-overlay {
  position: fixed;
  inset: 0;
  background: #2c001e; /* Ubuntu aubergine */
  z-index: 99999;
  display: flex;
  align-items: center;
  justify-content: center;
}

.preloader-content {
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2rem;
}

/* ── Logo texte ──────────────────────────────────────────── */
.logo-text {
  font-family: 'Ubuntu', 'Inter', sans-serif;
  font-size: 1.8rem;
  font-weight: 700;
  letter-spacing: 0.15em;
  color: #ffffff;
  display: flex;
  align-items: center;
  gap: 12px;
}

.brand-mark {
  display: inline-block;
  width: 28px;
  height: 28px;
  background: #e95420; /* Ubuntu Orange */
  border-radius: 50%;
  box-shadow: 0 0 18px #e9542066;
}

/* ── Texte sous le loader ───────────────────────────────── */
.preloader-hint {
  font-family: 'Ubuntu', 'Inter', sans-serif;
  font-size: 0.78rem;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  color: #aea79f; /* Ubuntu warm grey */
  margin: 0;
}

/* ══════════════════════════════════════════════════════════
   BERCEAU DE NEWTON — 5 boules
══════════════════════════════════════════════════════════ */
.newton-cradle {
  --nc-size: 82px;
  --nc-speed: 1.4s;
  /* Couleurs Ubuntu par position */
  --c1: #e95420; /* Orange vif  */
  --c2: #dd4814; /* Orange foncé */
  --c3: #aea79f; /* Warm grey   */
  --c4: #dd4814; /* Orange foncé */
  --c5: #e95420; /* Orange vif  */

  position: relative;
  display: flex;
  align-items: flex-start;
  justify-content: center;
  width: calc(var(--nc-size) * 1.1);
  height: calc(var(--nc-size) * 1.1);

  /* Barre supérieure du berceau */
  border-top: 3px solid #aea79f44;
  border-radius: 2px 2px 0 0;
}

/* Chaque pendule */
.newton-cradle__dot {
  position: relative;
  display: flex;
  flex-shrink: 0;
  align-items: center;
  height: 100%;
  width: 20%;
  transform-origin: center top;
}

/* Fil du pendule */
.newton-cradle__dot::before {
  content: '';
  position: absolute;
  top: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 1px;
  height: 75%;
  background: linear-gradient(to bottom, #aea79f66, #aea79f22);
}

/* La boule */
.newton-cradle__dot::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 80%;
  aspect-ratio: 1;
  border-radius: 50%;
  transition: background-color 0.3s ease;
}

/* Couleurs individuelles */
.newton-cradle__dot:nth-child(1)::after { background: var(--c1); box-shadow: 0 0 12px var(--c1)88; }
.newton-cradle__dot:nth-child(2)::after { background: var(--c2); box-shadow: 0 0 10px var(--c2)66; }
.newton-cradle__dot:nth-child(3)::after { background: var(--c3); box-shadow: 0 0  8px var(--c3)55; }
.newton-cradle__dot:nth-child(4)::after { background: var(--c4); box-shadow: 0 0 10px var(--c4)66; }
.newton-cradle__dot:nth-child(5)::after { background: var(--c5); box-shadow: 0 0 12px var(--c5)88; }

/* ── Animations pendulaires ──────────────────────────────── */
/* Boule de gauche (frappe depuis la gauche) */
.newton-cradle__dot:first-child {
  animation: nc-swing var(--nc-speed) linear infinite;
}

/* Boule de droite (rebondit vers la droite) */
.newton-cradle__dot:last-child {
  animation: nc-swing2 var(--nc-speed) linear infinite;
}

@keyframes nc-swing {
  0%   { transform: rotate(0deg);   animation-timing-function: ease-out; }
  25%  { transform: rotate(70deg);  animation-timing-function: ease-in; }
  50%  { transform: rotate(0deg);   animation-timing-function: linear; }
  100% { transform: rotate(0deg); }
}

@keyframes nc-swing2 {
  0%   { transform: rotate(0deg);   animation-timing-function: linear; }
  50%  { transform: rotate(0deg);   animation-timing-function: ease-out; }
  75%  { transform: rotate(-70deg); animation-timing-function: ease-in; }
  100% { transform: rotate(0deg); }
}

/* ── Transition de sortie ────────────────────────────────── */
.preloader-enter-active,
.preloader-leave-active {
  transition: opacity 0.9s cubic-bezier(0.65, 0, 0.35, 1),
              transform 0.9s cubic-bezier(0.65, 0, 0.35, 1);
}

.preloader-leave-to {
  opacity: 0;
  transform: translateY(-6%);
}
</style>
