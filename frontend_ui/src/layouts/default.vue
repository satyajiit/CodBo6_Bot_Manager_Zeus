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
        class="d-flex align-start justify-center ma-0 pa-0 layout-container"
      >
        <router-view />
      </v-main>

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

</script>

<style scoped>
.layout-container {
  display: flex;
  padding: 24px;
  max-width: calc(100vw -  485px); /* Subtract the width of the drawers */
}

.center-content {
  flex: 1;
  overflow-y: auto;
  height: 100vh;
  padding: 16px;
}
</style>
