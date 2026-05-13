import axiosInstance from "../api/axiosInstance";

export const addReview = async (
  data
) => {
  const response =
    await axiosInstance.post(
      "reviews/",
      data
    );

  return response.data;
};

export const getReviews =
  async (placeId) => {
    const response =
      await axiosInstance.get(
        `reviews/${placeId}/`
      );

    return response.data;
  };