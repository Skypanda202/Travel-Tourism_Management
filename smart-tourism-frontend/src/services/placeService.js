import axiosInstance from "../api/axiosInstance";

export const getPlaces = async () => {
  const response = await axiosInstance.get(
    "places/"
  );

  return response.data;
};

export const getPlaceDetails = async (
  id
) => {
  const response = await axiosInstance.get(
    `places/${id}/`
  );

  return response.data;
};