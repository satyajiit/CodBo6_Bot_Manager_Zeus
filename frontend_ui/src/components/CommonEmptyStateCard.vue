<template>
  <v-card elevation="2" class="empty-state-card rounded d-flex flex-column align-center justify-center pa-8">
    <v-img
      v-if="imageSrc"
      :src="imageSrc"
      alt="empty state image"
      class="mb-4"
      height="80"
      width="80"
    />
    <p class="text-center font-weight-bold text-body-1 mb-2">{{ mainText }}</p>
    <p class="text-center text-body-2 mb-4">{{ subText }}</p>
    <v-btn v-if="buttonText" :color="buttonColor" @click="onButtonClick">
      {{ buttonText }}
    </v-btn>
  </v-card>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue';

defineProps({
  imageSrc: {
    type: String,
    required: false,
    default: null, // Path to the image or null if no image is needed
  },
  mainText: {
    type: String,
    required: true, // The main text to display
  },
  subText: {
    type: String,
    required: true, // The subtext to display
  },
  buttonText: {
    type: String,
    required: false, // Text for the button
    default: null, // No button by default
  },
  buttonColor: {
    type: String,
    required: false,
    default: 'primary', // Default Vuetify button color
  },
});

const emit = defineEmits(['button-click']);

// Emit an event when the button is clicked
function onButtonClick() {
  emit('button-click');
}
</script>

<style scoped>
.empty-state-card {
  max-width: 400px;
  text-align: center;
}
</style>
