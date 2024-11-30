import axiosInstance from '@/api/axiosInstance';


const BotManagerRepository = {
  saveIpAddress(data) {
    return axiosInstance.post('/addServers', data);
  },
};

export default BotManagerRepository;
