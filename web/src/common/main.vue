<template>
  <component :is="curComponent" />
</template>

<script setup>
import { computed } from 'vue';
import PCpage from '../pages/main.vue';
import mobilePage from '../mobile/main.vue';
import {useDeviceDetection } from '../device'
const { isMobile } = useDeviceDetection();

const curComponent = computed(() => {
  return isMobile.value ? mobilePage : PCpage;
});
</script>