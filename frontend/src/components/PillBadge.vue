<template>
  <span class="pill-badge" :class="tone">
    <slot />
  </span>
</template>

<script setup>
defineProps({
  tone: {
    type: String,
    default: 'aubergine',
  },
});
</script>
