<script setup>
import {ref, onMounted, onUnmounted, computed} from "vue";
import botManagerRepository from "@/api/repositories/botManagerRepository.js";
import { toast } from "vue3-toastify";
import { useLoggerStore} from "@/stores/loggerStore.js";

const loggerStore = useLoggerStore(); // Access your store
const serverHealth = ref({ data: {} });
const intervalId = ref(null);
const logs = computed(() => loggerStore.getLogs);

// Fetch health data
const fetchHealthData = async () => {
  try {
    serverHealth.value = await botManagerRepository.fetchServerHealth();
    toast.info("Checking server health");
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
    <v-list height="300" class="overflow-y-auto">
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
    <v-divider/>

    <!-- Logs Section -->
    <div class="pa-4">
      <h4>Logs</h4>
    </div>
    <v-divider/>
    <v-list height="300" class="overflow-y-auto">
      <v-list-item v-for="(log, index) in logs" :key="index">
        <v-list-item-title class="font-weight-bold">{{ log.cmdName }}</v-list-item-title>
        <v-list-item-subtitle>{{ new Date(log.timestamp).toLocaleString() }}</v-list-item-subtitle>
        <v-list-item-subtitle>{{ log.message }}</v-list-item-subtitle>
      </v-list-item>
    </v-list>
  </v-navigation-drawer>
</template>

<style scoped lang="sass">

</style>
