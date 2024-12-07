<template>
  <div
    v-if="isLoading"
    class="loader-overlay d-flex align-center justify-center"
  >
    <v-card elevation="2" class="loader-card d-flex flex-column align-center">
      <v-progress-circular size="80" indeterminate color="primary" class="mb-4" />
      <p class="text-center">{{ loadingText }}</p>
    </v-card>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { useLoaderStore } from '@/stores/loaderStore';

// Access Pinia store
const loaderStore = useLoaderStore();

// Computed properties for loader state
const isLoading = computed(() => loaderStore.isLoading);
const loadingText = computed(() => loaderStore.loadingText);
</script>

<style scoped>
.loader-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(5px);
  z-index: 2000;
}

.loader-card {
  padding: 24px;
  border-radius: 8px;
  min-width: 200px;
  max-width: 300px;
}
</style>
