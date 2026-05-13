import axiosInstance from "../api/axiosInstance";

export const addFavorite = async (
  placeId
) => {
  const response =
    await axiosInstance.post(
      "favorites/",
      {
        place_id: placeId,
      }
    );

  return response.data;
};

export const getFavorites =
  async () => {
    const response =
      await axiosInstance.get(
        "favorites/"
      );

    return response.data;
  };