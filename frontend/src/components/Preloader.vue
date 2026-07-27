<template>
  <transition name="preloader">
    <div v-if="show" class="preloader-overlay">
      <div class="preloader-content">
        <div class="logo-text">
          <span class="brand-mark"></span>
          SAMNICK BIGA
        </div>
        <div class="progress-bar-container">
          <div class="progress-bar" :style="{ width: progress + '%' }"></div>
        </div>
      </div>
    </div>
  </transition>
</template>

<script setup>
import { ref, onMounted } from 'vue';

const show = ref(true);
const progress = ref(0);

onMounted(() => {
  // Simulate loading, wait for DOM and assets ideally, but we simulate a fast smooth load
  const interval = setInterval(() => {
    progress.value += Math.random() * 20;
    if (progress.value >= 100) {
      progress.value = 100;
      clearInterval(interval);
      setTimeout(() => {
        show.value = false;
        // Emit an event if needed so we know loading is done
        window.dispatchEvent(new Event('preloader-done'));
      }, 400); // Hold at 100% for a short moment
    }
  }, 100);
});
</script>

<style scoped>
.preloader-overlay {
  position: fixed;
  inset: 0;
  background: #111111; /* Dark theme preloader as requested by implied silence/premium feel */
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
  margin-bottom: 2rem;
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

.progress-bar-container {
  width: 240px;
  height: 3px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 4px;
  overflow: hidden;
}

.progress-bar {
  height: 100%;
  background: var(--ubuntu-orange);
  transition: width 0.15s ease-out;
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
