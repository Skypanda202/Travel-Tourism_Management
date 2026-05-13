import {
  BrowserRouter,
  Routes,
  Route,
} from "react-router-dom";

// Layouts
import MainLayout from "../layouts/MainLayout";
import AdminLayout from "../layouts/AdminLayout";

// Home
import Home from "../pages/home/Home";

// Places
import TouristPlaces from "../pages/places/TouristPlaces";
import PlaceDetails from "../pages/places/PlaceDetails";

// Authentication
import Login from "../pages/auth/Login";
import Register from "../pages/auth/Register";

// User Dashboard
import UserDashboard from "../pages/dashboard/UserDashboard";
import Favorites from "../pages/dashboard/Favorites";

// Booking
import CabBooking from "../pages/booking/CabBooking";

// Weather
import WeatherPage from "../pages/weather/WeatherPage";

// Chatbot
import AIChatAssistant from "../pages/chatbot/AIChatAssistant";

// Maps
import MapPage from "../pages/maps/MapPage";

// Admin Pages
import AdminDashboard from "../pages/admin/AdminDashboard";
import AddTouristPlace from "../pages/admin/AddTouristPlace";
import BookingManagement from "../pages/admin/BookingManagement";
import UserManagement from "../pages/admin/UserManagement";
import ReviewsManagement from "../pages/admin/ReviewsManagement";

const AppRoutes = () => {
  return (
    <BrowserRouter>

      <Routes>

        {/* USER ROUTES */}
        <Route
          path="/"
          element={
            <MainLayout>
              <Home />
            </MainLayout>
          }
        />

        <Route
          path="/places"
          element={
            <MainLayout>
              <TouristPlaces />
            </MainLayout>
          }
        />

        <Route
          path="/place/:id"
          element={
            <MainLayout>
              <PlaceDetails />
            </MainLayout>
          }
        />

        <Route
          path="/login"
          element={
            <MainLayout>
              <Login />
            </MainLayout>
          }
        />

        <Route
          path="/register"
          element={
            <MainLayout>
              <Register />
            </MainLayout>
          }
        />

        <Route
          path="/dashboard"
          element={
            <MainLayout>
              <UserDashboard />
            </MainLayout>
          }
        />

        <Route
          path="/favorites"
          element={
            <MainLayout>
              <Favorites />
            </MainLayout>
          }
        />

        <Route
          path="/cab-booking"
          element={
            <MainLayout>
              <CabBooking />
            </MainLayout>
          }
        />

        <Route
          path="/weather"
          element={
            <MainLayout>
              <WeatherPage />
            </MainLayout>
          }
        />

        <Route
          path="/assistant"
          element={
            <MainLayout>
              <AIChatAssistant />
            </MainLayout>
          }
        />

        <Route
          path="/maps"
          element={
            <MainLayout>
              <MapPage />
            </MainLayout>
          }
        />

        {/* ADMIN ROUTES */}

        <Route
          path="/admin"
          element={
            <AdminLayout>
              <AdminDashboard />
            </AdminLayout>
          }
        />

        <Route
          path="/admin/places"
          element={
            <AdminLayout>
              <AddTouristPlace />
            </AdminLayout>
          }
        />

        <Route
          path="/admin/bookings"
          element={
            <AdminLayout>
              <BookingManagement />
            </AdminLayout>
          }
        />

        <Route
          path="/admin/users"
          element={
            <AdminLayout>
              <UserManagement />
            </AdminLayout>
          }
        />

        <Route
          path="/admin/reviews"
          element={
            <AdminLayout>
              <ReviewsManagement />
            </AdminLayout>
          }
        />

      </Routes>

    </BrowserRouter>
  );
};

export default AppRoutes;