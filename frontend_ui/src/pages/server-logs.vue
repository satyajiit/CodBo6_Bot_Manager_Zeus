<script setup>

import botManagerRepository from "@/api/repositories/botManagerRepository.js";
import {toast} from "vue3-toastify";
import {ref} from "vue";
const logsData = ref(null)

    botManagerRepository.tailServerLogs().then((response) => {
      logsData.value = response.data.results
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
      v-for="(logs, index) in logsData"
      :key="index"
      class="mb-4 pa-4 text-white"
      style="height: 500px; background-color: black; overflow: auto"
    >
      <div class="terminal code-font">
        <p class="font-weight-bold">server@{{ logs.serverIp}}:~$</p>
        <span v-for="(log, index) in logsData.logs" :key="index" class="info">{{ log }}</span><br>
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
</style>
