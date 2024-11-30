<script setup>
import appConfig from '@/constants/appConfig.json';
import bo6Logo from '@/assets/icons/bo6.png';
</script>

<template>
  <v-app-bar :elevation="2" rounded>
    <v-container class="d-flex justify-between align-center" fluid>
      <!-- Centered Logo -->
      <div class="d-flex justify-center align-center flex-grow-1">
        <v-img :src="bo6Logo" max-height="120" max-width="180" />
      </div>

      <!-- Text on the Right -->
      <div class="d-flex justify-end align-center">
        <span class="font-weight-medium text-body-1">
          {{ appConfig.appName }}
        </span>
      </div>
    </v-container>
  </v-app-bar>
</template>

<style scoped lang="sass">

</style>
