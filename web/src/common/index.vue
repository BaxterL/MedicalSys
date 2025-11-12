<template>
  <component :is="curComponent" />
</template>

<script setup>
import { computed, ref, onMounted, onBeforeUnmount } from 'vue';
import PCindex from '../pages/index.vue';
import mobileIndex from '../mobile/index.vue';

const MOBILE_WIDTH = 768;
const screenWidth = ref(window.innerWidth);
const handleResize = () => {
  screenWidth.value = window.innerWidth;
};
onMounted(() => {
  window.addEventListener('resize', handleResize);
});
onBeforeUnmount(() => {
  window.removeEventListener('resize', handleResize);
});
const isMobile = computed(() => {
  return screenWidth.value < MOBILE_WIDTH;
});
const curComponent = computed(() => {
  return isMobile.value ? mobileIndex : PCindex;
});
</script>