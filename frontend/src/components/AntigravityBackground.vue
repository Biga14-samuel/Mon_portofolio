<template>
  <canvas ref="canvasRef" class="particle-canvas" aria-hidden="true"></canvas>
</template>

<script setup>
import { onMounted, onUnmounted, ref } from 'vue';

// ── Props ────────────────────────────────────────────────────────────────────
const props = defineProps({
  density: {
    type: Number,
    default: 1.0,
  },
});

// ── Palette Ubuntu pondérée ───────────────────────────────────────────────────
// Poids : Orange 30%, Orange clair 15%, Aubergine foncée 20%, Aubergine 25%, Gris 10%
const PALETTE_WEIGHTED = [];
(function buildPalette() {
  const entries = [
    { color: '#E95420', weight: 30 }, // Orange principal
    { color: '#F7A16E', weight: 15 }, // Orange clair
    { color: '#2C001E', weight: 20 }, // Aubergine foncée
    { color: '#77216F', weight: 25 }, // Aubergine
    { color: '#AEA79F', weight: 10 }, // Gris chaud
  ];
  for (const { color, weight } of entries) {
    for (let i = 0; i < weight; i++) PALETTE_WEIGHTED.push(color);
  }
})();

function pickColor() {
  return PALETTE_WEIGHTED[Math.floor(Math.random() * PALETTE_WEIGHTED.length)];
}

// ── Paramètres ────────────────────────────────────────────────────────────────
const MOUSE_RADIUS = 150;
const REPULSION_FORCE = 0.04;
const RETURN_SPEED = 0.06; // fraction vers laquelle revient la vitesse naturelle

// ── Classe Particule ─────────────────────────────────────────────────────────
class Stick {
  constructor(w, h, edgeBias = false) {
    this._init(w, h, edgeBias);
  }

  _init(w, h, edgeBias = false) {
    // Distribution avec légère surreprésentation sur les bords/coins
    if (edgeBias && Math.random() < 0.25) {
      // Placer sur un bord ou un coin
      const side = Math.floor(Math.random() * 4);
      const margin = 80;
      if (side === 0) { this.x = Math.random() * w; this.y = Math.random() * margin; }
      else if (side === 1) { this.x = w - Math.random() * margin; this.y = Math.random() * h; }
      else if (side === 2) { this.x = Math.random() * w; this.y = h - Math.random() * margin; }
      else { this.x = Math.random() * margin; this.y = Math.random() * h; }
    } else {
      this.x = Math.random() * w;
      this.y = Math.random() * h;
    }

    // Vitesse de dérive naturelle
    const angle = Math.random() * Math.PI * 2;
    const speed = 0.15 + Math.random() * 0.35; // 0.15 → 0.50 px/frame
    this.vxNatural = Math.cos(angle) * speed;
    this.vyNatural = Math.sin(angle) * speed;

    // Vélocité effective (peut être perturbée par la souris)
    this.vx = this.vxNatural;
    this.vy = this.vyNatural;

    // Forme : bâtonnet court
    this.length = 6 + Math.random() * 8;          // 6–14 px
    this.lineWidth = 1.5 + Math.random() * 1.0;   // 1.5–2.5 px
    this.rotation = Math.random() * Math.PI * 2;   // 0–360°
    this.dRotation = (Math.random() - 0.5) * 0.006; // ±0.3°/frame en radians

    // Couleur & opacité — fixées à la création
    this.color = pickColor();
    this.alpha = 0.35 + Math.random() * 0.50;      // 0.35–0.85
  }

  update(w, h, mx, my) {
    // Légère variation de rotation
    this.rotation += this.dRotation;

    // Répulsion souris
    const dx = this.x - mx;
    const dy = this.y - my;
    const dist = Math.sqrt(dx * dx + dy * dy);

    if (dist < MOUSE_RADIUS && dist > 0) {
      const t = 1 - dist / MOUSE_RADIUS;
      const force = t * REPULSION_FORCE;
      this.vx += (dx / dist) * force;
      this.vy += (dy / dist) * force;
    }

    // Retour progressif vers la trajectoire naturelle
    this.vx += (this.vxNatural - this.vx) * RETURN_SPEED;
    this.vy += (this.vyNatural - this.vy) * RETURN_SPEED;

    // Déplacement
    this.x += this.vx;
    this.y += this.vy;

    // Wrap-around (côté opposé)
    if (this.x < -20) this.x = w + 20;
    else if (this.x > w + 20) this.x = -20;
    if (this.y < -20) this.y = h + 20;
    else if (this.y > h + 20) this.y = -20;
  }

  draw(ctx) {
    const half = this.length / 2;
    ctx.save();
    ctx.translate(this.x, this.y);
    ctx.rotate(this.rotation);
    ctx.globalAlpha = this.alpha;
    ctx.strokeStyle = this.color;
    ctx.lineWidth = this.lineWidth;
    ctx.lineCap = 'round';
    ctx.beginPath();
    ctx.moveTo(-half, 0);
    ctx.lineTo(half, 0);
    ctx.stroke();
    ctx.restore();
  }
}

// ── Logique principale ────────────────────────────────────────────────────────
const canvasRef = ref(null);
let raf = null;

onMounted(() => {
  const canvas = canvasRef.value;
  if (!canvas) return;

  const ctx = canvas.getContext('2d', { alpha: true });
  let W = 0;
  let H = 0;
  let dpr = 1;
  let particles = [];
  let mouseX = -1000;
  let mouseY = -1000;

  // ── Resize ────────────────────────────────────────────────────────────────
  function resize() {
    dpr = Math.min(window.devicePixelRatio || 1, 2);
    W = window.innerWidth;
    H = window.innerHeight;
    canvas.width = Math.round(W * dpr);
    canvas.height = Math.round(H * dpr);
    canvas.style.width = W + 'px';
    canvas.style.height = H + 'px';
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    rebuildParticles(true);
  }

  function rebuildParticles(keepExisting = false) {
    const area = W * H;
    const target = Math.round(Math.min(280, Math.max(200, area / 3000)) * props.density);
    if (!keepExisting || particles.length === 0) {
      particles = [];
      for (let i = 0; i < target; i++) {
        particles.push(new Stick(W, H, true));
      }
    } else {
      // Ajuster le nombre en conservant l'existant
      while (particles.length < target) particles.push(new Stick(W, H, true));
      if (particles.length > target) particles.length = target;
    }
  }

  // ── Boucle d'animation ────────────────────────────────────────────────────
  function animate() {
    ctx.clearRect(0, 0, W, H);

    for (let i = 0, n = particles.length; i < n; i++) {
      particles[i].update(W, H, mouseX, mouseY);
      particles[i].draw(ctx);
    }

    raf = requestAnimationFrame(animate);
  }

  // ── Événements ───────────────────────────────────────────────────────────
  function onPointerMove(e) {
    mouseX = e.clientX;
    mouseY = e.clientY;
  }

  function onPointerLeave() {
    mouseX = -1000;
    mouseY = -1000;
  }

  const ro = new ResizeObserver(resize);
  ro.observe(document.documentElement);

  window.addEventListener('pointermove', onPointerMove, { passive: true });
  window.addEventListener('pointerleave', onPointerLeave, { passive: true });

  resize();
  animate();

  onUnmounted(() => {
    if (raf) cancelAnimationFrame(raf);
    ro.disconnect();
    window.removeEventListener('pointermove', onPointerMove);
    window.removeEventListener('pointerleave', onPointerLeave);
  });
});
</script>

<style scoped>
.particle-canvas {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  z-index: 0;
  pointer-events: none;
  display: block;
}
</style>
