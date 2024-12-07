<script setup>

import botManagerRepository from "@/api/repositories/botManagerRepository.js";
import {toast} from "vue3-toastify";
import {computed, ref} from "vue";
import appConfig from "@/constants/appConfig.json";
import {useLoaderStore} from "@/stores/loaderStore.js";
import { useServerStore } from "@/stores/serverStore.js";
const serverStore = useServerStore()

let logsData = ref({});
const allServersList = computed(() => serverStore.getAllServers);
const loaderStore = useLoaderStore();


async function getLogs() {
  try {

    const formattedIps = allServersList.value.filter(
      (server) => server.serverIp !== appConfig.allServersText
    );

    // Skip if no valid IPs
    if (formattedIps.length === 0) {
      return;
    }

    const payload = {
      command: "tail_logs",
    };

    payload.servers = formattedIps

    loaderStore.showLoader('Getting logs...');
    const response = await botManagerRepository.tailServerLogs(payload);
    logsData.value = response.data;
    loaderStore.hideLoader();

  } catch (e) {
    loaderStore.hideLoader();
    toast.error(`Failed get logs": ${e.message}`);
  }
}

getLogs()


</script>

<template>
  <v-container
    class="overflow-y-auto pb-0"
    height="720px"
    fluid
  >
    <div
      v-for="(data, index) in logsData.results"
      :key="index"
      class="mb-4 pa-4 text-white"
      style="height: 500px; background-color: black; overflow: auto"
    >
      <div class="terminal code-font">
        <p class="font-weight-bold">server@{{ data.serverIp}}:~$</p>
        <div v-if="data.status === 'success'">
          <span v-for="(log, index) in data.logs" :key="index" :class="log.toLowerCase().includes('error') ? 'error' : 'info'">{{ log }} <br/></span>
        </div>
        <div v-else>
          <span class="error">Failed to fetch logs</span>
        </div>
      </div>
    </div>

  </v-container>
</template>

<style scoped>
.terminal {
  white-space: pre-wrap;
  line-height: 1.5;
  padding-left: 12px;
}
.info {
  color: #42A5F5;
}

.error {
  color: #FF5252;
}
</style>
