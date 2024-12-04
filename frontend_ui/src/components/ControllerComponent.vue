<template>
  <v-container>
    <v-card class="pa-6">
      <!-- Top: L and R Buttons -->
      <v-row justify="space-between" align="center" class="mb-6">
        <v-btn
          outlined
          class="button l-button"
          @click="handleButtonClick('press_lb')"
        >
          L
        </v-btn>
        <v-btn
          outlined
          class="button r-button"
          @click="handleButtonClick('press_rb')"
        >
          R
        </v-btn>
      </v-row>

      <div class="d-flex flex-row align-center justify-space-between pt-6">
        <v-row dense style="max-width: 250px">
          <v-col cols="4"></v-col>
          <v-col cols="4">
            <v-btn
              outlined
              class="button"
              @click="handleButtonClick('press_dpad_up')"
            >
              <v-icon
                icon="mdi-arrow-up-bold"
                size="large"
              ></v-icon>
            </v-btn>
          </v-col>
          <v-col cols="4"></v-col>
          <v-col cols="4">
            <v-btn
              outlined
              class="button"
              @click="handleButtonClick('press_dpad_left')"
            >
              <v-icon
                icon="mdi-arrow-left-bold"
                size="large"
              ></v-icon>
            </v-btn>
          </v-col>
          <v-col cols="4">
            <v-btn
              outlined
              class="button"
              @click="handleButtonClick('press_dpad_down')"
            >
              <v-icon
                icon="mdi-arrow-down-bold"
                size="large"
              ></v-icon>
            </v-btn>
          </v-col>
          <v-col cols="4">
            <v-btn
              outlined
              class="button"
              @click="handleButtonClick('press_dpad_right')"
            >
              <v-icon
                icon="mdi-arrow-right-bold"
                size="large"
              ></v-icon>
            </v-btn>
          </v-col>
        </v-row>
        <div class="buttons-grid">
          <v-btn
            outlined
            class="button y-button"
            color="yellow darken-2"
            @click="handleButtonClick('press_y')"
          >
            Y
          </v-btn>
          <v-btn
            outlined
            class="button x-button"
            color="blue darken-2"
            @click="handleButtonClick('press_x')"
          >
            X
          </v-btn>
          <v-btn
            outlined
            class="button a-button"
            color="green darken-2"
            @click="handleButtonClick('press_a')"
          >
            A
          </v-btn>
          <v-btn
            outlined
            class="button b-button"
            color="red darken-2"
            @click="handleButtonClick('press_b')"
          >
            B
          </v-btn>
        </div>
      </div>
    </v-card>
  </v-container>
</template>

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

const serverStore = useServerStore()
async function handleButtonClick(command) {
  try {

    const formattedIps = allServersList.value.filter(
      (server) => server.serverIp !== appConfig.allServersText
    );

    // Skip if no valid IPs
    if (formattedIps.length === 0) {
      return;
    }

    const payload = {
      keyCode: command,
    };

    if (serverToSend.value !== appConfig.allServersText) {
        payload.servers = [{ serverIp: serverToSend.value }]
    } else {
      payload.servers = formattedIps
    }
    loaderStore.showLoader('Sending Gamepad Command...');
    const response = await botManagerRepository.sendGamePadCommandsToServers(payload);
    toast.success(response.message)
    loaderStore.hideLoader();
  } catch (error) {
    loaderStore.hideLoader();
    toast.error(`Failed to send command "${command}": ${error.message}`);
  }
}
</script>

<style scoped>
/* General Styles */
.button {
  width: 64px;
  height: 64px;
  font-weight: bold;
  font-size: 16px;
}

/* D-Pad Styles */
.dpad {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.dpad-middle {
  display: flex;
  justify-content: space-between;
  width: 160px;
  margin: 8px 0;
}

.dpad-button {
  min-width: 64px;
  min-height: 64px;
  font-weight: bold;
}

/* Buttons Grid for Y, X, A, B */
.buttons-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
  justify-items: center;
}

/* L and R Buttons */
.l-button,
.r-button {
  width: 80px;
  height: 64px;
  font-weight: bold;
  font-size: 16px;
}
</style>
