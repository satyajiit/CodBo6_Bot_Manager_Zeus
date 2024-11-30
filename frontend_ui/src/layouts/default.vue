<template>
  <v-app>
    <Toolbar />




    <LeftStickyDrawer />


    <v-row class="pa-0 ma-0">
      <v-col cols="9">
        <v-main>
          <router-view />
        </v-main>
      </v-col>

      <v-col cols="3">

        <RightStickyDrawer />

      </v-col>

    </v-row>

  </v-app>
</template>

<script setup>
  //
</script>
