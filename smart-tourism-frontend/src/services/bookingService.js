import axiosInstance from "../api/axiosInstance";

export const createBooking =
  async (data) => {
    const response =
      await axiosInstance.post(
        "bookings/",
        data
      );

    return response.data;
  };

export const getBookings =
  async () => {
    const response =
      await axiosInstance.get(
        "bookings/"
      );

    return response.data;
  };