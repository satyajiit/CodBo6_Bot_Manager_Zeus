import axiosInstance from '@/api/axiosInstance';
import { withLogging } from '@/utils/withLogging';

const BotManagerRepository = {

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
    return withLogging(cmdName, requestMessage, () =>
      axiosInstance.post(cmdName, data)
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

    return withLogging(cmdName, requestMessage, () =>
      axiosInstance.get(cmdName)
    );
  },

  sendGamePadCommandsToServers(data) {
    const cmdName = '/sendGamePadCommandToServers';

    console.log(data)

    // Determine the request message based on the servers
    let requestMessage;
    if (data.servers && data.servers.length > 0) {
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

    console.log(data)

    // Determine the request message based on the servers
    let requestMessage;
    if (data.servers && data.servers.length > 0) {
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
