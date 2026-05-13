import { configureStore } from "@reduxjs/toolkit";

import authReducer from "./slices/authSlice";
import placeReducer from "./slices/placeSlice";
import bookingReducer from "./slices/bookingSlice";
import dashboardReducer from "./slices/dashboardSlice";

const store = configureStore({
  reducer: {
    auth: authReducer,
    places: placeReducer,
    bookings: bookingReducer,
    dashboard: dashboardReducer,
  },
});

export default store;