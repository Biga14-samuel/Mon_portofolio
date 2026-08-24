<template>
  <canvas ref="canvasRef" class="antigravity-canvas" aria-hidden="true"></canvas>
</template>

<script setup>
import { onMounted, onUnmounted, ref } from 'vue';

const canvasRef = ref(null);

// Palette officielle Ubuntu avec variantes douces et élégantes
const UBUNTU_COLORS = [
  '#E95420', // Ubuntu Orange
  '#77216F', // Canonical Aubergine
  '#5E2750', // Mid Aubergine
  '#2C001E', // Dark Aubergine
  '#FCA886', // Light Orange
  '#C48ABC', // Light Aubergine
  '#AEA79F', // Warm Grey
];

const CONFIG = {
  particleCount: 50,
  speedFactor: 0.7,
  gravity: -0.035, // Flottaison antigravité ascendante
  interactionRadius: 160,
  friction: 0.97,
};

let animationFrameId = null;
const spriteCache = {};

function getSprite(color, shapeType) {
  const key = `${color}-${shapeType}`;
  if (spriteCache[key]) return spriteCache[key];

  const size = 64;
  const center = size / 2;
  const drawSize = 28;

  const c = document.createElement('canvas');
  c.width = size;
  c.height = size;
  const cx = c.getContext('2d');

  // Ombre douce cuite dans le sprite pour accélération GPU
  cx.shadowColor = 'rgba(44, 0, 30, 0.12)';
  cx.shadowBlur = 12;
  cx.shadowOffsetX = 3;
  cx.shadowOffsetY = 4;
  cx.fillStyle = color;

  cx.translate(center, center);
  cx.beginPath();

  if (shapeType === 0) {
    // Cercle (forme privilégiée)
    cx.arc(0, 0, drawSize / 2, 0, Math.PI * 2);
  } else if (shapeType === 1) {
    // Carré adouci
    const r = drawSize / 2;
    cx.roundRect ? cx.roundRect(-r, -r, drawSize, drawSize, 6) : cx.rect(-r, -r, drawSize, drawSize);
  } else {
    // Triangle doux
    cx.moveTo(0, -drawSize / 2);
    cx.lineTo(drawSize / 2, drawSize / 2);
    cx.lineTo(-drawSize / 2, drawSize / 2);
    cx.closePath();
  }

  cx.fill();
  spriteCache[key] = c;
  return c;
}

class Particle {
  constructor(w, h, randomY = true) {
    this.init(w, h, randomY);
  }

  init(w, h, randomY = false) {
    this.x = Math.random() * w;
    this.y = randomY ? Math.random() * h : h + 40;
    this.visualSize = Math.random() * 16 + 8; // 8px à 24px
    this.vx = (Math.random() - 0.5) * 1.6 * CONFIG.speedFactor;
    this.vy = (Math.random() - 0.5) * 1.6 * CONFIG.speedFactor - Math.random() * 0.8;
    this.color = UBUNTU_COLORS[Math.floor(Math.random() * UBUNTU_COLORS.length)];
    this.rotation = Math.random() * Math.PI * 2;
    this.rotationSpeed = (Math.random() - 0.5) * 0.03;

    // 80% cercles, 10% carrés arrondis, 10% triangles
    const rand = Math.random();
    this.shapeType = rand < 0.8 ? 0 : rand < 0.9 ? 1 : 2;

    this.sprite = getSprite(this.color, this.shapeType);
    this.depth = Math.random() * 0.9 + 0.5; // Effet de profondeur 3D
  }

  update(w, h, mouseX, mouseY) {
    this.vy += CONFIG.gravity * 0.05 * this.depth;
    this.x += this.vx * this.depth;
    this.y += this.vy * this.depth;
    this.rotation += this.rotationSpeed;

    // Répulsion souris fluide
    const dx = this.x - mouseX;
    const dy = this.y - mouseY;
    const dist = Math.sqrt(dx * dx + dy * dy);

    if (dist < CONFIG.interactionRadius) {
      const force = (CONFIG.interactionRadius - dist) / CONFIG.interactionRadius;
      const angle = Math.atan2(dy, dx);
      const push = force * 3.5;
      this.vx += Math.cos(angle) * push;
      this.vy += Math.sin(angle) * push;
    }

    this.vx *= CONFIG.friction;
    this.vy *= CONFIG.friction;

    // Recyclage des limites d'écran
    if (this.x < -40) this.x = w + 40;
    if (this.x > w + 40) this.x = -40;
    if (this.y < -50) this.init(w, h, false);
  }

  draw(ctx) {
    ctx.save();
    ctx.translate(this.x, this.y);
    ctx.rotate(this.rotation);
    const scaleFactor = (this.visualSize * this.depth) / 28;
    const renderSize = 64 * scaleFactor;
    ctx.drawImage(this.sprite, -renderSize / 2, -renderSize / 2, renderSize, renderSize);
    ctx.restore();
  }
}

onMounted(() => {
  const canvas = canvasRef.value;
  if (!canvas) return;

  const ctx = canvas.getContext('2d', { alpha: true, desynchronized: true });
  let width = window.innerWidth;
  let height = window.innerHeight;

  function resize() {
    const dpr = Math.min(window.devicePixelRatio || 1, 2);
    width = window.innerWidth;
    height = window.innerHeight;
    canvas.width = width * dpr;
    canvas.height = height * dpr;
    ctx.scale(dpr, dpr);
  }

  window.addEventListener('resize', resize, { passive: true });
  resize();

  const particles = [];
  for (let i = 0; i < CONFIG.particleCount; i++) {
    particles.push(new Particle(width, height, true));
  }

  let mouseX = -1000;
  let mouseY = -1000;

  function handlePointerMove(e) {
    mouseX = e.clientX;
    mouseY = e.clientY;
  }

  window.addEventListener('pointermove', handlePointerMove, { passive: true });

  function animate() {
    ctx.clearRect(0, 0, width, height);
    for (let i = 0; i < particles.length; i++) {
      particles[i].update(width, height, mouseX, mouseY);
      particles[i].draw(ctx);
    }
    animationFrameId = requestAnimationFrame(animate);
  }

  animate();

  onUnmounted(() => {
    if (animationFrameId) cancelAnimationFrame(animationFrameId);
    window.removeEventListener('resize', resize);
    window.removeEventListener('pointermove', handlePointerMove);
  });
});
</script>

<style scoped>
.antigravity-canvas {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  pointer-events: none;
  z-index: 0;
  opacity: 0.72;
  will-change: transform;
}
</style>
