import { createSlice } from "@reduxjs/toolkit";

const dashboardSlice = createSlice({
  name: "dashboard",

  initialState: {
    analytics: {},
  },

  reducers: {
    setAnalytics: (state, action) => {
      state.analytics = action.payload;
    },
  },
});

export const { setAnalytics } =
  dashboardSlice.actions;

export default dashboardSlice.reducer;