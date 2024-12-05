<script setup>
import { useServerStore } from "@/stores/serverStore.js";
import botManagerRepository from "@/api/repositories/botManagerRepository.js";
import appConfig from '@/constants/appConfig.json';
import {computed} from "vue";
import {toast} from "vue3-toastify";
import {useLoaderStore} from "@/stores/loaderStore.js";

const serverToSend = computed(() => serverStore.getCurrentlySelected)
const allServersList = computed(() => serverStore.getAllServers);
const loaderStore = useLoaderStore();

async function handleClick(command) {
  try {

    const formattedIps = allServersList.value.filter(
      (server) => server.serverIp !== appConfig.allServersText
    );

    // Skip if no valid IPs
    if (formattedIps.length === 0) {
      return;
    }

    const payload = {
      command: command,
    };

    if (serverToSend.value !== appConfig.allServersText) {
      payload.servers = [{ serverIp: serverToSend.value }]
    } else {
      payload.servers = formattedIps
    }
    loaderStore.showLoader('Sending Command...');
    const response = await botManagerRepository.sendDashboardCommandsToServers(payload);
    toast.success(response.message)
    loaderStore.hideLoader();
  } catch (error) {
    loaderStore.hideLoader();
    toast.error(`Failed to send command "${command}": ${error.message}`);
  }
}

</script>

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
          <v-list-item link>
            <v-list-item-title>
              Enable AFK in Xbox Server
            </v-list-item-title>
            <v-list-item-subtitle />
            <template #append>
              <v-icon>mdi-arrow-right</v-icon>
            </template>
          </v-list-item>
        </v-list>
      </v-tabs-window-item>
      <v-tabs-window-item>
        <v-list>
          <v-list-item link>
            <v-list-item-title>
              Enable Movement AFK in in game
            </v-list-item-title>
            <v-list-item-subtitle />
            <template #append>
              <v-icon>mdi-arrow-right</v-icon>
            </template>
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
              <v-icon>mdi-arrow-right</v-icon>
            </template>
          </v-list-item>
          <v-list-item link>
            <v-list-item-title>
              Open all chrome profiles on target VM
            </v-list-item-title>
            <v-list-item-subtitle />
            <template #append>
              <v-icon>mdi-arrow-right</v-icon>
            </template>
          </v-list-item>
        </v-list>
      </v-tabs-window-item>
    </v-tabs-window>
  </v-container>
</template>
