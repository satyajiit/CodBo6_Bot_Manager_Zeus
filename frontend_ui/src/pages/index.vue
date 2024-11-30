<template>
  <v-container class="h-100" fluid>
    <v-tabs
      v-model="tab"
      mandatory
      color="primary"
      fixed-tabs
    >
      <v-tab text="Xbox Cloud">

      </v-tab>

      <v-tab text="In-Game">

      </v-tab>
    </v-tabs>

    <v-tabs-window v-model="tab">
      <v-tabs-window-item>
        <v-list>
          <v-list-item>
            <v-switch
              color="primary"
              v-model="xboxSwitch"
              class="pl-3"
              :label="`Enable AFK in Xbox Server`"
              hide-details
            ></v-switch>
          </v-list-item>
        </v-list>
      </v-tabs-window-item>
      <v-tabs-window-item>
        <v-list>
          <v-list-item>
            <v-switch
              color="primary"
              v-model="inGameSwitch"
              class="pl-3"
              :label="`Enable AFK in In-Game Server`"
              hide-details
            ></v-switch>
          </v-list-item>
        </v-list>
      </v-tabs-window-item>
    </v-tabs-window>
  </v-container>
</template>

<script setup>
import { ref } from 'vue';

  let tab = ref(0);

  let xboxSwitch = ref(false);
  let inGameSwitch = ref(false);
</script>
