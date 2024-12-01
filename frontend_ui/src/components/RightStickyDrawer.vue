<script setup>
import { ref, onMounted, onUnmounted, computed, watch } from "vue";
import botManagerRepository from "@/api/repositories/botManagerRepository.js";
import { toast } from "vue3-toastify";
import { useLoggerStore } from "@/stores/loggerStore.js";
import EmptyStateIcon from "@/assets/icons/database-storage.svg";
import { useServerStore } from "@/stores/serverStore.js";
import appConfig from "@/constants/appConfig.json";
import { nextTick } from "vue";
const loggerStore = useLoggerStore();
const serverStore = useServerStore();
const intervalId = ref(null);
const healthList = ref([]); // Initialize as an empty array for reactivity
const allServersList = computed(() => serverStore.getAllServers);
const logs = computed(() => loggerStore.getLogs);

const logList = ref(null);
const isAutoScroll = ref(true);


function toggleAutoScroll() {
  isAutoScroll.value = !isAutoScroll.value;
}

watch(logs, () => {
  nextTick(() => {
    const logListElement = logList.value;
    if (logListElement && logListElement.$el && isAutoScroll.value) {
      logListElement.$el.scrollTo({
        top: logListElement.$el.scrollHeight,
        behavior: 'smooth' // Smooth scrolling
      });
    }
  });
});

// Fetch health data
const fetchHealthData = async () => {

  try {
    // Filter out the "all" entry from server list
    const formattedIps = allServersList.value.filter(
      (server) => server.serverIp !== appConfig.allServersText
    );

    // Skip if no valid IPs
    if (formattedIps.length === 0) {
      healthList.value = [];
      return;
    }

    // Fetch server health
    const response = await botManagerRepository.fetchServerHealth(formattedIps);
    if (response?.data?.serversList?.length > 0) {
      healthList.value = response.data.serversList;
    } else {
      healthList.value = []; // Clear the list if no data returned
    }
  } catch (error) {
    console.error("Error fetching server health:", error);
    toast.error(error.message || "Failed to fetch server health.");
    healthList.value = []; // Clear the list on error
  }
};

watch(
  () => allServersList.value,
  () => {
    fetchHealthData();
  },
  { deep: true, immediate: false }
);

onMounted(() => {
  fetchHealthData();
  intervalId.value = setInterval(fetchHealthData, appConfig.healthCheckIntervalSeconds * 1000);
});

onUnmounted(() => {
  // Clear the interval on unmount
  if (intervalId.value) {
    clearInterval(intervalId.value);
  }
});

function getColorByStatus(status) {
  const statusLower = status.toLowerCase();

  if (statusLower.includes('error')) {
    return "#EF5350";
  } else if (statusLower.includes('ok')) {
    return "#4CAF50";
  } else {
    return "#FFD54F";
  }
}



</script>



<template>
  <v-navigation-drawer
    location="end"
    elevation="2"
    permanent
  >
    <!-- Server Health Section -->
    <div class="pa-4">
      <h4>🖥️  Server Health</h4>
    </div>
    <v-divider />
    <v-list v-if="healthList.length > 0" height="200" class="overflow-y-auto">
      <v-list-item v-for="(serverHealth, index) in healthList" :key="index">
        <v-tooltip :text="serverHealth.reason">
          <template #activator="{ props }">
          <v-list-item-title v-bind="props" class="font-weight-bold">{{ serverHealth.serverIp }}</v-list-item-title>
          </template>
        </v-tooltip>
        <template #append>
          <div v-if="serverHealth.status === 'healthy'" class="d-flex ga-2 align-center">
            <v-icon
              color="#388E3C"
              size="28px"
            >
              mdi-circle-medium
            </v-icon>
          </div>
          <div class="d-flex ga-2" v-else>
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
          Status of all your added servers would show here!
        </v-card-text>
      </v-card>
    </div>
    <v-divider />

    <!-- Logs Section -->
    <div class="pa-4 d-flex flex-row align-center justify-space-between">
      <h4>Logs</h4>

      <v-tooltip text="Disable Autoscroll">
        <template v-slot:activator="{ props }">
          <v-btn v-bind="props" size="24" icon>
            <v-icon size="small" @click="toggleAutoScroll" color="black">mdi-arrow-vertical-lock</v-icon>
          </v-btn>
        </template>
      </v-tooltip>
    </div>
    <v-divider />
    <div style="background-color: black">
      <v-list ref="logList" height="400" class="overflow-y-auto code-font">
        <v-list-item v-for="(log, index) in logs" :key="index">
          <div class="list-text font-weight-bold">
            {{ log.cmdName }}
          </div>
          <div class="list-text">
            {{ new Date(log.timestamp).toLocaleString() }}
          </div>
          <div :style="{ color: getColorByStatus(log.message) }" class="list-text">
            {{ log.message }}
          </div>
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
