<script setup>
import {ref} from 'vue';
import {useLoaderStore} from '@/stores/loaderStore';
import CommonEmptyStateCard from '@/components/CommonEmptyStateCard.vue';
import serverEmptyIcon from '@/assets/icons/server_empty.svg';
import botManagerRepository from "@/api/repositories/botManagerRepository.js";
import {toast} from "vue3-toastify";
import {useServerStore} from "@/stores/serverStore.js";
import {el} from "vuetify/locale";
const serverStore = useServerStore();

const loaderStore = useLoaderStore();
const items = ref([]);
const ipDialogVisible = ref(false);

const openDialog = () => {
  ipDialogVisible.value = true;
};


async function fetchData() {
  try {
    loaderStore.showLoader('Fetching data...');
    botManagerRepository.fetchServers()
      .then((resp) => {
        items.value = resp.data;
        if (resp.data.length > 0)
          serverStore.setServerList(resp.data);
        else
          serverStore.setServerList([]);
      })
      .catch((error) => {
        toast.error(error.message);
      });
  } catch (error) {
    toast.error(error.message);
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
      fetchData()
    })
    .catch((error) => {
      loaderStore.hideLoader();
      toast.error(error.message);
    });
}

function deleteServer(ipAddress) {
  loaderStore.showLoader('Deleting server...');
  botManagerRepository.deleteServer([{ serverIp: ipAddress }])
    .then((resp) => {
      loaderStore.hideLoader();
      toast.success(resp.message);
      fetchData()
    })
    .catch((error) => {
      loaderStore.hideLoader();
      console.log(error);
      toast.error(error.message);
    });

}

fetchData();
</script>

<template>
  <v-container class="h-100" fluid>

    <IpInputDialog
      @update:ipDialogVisible="ipDialogVisible = $event"
      :ip-dialog-visible="ipDialogVisible"
      @save="handleIpSave" />


    <!-- Show empty state if no data -->
    <div v-if="items.length === 0" class="d-flex flex-column align-center justify-center h-100 w-100 mt-4">
      <CommonEmptyStateCard
        :imageSrc=serverEmptyIcon
        mainText="No Servers/VMs Added"
        subText="Start by adding a new server or virtual machine."
        buttonText="Add Server"
        buttonColor="secondary"
        @button-click="handleButtonClick"
      />
    </div>

    <!-- Show data when available -->
    <div class="mt-2" v-else>
      <v-list-item
        v-for="(server, index) in items"
        :key="index"
      >
        <v-card rounded>
          <template #title>
            <v-list-item-title class="text-start font-weight-bold">{{ server.serverIp }}</v-list-item-title>
          </template>
          <template #append>
            <v-btn @click="deleteServer(server.serverIp)" icon variant="flat"><v-icon color="red">mdi-trash-can</v-icon></v-btn>
          </template>
        </v-card>
      </v-list-item>
    </div>
  </v-container>
</template>

<style scoped>

</style>
