<script setup>
import appConfig from '@/constants/appConfig.json';
import botManagerRepository from "@/api/repositories/botManagerRepository.js";
import {toast} from "vue3-toastify";
import { computed } from 'vue';
import { useServerStore } from '@/stores/serverStore';


function openYT() {
  botManagerRepository.openUrlOnBrowser({
    targetUrl: appConfig.ytChannelUrl
  }).then(() => {
  }).catch((error) => {
    toast.error(error.message);
  });
}
const serverStore = useServerStore();
const selectedServer = computed(() => serverStore.getCurrentlySelected);
const allServers = computed(() => serverStore.getAllServers);
const deviceHwId = computed(() => serverStore.getDeviceHwId);

function changeServer(index) {
  const serverIp = allServers.value[index].serverIp;
  serverStore.setCurrentlySelected(serverIp);
}

function copyToClipboard(text) {
  botManagerRepository.copyToClipboard({
    text: text
  }).then(() => {
    toast.success("Copied to clipboard!");
  }).catch((error) => {
    toast.error(error.message);
  });
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
      <div class="pl-2 pr-2" v-if="allServers.length > 1">
        <v-btn
          variant="tonal"
          block
          color="primary"
        >
          {{ selectedServer }}

          <v-menu activator="parent">
            <v-list style="height: max-content">
              <v-list-item
                v-for="(item, index) in allServers"
                :key="index"
                :value="index"
                @click="changeServer(index)"
              >
                <v-list-item-title>{{ item.serverIp }}</v-list-item-title>
              </v-list-item>
            </v-list>
          </v-menu>
        </v-btn>
      </div>
      <div class="ml-2 pr-2 pt-2">
        <v-tooltip :text=deviceHwId to>
          <template v-slot:activator="{ props }">
      <v-btn
        class="me-2 text-none"
        color="primary"
        block
        v-bind="props"
        prepend-icon="mdi-content-copy"
        variant="flat"
        @click="copyToClipboard(deviceHwId)"
      >
        Copy HWID
      </v-btn>
          </template>
        </v-tooltip>
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
