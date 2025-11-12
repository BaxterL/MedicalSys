import { ref, onMounted, onBeforeUnmount, computed } from 'vue';

export const useDeviceDetection = () => {
  const MOBILE_WIDTH = 768;
  const screenWidth = ref(window.innerWidth);
  
  const handleResize = () => {
    screenWidth.value = window.innerWidth;
  };
  
  const isMobile = computed(() => {
    return screenWidth.value < MOBILE_WIDTH;
  });
  
  onMounted(() => {
    window.addEventListener('resize', handleResize);
  });
  
  onBeforeUnmount(() => {
    window.removeEventListener('resize', handleResize);
  });
  
  return {
    screenWidth,
    isMobile
  };
};