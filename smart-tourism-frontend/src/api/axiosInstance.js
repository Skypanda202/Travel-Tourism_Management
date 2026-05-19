import axios from "axios";

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL?.replace(/\/?$/, "/") ||
  "http://127.0.0.1:8000/api/";

const PUBLIC_AUTH_ENDPOINTS = [
  "login/",
  "register/",
  "google/",
  "verify-email/",
  "token/refresh/",
];

const isPublicAuthEndpoint = (url = "") => {
  const normalizedUrl = url.replace(/^\/+/, "");
  return PUBLIC_AUTH_ENDPOINTS.some((endpoint) => normalizedUrl === endpoint);
};

const axiosInstance = axios.create({
  baseURL: API_BASE_URL,

  headers: {
    "Content-Type":
      "application/json",
  },

});

// Request Interceptor
axiosInstance.interceptors.request.use(

  (config) => {
    if (isPublicAuthEndpoint(config.url)) {
      delete config.headers.Authorization;
      return config;
    }

    const token =
      localStorage.getItem("token");

    // Attach JWT Token
    if (token) {

      config.headers.Authorization =
        `Bearer ${token}`;
    }

    return config;
  },

  (error) => Promise.reject(error)

);

axiosInstance.interceptors.response.use(
  (response) => response,
  (error) => {
    if (
      error.response?.status === 401 &&
      !isPublicAuthEndpoint(error.config?.url)
    ) {
      localStorage.removeItem("token");
    }

    return Promise.reject(error);
  }
);

export default axiosInstance;
