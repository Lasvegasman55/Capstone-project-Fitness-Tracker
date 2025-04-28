// services/api.js
import axios from 'axios';

// Replace with your Django API URL
const API_URL = 'http://10.0.2.2:8000/api';  // 10.0.2.2 points to localhost on Android emulator

// Create an axios instance with default config
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add a request interceptor to include the auth token in requests
api.interceptors.request.use(
  config => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  error => {
    return Promise.reject(error);
  }
);

// API endpoint functions
export const authAPI = {
  login: (username, password) => api.post('/token/', { username, password }),
  register: (userData) => api.post('/register/', userData),
};

export const workoutsAPI = {
  getWorkouts: () => api.get('/workouts/'),
  getWorkout: (id) => api.get(`/workouts/${id}/`),
  createWorkout: (data) => api.post('/workouts/', data),
  updateWorkout: (id, data) => api.put(`/workouts/${id}/`, data),
  deleteWorkout: (id) => api.delete(`/workouts/${id}/`),
};

export const fastingAPI = {
  getFastingSessions: () => api.get('/fasting-sessions/'),
  getActiveSession: () => api.get('/fasting-sessions/?is_active=true'),
  startFasting: (data) => api.post('/fasting-sessions/', data),
  endFasting: (id, data) => api.put(`/fasting-sessions/${id}/`, data),
};

export default api;