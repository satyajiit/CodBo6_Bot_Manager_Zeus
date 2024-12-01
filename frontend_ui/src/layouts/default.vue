<template>
  <v-app>
    <!-- Global Loader -->
    <GlobalLoader />

    <!-- Top Toolbar -->
    <Toolbar />

    <!-- Main Layout -->
    <v-container
      fluid
      class="pt-12 ma-0 d-flex align-start justify-center"
    >
      <!-- Left Sticky Drawer -->
      <LeftStickyDrawer />

      <!-- Center Content -->
      <v-main
        class="d-flex align-start flex-column justify-center ma-0 pa-0 layout-container position-relative"
      >
        <router-view />
      </v-main>
      <div v-if="!currentRoute.name.includes('server')" class="d-flex align-start justify-center w-100 layout-container bottom-info">
        <v-alert
          :text="`Changes will be applied to the selected server: ${selectedServer}`"
          color="#42A5F5"
          icon="mdi-information"
        ></v-alert>
      </div>

      <!-- Right Sticky Drawer -->
      <RightStickyDrawer />
    </v-container>
  </v-app>
</template>

<script setup>
import RightStickyDrawer from "@/components/RightStickyDrawer.vue";
import LeftStickyDrawer from "@/components/LeftStickyDrawer.vue";
import Toolbar from "@/components/Toolbar.vue";
import GlobalLoader from "@/components/GlobalLoader.vue";
import botManagerRepository from "@/api/repositories/botManagerRepository.js";
import {toast} from "vue3-toastify";
import {useLoaderStore} from "@/stores/loaderStore.js";
import {useServerStore} from "@/stores/serverStore.js";
import {useRoute} from "vue-router";
import {computed} from "vue";
const loaderStore = useLoaderStore();
const serverStore = useServerStore();

function fetchDeviceHwId() {
  try {
    botManagerRepository.getDeviceHwId()
      .then((resp) => {
        serverStore.setDeviceHwId(resp.data.hwid);
      })
      .catch((error) => {
        toast.error(error.message);
      });
  } catch (error) {
    toast.error(error.message);
  } finally {
    loaderStore.hideLoader();
  }
}

function fetchAllServers() {
  try {
    loaderStore.showLoader('Fetching servers list...');
    botManagerRepository.fetchServers()
      .then((resp) => {
        if (resp.data.length > 0)
        serverStore.setServerList(resp.data);
      })
      .catch((error) => {
        toast.error(error.message);
      });
  } catch (error) {
    toast.error(error.message);
  } finally {
    loaderStore.hideLoader();
  }
}

fetchAllServers()
fetchDeviceHwId()

const route = useRoute()
const currentRoute = route

const selectedServer = computed(() => serverStore.getCurrentlySelected);

</script>

<style scoped>
.layout-container {
  display: flex;
  padding: 24px;
  max-width: calc(100vw -  485px); /* Subtract the width of the drawers */
}

.bottom-info {
  position: absolute;
  bottom: 0;
  padding-bottom: 8px
}
</style>
