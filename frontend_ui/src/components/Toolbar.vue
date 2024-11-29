<script setup>
import appConfig from '@/constants/appConfig.json';

</script>

<template>
  <v-app-bar :elevation="2" rounded>
    <v-app-bar-title class="font-weight-medium">{{ appConfig.appName }}</v-app-bar-title>
  </v-app-bar>
</template>

<style scoped lang="sass">

</style>
