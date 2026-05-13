import axios from "axios";

const axiosInstance = axios.create({

  // Environment Variable
  baseURL:
    import.meta.env.VITE_API_BASE_URL,

  headers: {
    "Content-Type":
      "application/json",
  },

});

// Request Interceptor
axiosInstance.interceptors.request.use(

  (config) => {

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

export default axiosInstance;