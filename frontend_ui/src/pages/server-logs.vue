<script setup>

import botManagerRepository from "@/api/repositories/botManagerRepository.js";
import {toast} from "vue3-toastify";
import {ref} from "vue";

let logsData = ref({});


    botManagerRepository.tailServerLogs().then((response) => {
      logsData.value = response.data
      console.log("Logs", logsData.value)
    }).catch((error) => {
      toast.error(error.message);
    });

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
