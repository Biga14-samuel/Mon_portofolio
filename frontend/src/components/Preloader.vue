<template>
  <transition name="preloader">
    <div v-if="show" class="preloader-overlay">
      <div class="preloader-content">
        <div class="logo-text">
          <span class="brand-mark"></span>
          SAMNICK BIGA
        </div>
        <div class="domino-loader">
          <div class="domino"></div>
          <div class="domino"></div>
          <div class="domino"></div>
          <div class="domino"></div>
          <div class="domino"></div>
          <div class="domino"></div>
        </div>
      </div>
    </div>
  </transition>
</template>

<script setup>
import { ref, onMounted } from 'vue';

const show = ref(true);

onMounted(() => {
  // Simulate loading, wait for DOM and assets ideally, but we simulate a fast smooth load
  setTimeout(() => {
    show.value = false;
    // Emit an event if needed so we know loading is done
    window.dispatchEvent(new Event('preloader-done'));
  }, 2200); // Wait enough time to show the domino animation
});
</script>

<style scoped>
.preloader-overlay {
  position: fixed;
  inset: 0;
  background: #111111; /* Dark theme preloader */
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
}

.logo-text {
  font-size: 1.8rem;
  font-weight: 700;
  letter-spacing: 0.15em;
  color: #ffffff;
  margin-bottom: 2.5rem;
  display: flex;
  align-items: center;
  gap: 12px;
}

.brand-mark {
  display: inline-block;
  width: 28px;
  height: 28px;
  background: var(--ubuntu-orange);
  border-radius: 50%;
}

/* Animation Domino */
.domino-loader {
  display: flex;
  gap: 12px;
  justify-content: center;
  align-items: center;
  height: 60px;
  padding-left: 20px; /* Offset for rotation */
}

.domino {
  width: 8px;
  height: 40px;
  background-color: var(--ubuntu-orange);
  border-radius: 2px;
  transform-origin: bottom right;
  animation: domino-fall 2.2s infinite ease-in-out;
  box-shadow: 1px 1px 3px rgba(0,0,0,0.3);
}

.domino:nth-child(1) { animation-delay: 0.0s; }
.domino:nth-child(2) { animation-delay: 0.15s; }
.domino:nth-child(3) { animation-delay: 0.3s; }
.domino:nth-child(4) { animation-delay: 0.45s; }
.domino:nth-child(5) { animation-delay: 0.6s; }
.domino:nth-child(6) { animation-delay: 0.75s; }

@keyframes domino-fall {
  0% {
    transform: rotate(0deg);
    opacity: 1;
  }
  20% {
    transform: rotate(72deg);
    opacity: 0.8;
  }
  60% {
    transform: rotate(72deg);
    opacity: 0.8;
  }
  80% {
    transform: rotate(0deg);
    opacity: 1;
  }
  100% {
    transform: rotate(0deg);
    opacity: 1;
  }
}

.preloader-enter-active,
.preloader-leave-active {
  transition: opacity 0.8s cubic-bezier(0.65, 0, 0.35, 1), transform 0.8s cubic-bezier(0.65, 0, 0.35, 1);
}

.preloader-leave-to {
  opacity: 0;
  transform: translateY(-5%);
}
</style>
