import { useEffect, useState } from "react";

import axiosInstance from "../api/axiosInstance";

const useFetch = (url) => {
  const [data, setData] =
    useState([]);

  const [loading, setLoading] =
    useState(true);

  const [error, setError] =
    useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response =
          await axiosInstance.get(url);

        setData(response.data);
      } catch (err) {
        setError(err);
      }

      setLoading(false);
    };

    fetchData();
  }, [url]);

  return {
    data,
    loading,
    error,
  };
};

export default useFetch;