<script setup>
import appConfig from '@/constants/appConfig.json';
import bo6Logo from '@/assets/icons/bo6.png';
import github from '@/assets/icons/github.svg';
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

      <v-btn
        width="200"
        variant="tonal"
        color="black"
        @click="openGithub"
        class="font-weight-regular"
        style="text-transform: none;"
      >
        <v-img
          :src="github"
          height="20"
          width="20"
          class="mr-2"
        />
        Star on GitHub
      </v-btn>



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
</style>
