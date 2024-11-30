import { defineStore } from 'pinia';

export const useLoaderStore = defineStore('loader', {
  state: () => ({
    isLoading: false,
    loadingText: 'Loading...', // Default loading text
  }),
  actions: {
    showLoader(text = 'Loading...') {
      this.isLoading = true;
      this.loadingText = text;
    },
    hideLoader() {
      this.isLoading = false;
      this.loadingText = 'Loading...';
    },
  },
});
