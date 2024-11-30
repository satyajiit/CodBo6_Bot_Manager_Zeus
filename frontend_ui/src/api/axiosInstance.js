import axios from 'axios';
import appConfig from '@/constants/appConfig.json';

const axiosInstance = axios.create({
  baseURL: appConfig.backendUrl,
  timeout: 10000, // 10 seconds
});

axiosInstance.interceptors.request.use(
  (config) => {
      config.headers.Authorization = appConfig.authKey;
    return config;
  },
  (error) => Promise.reject(error)
);

axiosInstance.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error);
    return Promise.reject(error);
  }
);

export default axiosInstance;
