<template>
  <div class="dynamic-logo" @mouseenter="scramble" @click="scramble">
    <div class="shape" :class="[shapes[0], colors[0]]"></div>
    <div class="shape" :class="[shapes[1], colors[1]]"></div>
    <div class="shape" :class="[shapes[2], colors[2]]"></div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';

const shapeTypes = ['circle', 'square', 'rectangle', 'diamond', 'line', 'dot'];
const colorTypes = ['blue', 'red', 'yellow', 'green', 'black', 'grey'];

const shapes = ref(['circle', 'square', 'rectangle']);
const colors = ref(['blue', 'red', 'yellow']);

let intervalId;

const getRandomItem = (arr) => arr[Math.floor(Math.random() * arr.length)];

const scramble = () => {
  shapes.value = [
    getRandomItem(shapeTypes),
    getRandomItem(shapeTypes),
    getRandomItem(shapeTypes)
  ];
  colors.value = [
    getRandomItem(colorTypes),
    getRandomItem(colorTypes),
    getRandomItem(colorTypes)
  ];
};

onMounted(() => {
  intervalId = setInterval(scramble, 3500); // Change shapes every 3.5 seconds
});

onUnmounted(() => {
  clearInterval(intervalId);
});
</script>

<style scoped>
.dynamic-logo {
  display: flex;
  align-items: center;
  gap: 6px;
  height: 40px;
  cursor: pointer;
  position: relative;
  width: 90px;
  justify-content: center;
}

.shape {
  transition: all 0.7s cubic-bezier(0.34, 1.56, 0.64, 1);
  will-change: width, height, border-radius, transform, background-color;
  transform-origin: center;
  box-shadow: inset 0 0 0 1px rgba(0,0,0,0.05); /* very subtle inner line */
}

/* Shapes */
.circle {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  transform: rotate(0deg);
}

.square {
  width: 24px;
  height: 24px;
  border-radius: 6px;
  transform: rotate(0deg);
}

.rectangle {
  width: 12px;
  height: 32px;
  border-radius: 8px;
  transform: rotate(0deg);
}

.diamond {
  width: 20px;
  height: 20px;
  border-radius: 6px;
  transform: rotate(45deg);
}

.line {
  width: 28px;
  height: 6px;
  border-radius: 3px;
  transform: rotate(-15deg);
}

.dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  transform: rotate(0deg);
}

/* Colors (Bauhaus Palette) */
.blue { background-color: #0055A4; }
.red { background-color: #EF3340; }
.yellow { background-color: #FFD100; }
.green { background-color: #00965E; }
.black { background-color: #222222; }
.grey { background-color: #A0A0A0; }

/* Blending effect */
.dynamic-logo:hover .shape {
  mix-blend-mode: multiply;
  opacity: 0.9;
}
</style>
