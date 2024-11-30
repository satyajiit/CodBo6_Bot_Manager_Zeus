import { defineStore } from 'pinia';

export const useLoggerStore = defineStore('loggerStore', {
  state: () => ({
    logs: [] // Array to store all logs
  }),
  actions: {
    // Add a log to the store
    addLog(cmdName, message) {
      const logEntry = {
        cmdName,
        timestamp: Date.now(),
        message
      };
      this.logs.push(logEntry);
    },
    // Clear all logs (if needed)
    clearLogs() {
      this.logs = [];
    }
  },
  getters: {
    getLogs(state) {
      return [...state.logs].sort((a, b) => b.timestamp - a.timestamp);
    }
  }
});
