<template>
  <component :is="curComponent" />
</template>

<script setup>
import { computed } from 'vue';
import PCpage from '../pages/chat.vue';
import mobilePage from '../mobile/chat.vue';
import {useDeviceDetection } from '../device'
const { isMobile } = useDeviceDetection();

const curComponent = computed(() => {
  return isMobile.value ? mobilePage : PCpage;
});
</script>