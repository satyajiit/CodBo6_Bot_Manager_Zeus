<script setup>
import {ref} from 'vue';
import {useLoaderStore} from '@/stores/loaderStore';
import CommonEmptyStateCard from '@/components/CommonEmptyStateCard.vue';
import serverEmptyIcon from '@/assets/icons/server_empty.svg';
import botManagerRepository from "@/api/repositories/botManagerRepository.js";
import {toast} from "vue3-toastify";

const loaderStore = useLoaderStore();
const items = ref([]);
const ipDialogVisible = ref(false);

const openDialog = () => {
  ipDialogVisible.value = true;
};

async function fetchData() {
  try {
    loaderStore.showLoader('Fetching data...');
    items.value = await new Promise((resolve) =>
      setTimeout(() => resolve([]), 2000)
    );
  } catch (error) {
    console.error('Error fetching data:', error);
  } finally {
    loaderStore.hideLoader();
  }
}

function handleButtonClick() {
  openDialog();
}

function handleIpSave(ipArray) {

  loaderStore.showLoader('Saving data...');

  const formattedIps = ipArray.map((ip) => ({ serverIp: ip }));

  botManagerRepository.saveIpAddress(formattedIps)
    .then((resp) => {
      loaderStore.hideLoader();
      toast.success(resp.message);
    })
    .catch((error) => {
      loaderStore.hideLoader();
      toast.success(error.message);
    });
}

fetchData();
</script>

<template>
  <v-container class="d-flex flex-column align-center justify-center" fluid>

    <IpInputDialog
      @update:ipDialogVisible="ipDialogVisible = $event"
      :ip-dialog-visible="ipDialogVisible"
      @save="handleIpSave" />


    <!-- Show empty state if no data -->
    <CommonEmptyStateCard
      v-if="items.length === 0"
      :imageSrc=serverEmptyIcon
      mainText="No Servers/VMs Added"
      subText="Start by adding a new server or virtual machine."
      buttonText="Add Server"
      buttonColor="secondary"
      @button-click="handleButtonClick"
    />

    <!-- Show data when available -->
    <div v-else>
      <v-card
        v-for="(item, index) in items"
        :key="index"
        class="mb-2"
        outlined
      >
        <v-card-text>
          <p>{{ item.name }}</p>
        </v-card-text>
      </v-card>
    </div>
  </v-container>
</template>

<style scoped>
.v-container {
  height: 100vh;
  width: 100%;
  text-align: center;
}
</style>
