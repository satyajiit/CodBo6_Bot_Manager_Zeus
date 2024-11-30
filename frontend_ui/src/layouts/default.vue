<template>
  <v-app>
    <!-- Global Loader -->
    <GlobalLoader />

    <!-- Top Toolbar -->
    <Toolbar />

    <!-- Main Layout -->
    <v-container fluid class="layout-container pa-0 ma-0">
      <!-- Left Sticky Drawer -->
      <LeftStickyDrawer />

      <!-- Center Content -->
      <v-main class="center-content ma-0 pa-0">
        <router-view />
      </v-main>

      <!-- Right Sticky Drawer -->
      <RightStickyDrawer />
    </v-container>
  </v-app>
</template>

<script setup>
</script>

<style scoped>
.layout-container {
  display: flex;
  height: calc(100vh - 64px); /* Subtract the height of the toolbar */
}

.center-content {
  flex: 1;
  overflow-y: auto;
  height: 100vh;
  padding: 16px;
}
</style>
