<script setup>
import appConfig from '@/constants/appConfig.json';
function openYT() {
  window.open('https://www.youtube.com/@GamesPatch', '_blank');
}
</script>

<template>
  <v-navigation-drawer
    class="primary"
    elevation="2"
    permanent
  >
    <v-list>
      <v-list-item
        v-for="option in appConfig.leftDrawerOptions"
        :key="option.title"
        :to="option.route"
        active-color="primary"
        :prepend-icon="option.icon"
        :title="option.title"
      ></v-list-item>
    </v-list>

    <template v-slot:append>
      <div class="pa-2">
        <v-card @click="openYT" elevation="2" rounded color="secondary" class="pa-3">
          <p class="text-sm-center">
            Made with ❤️ from GamesPatch
          </p>

        </v-card>
      </div>
    </template>
  </v-navigation-drawer>
</template>

<style scoped lang="sass">

</style>
