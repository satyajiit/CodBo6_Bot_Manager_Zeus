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

  fetchServers() {
    const cmdName = '/getServers';
    const requestMessage = 'Fetching server list from the database...';

    return withLogging(cmdName, requestMessage, () =>
      axiosInstance.get(cmdName)
    );
  }
};

export default BotManagerRepository;
