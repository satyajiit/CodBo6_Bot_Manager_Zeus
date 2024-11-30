<script setup>
import {ref, onMounted, onUnmounted, computed} from "vue";
import botManagerRepository from "@/api/repositories/botManagerRepository.js";
import { toast } from "vue3-toastify";
import { useLoggerStore} from "@/stores/loggerStore.js";
import EmptyStateIcon from "@/assets/icons/database-storage.svg";
const loggerStore = useLoggerStore(); // Access your store
const serverHealth = ref({ data: {} });
const intervalId = ref(null);
const logs = computed(() => loggerStore.getLogs);

// Fetch health data
const fetchHealthData = async () => {
  try {
    serverHealth.value = await botManagerRepository.fetchServerHealth();
  } catch (err) {
    toast.error(err.message);
  }
};

onMounted(() => {
  // Fetch initial data when mounted
  fetchHealthData();

  // Set interval to update every 15 seconds
  intervalId.value = setInterval(fetchHealthData, 15000);
});

onUnmounted(() => {
  // Clear the interval when the component is unmounted
  if (intervalId.value) {
    clearInterval(intervalId.value);
  }
});
</script>

<template>
  <v-navigation-drawer
    location="end"
    elevation="2"
    permanent
  >
    <!-- Server Health Section -->
    <div class="pa-4">
      <h4>Server Health</h4>
    </div>
    <v-divider/>
    <v-list v-if="serverHealth && Object.keys(serverHealth.data).length > 0" height="200" class="overflow-y-auto">
      <v-list-item v-for="(serverHealth, index) in serverHealth.data.server_status" :key="index">
        <v-list-item-title class="font-weight-bold">{{ serverHealth.server_ip }}</v-list-item-title>
        <template #append>
          <div v-if="serverHealth.status === 'healthy'" class="d-flex ga-2 align-center">
            <p>Healthy</p>
            <v-icon
              color="#388E3C"
              size="28px"
            >
              mdi-circle-medium
            </v-icon>
          </div>
          <div class="d-flex ga-2" v-else>
            <p>Unhealthy</p>
            <v-icon
              color="#E53935"
              size="28px"
            >
              mdi-circle-medium
            </v-icon>
          </div>
        </template>
      </v-list-item>
    </v-list>
    <div style="height: 200px" class="d-flex flex-row align-center justify-center" v-else>
      <v-card flat>
        <v-card-text class="d-flex align-center justify-center flex-column text-center">
          <v-img class="mb-2" height="50" width="50" :src="EmptyStateIcon"></v-img>
          Servers that are online will appear here
        </v-card-text>
      </v-card>
    </div>
    <v-divider/>

    <!-- Logs Section -->
    <div class="pa-4">
      <h4>Logs</h4>
    </div>
    <v-divider />
    <div style="background-color: black">
      <v-list height="400" class="overflow-y-auto code-font">
        <v-list-item v-for="(log, index) in logs" :key="index">
          <div class="list-text font-weight-bold">
            {{ log.cmdName }}
          </div>
          <v-list-item-subtitle class="list-text">{{ new Date(log.timestamp).toLocaleString() }}</v-list-item-subtitle>
          <v-list-item-subtitle class="list-text">{{ log.message }}</v-list-item-subtitle>
        </v-list-item>
      </v-list>
    </div>
  </v-navigation-drawer>
</template>

<style scoped>
.list-text {
  color: white;
  font-size: 13px;
}
</style>
