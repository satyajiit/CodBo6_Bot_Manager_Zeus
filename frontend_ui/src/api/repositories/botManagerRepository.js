import axiosInstance from '@/api/axiosInstance';


const UserRepository = {
  fetchUsers(params = {}) {
    return axiosInstance.get('/users', { params });
  },

  getUserById(userId) {
    return axiosInstance.get(`/users/${userId}`);
  },

  createUser(data) {
    return axiosInstance.post('/users', data);
  },

  updateUser(userId, data) {
    return axiosInstance.put(`/users/${userId}`, data);
  },

  deleteUser(userId) {
    return axiosInstance.delete(`/users/${userId}`);
  },
};

export default UserRepository;
