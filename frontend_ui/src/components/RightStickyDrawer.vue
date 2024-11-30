<script setup>

const items = [
  { title: 'Server 1', icon: 'mdi-circle-medium', color: 'green' },
  { title: 'Server 1', icon: 'mdi-circle-medium', color: 'green' },
  { title: 'Server 1', icon: 'mdi-circle-medium', color: 'green' },
  { title: 'Server 1', icon: 'mdi-circle-medium', color: 'green' },
  { title: 'Server 1', icon: 'mdi-circle-medium', color: 'green' },
  { title: 'Server 1', icon: 'mdi-circle-medium', color: 'green' },
  { title: 'Server 1', icon: 'mdi-circle-medium', color: 'green' },
  { title: 'Server 1', icon: 'mdi-circle-medium', color: 'green' },
  { title: 'Server 1', icon: 'mdi-circle-medium', color: 'green' },
]

</script>

<template>
  <v-navigation-drawer
    location="end"
    elevation="2"
    permanent
  >
    <div class="pa-4">
      <h4>Health</h4>
    </div>
    <v-divider />
    <v-list height="300" class="overflow-y-auto">
      <v-list-item v-for="(item, index) in items" :key="index">
        <v-list-item-title>{{ item.title }}</v-list-item-title>
        <template
          #append
        >
          <v-icon
            color="green"
            size="28px"
          >
            mdi-circle-medium
          </v-icon>
        </template>
      </v-list-item>
    </v-list>
    <v-divider />
    <div class="pa-4">
      <h4>Logs</h4>
    </div>
    <v-divider />
  </v-navigation-drawer>
</template>

<style scoped lang="sass">

</style>
