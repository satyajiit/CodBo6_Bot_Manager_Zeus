<script setup>
import appConfig from '@/constants/appConfig.json';

</script>

<template>
  <v-app-bar :elevation="2" rounded>
    <v-container class="d-flex justify-center align-center" fluid>
      <v-app-bar-title class="font-weight-medium text-center">
        {{ appConfig.appName }}
      </v-app-bar-title>
    </v-container>
  </v-app-bar>
</template>

<style scoped lang="sass">

</style>
