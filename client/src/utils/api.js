import axios from 'axios';

const BASE = Object.freeze({
  dev : "http://localhost:5000",
  prod : "https://mini-cart-app.onrender.com"
})

export const publicApi = axios.create({
  baseURL: BASE.prod,
  headers: {
    'Content-Type': 'application/json',
  },
});

const api = axios.create({
  baseURL: BASE.prod,
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('access_token');

      if (error.config?.headers?.['X-Login-Request'] !== 'true') {
        const isAdminRoute = window.location.pathname.startsWith('/admin');
        window.location.href = isAdminRoute ? '/admin/login' : '/login';
      }
    } else if (error.response?.status === 422 && error.response?.data?.msg === "Subject must be a string") {
      localStorage.removeItem('access_token');
    }
    return Promise.reject(error);
  }
);

export default api;
