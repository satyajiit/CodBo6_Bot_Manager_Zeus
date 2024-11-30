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
</script>

<style scoped>
.layout-container {
  display: flex;
  padding: 24px;
  max-width: calc(100vw -  510px); /* Subtract the width of the drawers */
}

.center-content {
  flex: 1;
  overflow-y: auto;
  height: 100vh;
  padding: 16px;
}
</style>
