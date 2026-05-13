import axiosInstance from "../api/axiosInstance";

export const sendAIMessage = async (
  message
) => {
  const response =
    await axiosInstance.post(
      "ai/chat/",
      {
        message,
      }
    );

  return response.data;
};