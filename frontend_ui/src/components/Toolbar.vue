<script setup>
import appConfig from '@/constants/appConfig.json';
import bo6Logo from '@/assets/icons/bo6.png';
</script>

<template>
  <v-app-bar :elevation="2" rounded>
    <v-container class="d-flex justify-between align-center" fluid>
      <!-- Invisible Spacer to Balance Text and Center the Logo -->
      <div class="invisible-spacer"></div>

      <!-- Centered Logo -->
      <div class="logo-container">
        <v-img :src="bo6Logo" max-height="60" max-width="120" />
      </div>

      <!-- Text on the Right -->
      <div class="text-container d-flex justify-end align-center">
        <span class="font-weight-medium text-subtitle-2 text-teal-darken-4">
          {{ appConfig.appName }}
        </span>
      </div>
    </v-container>
  </v-app-bar>
</template>

<style scoped>
/* Invisible Spacer to Balance Left Side */
.invisible-spacer {
  flex: 1;
}

/* Centered Logo */
.logo-container {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 120px; /* Explicit width for the logo container */
  height: 60px; /* Explicit height for the logo container */
}

/* Right-Aligned Text */
.text-container {
  flex: 1;
  text-align: right;
}
</style>
