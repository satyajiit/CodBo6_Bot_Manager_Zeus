<script setup>
import appConfig from '@/constants/appConfig.json';
function openYT() {
  window.open('https://www.youtube.com/@GamesPatch', '_blank');
}

const items = [
  { title: 'All' },
  { title: 'Server 1' },
  { title: 'Server 2' },
  { title: 'Server 3' },
  { title: 'Server 4' },
  { title: 'Server 5' },
  { title: 'Server 6' },
  { title: 'Server 7' },
  { title: 'Server 8' },
  { title: 'Server 9' },
  { title: 'Server 10' },
];

let serverButtonText = 'Select server';

function changeServer(index) {
  serverButtonText = items[index].title;
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

    <template #append>
      <div class="pl-2 pr-2">
        <v-btn
          @click="changeServer"
          variant="tonal"
          block
          color="primary"
        >
          {{ serverButtonText }}

          <v-menu activator="parent">
            <v-list height="300">
              <v-list-item
                v-for="(item, index) in items"
                :key="index"
                :value="index"
                @click="changeServer(index)"
              >
                <v-list-item-title>{{ item.title }}</v-list-item-title>
              </v-list-item>
            </v-list>
          </v-menu>
        </v-btn>
      </div>
      <div class="pa-2">
        <v-card
          elevation="2"
          class="pa-3"
          color="secondary"
          rounded
          @click="openYT"
        >
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
