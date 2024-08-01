import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/api',
});

// Add authentication token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Token ${token}`;
  }
  return config;
});

export const login = async (username, password) => {
  const response = await api.post('/login/', { username, password });
  return response.data;
};

export const getProfile = async () => {
  const response = await api.get('/profile/');
  return response.data;
};

export const updateProfile = async (profileData) => {
  const response = await api.put('/profile/', profileData);
  return response.data;
};

export const getAgreements = async () => {
  const response = await api.get('/agreements/');
  return response.data;
};

export const createAgreement = async (agreementData) => {
  const response = await api.post('/agreements/', agreementData);
  return response.data;
};

export const getTransactions = async () => {
  const response = await api.get('/transactions/');
  return response.data;
};

export default api;