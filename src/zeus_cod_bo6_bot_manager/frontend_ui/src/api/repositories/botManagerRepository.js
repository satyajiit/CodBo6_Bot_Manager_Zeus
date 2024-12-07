import axiosInstance from '@/api/axiosInstance';
import { withLogging } from '@/utils/withLogging';
import { useServerStore } from "@/stores/serverStore.js";
const serverStore = useServerStore();

const BotManagerRepository = {

  tailServerLogs(data) {
    const cmdName = '/tailLogs';
    let requestMessage;
    if (data.servers && data.servers.length === serverStore.servers.length) {
      requestMessage = `Getting logs from "${data.command}" specific servers: ${data.servers.join(', ')}.`;
    } else {
      requestMessage = `Getting logs "${data.command}" from all servers.`;
    }

    return withLogging(cmdName, requestMessage, () =>
      axiosInstance.post(cmdName, data)
    );
  },

  openUrlOnBrowser(data) {
    const cmdName = '/openUrlOnBrowser';
    const requestMessage = 'Opening URL on the browser...';

    return withLogging(cmdName, requestMessage, () =>
      axiosInstance.post(cmdName, data)
    );
  },

  saveIpAddress(data) {
    const cmdName = '/addServers';
    const requestMessage = 'Adding server IP to the database...';

    //withLogging to handle API call and logging
    return withLogging(cmdName, requestMessage, () =>
      axiosInstance.post(cmdName, data)
    );
  },

  fetchServerHealth(data) {
    const cmdName = '/checkServerHealth';
    const requestMessage = 'Checking health of servers';

    //withLogging to handle API call and logging
    return withLogging(cmdName, requestMessage, (() =>
      axiosInstance.post(cmdName, data)), false
    );
  },

  deleteServer(data) {
    const cmdName = '/deleteServers';
    const requestMessage = 'Deleting server IP from the database...';

    return withLogging(cmdName, requestMessage, () =>
      axiosInstance.post(cmdName, data)
    );
  },

  getDeviceHwId() {
    const cmdName = '/getDeviceHwId';
    const requestMessage = 'Fetching device hardware ID...';

    return withLogging(cmdName, requestMessage, () =>
      axiosInstance.get(cmdName)
    );
  },

  copyToClipboard(data) {
    const cmdName = '/copyToClipboard';
    const requestMessage = 'Copying text to clipboard...';

    return withLogging(cmdName, requestMessage, () =>
      axiosInstance.post(cmdName, data)
    );
  },

  fetchServers() {
    const cmdName = '/getServers';
    const requestMessage = 'Fetching server list from the database...';

    return withLogging(cmdName, requestMessage, (() =>
      axiosInstance.get(cmdName)
    ), false);
  },

  sendGamePadCommandsToServers(data) {
    const cmdName = '/sendGamePadCommandToServers';

    console.log(data)

    // Determine the request message based on the servers
    let requestMessage;
    if (data.servers && data.servers.length === serverStore.servers.length) {
      requestMessage = `Sending gamepad command "${data.command}" to specific servers: ${data.servers.join(', ')}.`;
    } else {
      requestMessage = `Sending gamepad command "${data.command}" to all servers.`;
    }

    return withLogging(cmdName, requestMessage, () =>
      axiosInstance.post(cmdName, data)
    );
  } ,

  sendDashboardCommandsToServers(data) {
    const cmdName = '/sendDashboardCommands';
    // Determine the request message based on the servers
    let requestMessage;
    if (data.servers && data.servers.length === serverStore.servers.length) {
      requestMessage = `Sending command "${data.command}" to specific servers: ${data.servers.join(', ')}.`;
    } else {
      requestMessage = `Sending command "${data.command}" to all servers.`;
    }

    return withLogging(cmdName, requestMessage, () =>
      axiosInstance.post(cmdName, data)
    );
  }

};



export default BotManagerRepository;
