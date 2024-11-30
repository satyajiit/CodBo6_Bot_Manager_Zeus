import { defineStore } from 'pinia';
import appConfig from '@/constants/appConfig.json';


export const useServerStore = defineStore('serverStore', {
  state: () => ({
    servers: [],
    currentlySelected: 'All servers' // Default selected server
  }),

  getters: {
    // Get the currently selected server
    getCurrentlySelected(state) {
      return state.currentlySelected;
    },

    // Get the list of all servers
    getAllServers(state) {
      return state.servers;
    }
  },

  actions: {
    // Set the list of all servers with "All servers" at index 0
    setServerList(serverList) {
      this.servers = [{ serverIp: appConfig.allServersText }, ...serverList.filter(server => server.serverIp !== 'All servers')];
    },

    // Set the currently selected server
    setCurrentlySelected(serverIp) {
      this.currentlySelected = serverIp;
    }
  }
});
