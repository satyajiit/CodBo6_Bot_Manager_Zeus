import axiosInstance from '@/api/axiosInstance';
import { withLogging } from '@/utils/withLogging';

const BotManagerRepository = {
  saveIpAddress(data) {
    const cmdName = '/addServers';
    const requestMessage = 'Adding server IP to the database...';

    //withLogging to handle API call and logging
    return withLogging(cmdName, requestMessage, () =>
      axiosInstance.post(cmdName, data)
    );
  },

  deleteServer(data) {
    const cmdName = '/deleteServer';
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
