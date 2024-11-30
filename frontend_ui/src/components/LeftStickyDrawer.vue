<script setup>

//initialise left drawer options to an array with icon, title and route
const leftDrawerOptions = [
  { icon: 'mdi-view-dashboard', title: 'Dashboard', route: '/' },
  { icon: 'mdi-account-box', title: 'Servers', route: '/account' },
  { icon: 'mdi-gavel', title: 'GamePad', route: '/admin' }
]

</script>

<template>
  <v-navigation-drawer
    class="primary"
    elevation="2"
    permanent
  >
    <v-list color="transparent">
      <v-list-item
        v-for="option in leftDrawerOptions"
        :key="option.title"
        :to="option.route"
        :prepend-icon="option.icon"
        :title="option.title"
      ></v-list-item>
    </v-list>

    <template v-slot:append>
      <div class="pa-2">
        <v-btn block>
          Logout
        </v-btn>
      </div>
    </template>
  </v-navigation-drawer>
</template>

<style scoped lang="sass">

</style>
