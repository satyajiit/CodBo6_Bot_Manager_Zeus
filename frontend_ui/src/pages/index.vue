<template>
  <v-container
    class="h-100"
    fluid
  >
    <v-tabs
      v-model="tab"
      mandatory
      color="primary"
      fixed-tabs
    >
      <v-tab text="☁️ Xbox Cloud" />
      <v-tab text="🎮 In-Game" />
      <v-tab text="⚙️ Chrome Configs" />
    </v-tabs>

    <v-tabs-window v-model="tab">
      <v-tabs-window-item>
        <v-list>
          <v-list-item>
            <v-switch
              v-model="xboxSwitch"
              color="primary"
              class="pl-3"
              :label="`Enable AFK in Xbox Server`"
              hide-details
            />
          </v-list-item>
        </v-list>
      </v-tabs-window-item>
      <v-tabs-window-item>
        <v-list>
          <v-list-item>
            <v-switch
              v-model="inGameSwitch"
              color="primary"
              class="pl-3"
              :label="`Enable Movement AFK in in game`"
              hide-details
            />
          </v-list-item>
        </v-list>
      </v-tabs-window-item>
      <v-tabs-window-item>
        <v-list>
          <v-list-item link>
            <v-list-item-title>
              Install TaperMonkey Extension on all Chrome profiles
            </v-list-item-title>
            <v-list-item-subtitle />
            <template #append>
              <v-icon>mdi-open-in-new</v-icon>
            </template>
          </v-list-item>
          <v-list-item link>
            <v-list-item-title>
              Open all chrome profiles on target VM
            </v-list-item-title>
            <v-list-item-subtitle />
            <template #append>
              <v-icon>mdi-open-in-new</v-icon>
            </template>
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
