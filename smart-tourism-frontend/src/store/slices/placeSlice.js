import { createSlice } from "@reduxjs/toolkit";

const placeSlice = createSlice({
  name: "places",

  initialState: {
    places: [],
    loading: false,
    error: null,
  },

  reducers: {
    fetchPlacesStart: (state) => {
      state.loading = true;
    },

    fetchPlacesSuccess: (state, action) => {
      state.loading = false;
      state.places = action.payload;
    },

    fetchPlacesFailure: (state, action) => {
      state.loading = false;
      state.error = action.payload;
    },
  },
});

export const {
  fetchPlacesStart,
  fetchPlacesSuccess,
  fetchPlacesFailure,
} = placeSlice.actions;

export default placeSlice.reducer;