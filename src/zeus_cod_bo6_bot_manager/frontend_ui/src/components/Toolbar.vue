<script setup>
import appConfig from '@/constants/appConfig.json';
import bo6Logo from '@/assets/icons/bo6.png';
import github from '@/assets/icons/github.png';
import botManagerRepository from "@/api/repositories/botManagerRepository.js";
import {toast} from "vue3-toastify";

function openGithub() {
  botManagerRepository.openUrlOnBrowser({
    targetUrl: appConfig.githubUrl
  }).then(() => {
  }).catch((error) => {
    toast.error(error.message);
  });
}

</script>

<template>
  <v-app-bar
    :elevation="2"
    rounded
  >
    <v-container class="d-flex flex-row align-center justify-space-between w-100" fluid>
      <!-- Invisible Spacer to Balance Text and Center the Logo -->

      <div v-ripple @click="openGithub" class="icon-button">
        <div class="icon-avatr pa-2">
          <v-img
            :src="github"
            height="20"
            width="20"
          />
        </div>
        <div class="ml-2 text-white pa-1 font-weight-medium" style="font-size: 14px; user-select: none">
          Star on GitHub
        </div>
      </div>



      <!-- Centered Logo -->
      <div class="logo-container">
        <v-img
          :src="bo6Logo"
          max-height="60"
          max-width="120"
        />
      </div>

      <!-- Text on the Right -->
      <span
        class="text-teal-darken-4"
        style="font-size: small"
      >
        {{ appConfig.appName }} <v-badge
          color="info"
          :content="appConfig.appVersion"
          inline
        />
      </span>
    </v-container>
  </v-app-bar>
</template>

<style scoped>
.logo-container {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 120px;
  height: 60px;
}

.icon-button {
  display: flex;
  flex-direction: row;
  width: 200px;
  align-items: center;
  justify-content: start;
  border-radius: 4px;
  background-color: #212121;
  cursor: pointer;
}
.icon-avatr {
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #424242;
  border-top-left-radius: 4px;
  border-bottom-left-radius: 4px;

}
</style>
