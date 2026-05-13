import axiosInstance from "../api/axiosInstance";

export const loginUser = async (data) => {
  const response = await axiosInstance.post(
    "login/",
    data
  );

  return response.data;
};

export const registerUser = async (
  data
) => {
  const response = await axiosInstance.post(
    "register/",
    data
  );

  return response.data;
};