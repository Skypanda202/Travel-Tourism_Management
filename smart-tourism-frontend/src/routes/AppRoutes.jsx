import {
  BrowserRouter,
  Routes,
  Route,
} from "react-router-dom";

// Layouts
import MainLayout from "../layouts/MainLayout";
import AdminLayout from "../layouts/AdminLayout";
import ProtectedRoutes from "./ProtectedRoutes";

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
// import WeatherPage from "../pages/weather/WeatherPage";

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
import CabManagement from "../pages/admin/CabManagement";
import RevenueDashboard from "../pages/admin/RevenueDashboard";

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
              <ProtectedRoutes>
                <UserDashboard />
              </ProtectedRoutes>
            </MainLayout>
          }
        />

        <Route
          path="/favorites"
          element={
            <MainLayout>
              <ProtectedRoutes>
                <Favorites />
              </ProtectedRoutes>
            </MainLayout>
          }
        />

        <Route
          path="/cab-booking"
          element={
            <MainLayout>
              <ProtectedRoutes>
                <CabBooking />
              </ProtectedRoutes>
            </MainLayout>
          }
        />

        {/* <Route
          path="/weather"
          element={
            <MainLayout>
              <WeatherPage />
            </MainLayout>
          }
        /> */}

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
            <ProtectedRoutes adminOnly>
              <AdminLayout>
                <AdminDashboard />
              </AdminLayout>
            </ProtectedRoutes>
          }
        />

        <Route
          path="/admin/places"
          element={
            <ProtectedRoutes adminOnly>
              <AdminLayout>
                <AddTouristPlace />
              </AdminLayout>
            </ProtectedRoutes>
          }
        />

        <Route
          path="/admin/bookings"
          element={
            <ProtectedRoutes adminOnly>
              <AdminLayout>
                <BookingManagement />
              </AdminLayout>
            </ProtectedRoutes>
          }
        />

        <Route
          path="/admin/users"
          element={
            <ProtectedRoutes adminOnly>
              <AdminLayout>
                <UserManagement />
              </AdminLayout>
            </ProtectedRoutes>
          }
        />

        <Route
          path="/admin/reviews"
          element={
            <ProtectedRoutes adminOnly>
              <AdminLayout>
                <ReviewsManagement />
              </AdminLayout>
            </ProtectedRoutes>
          }
        />

        <Route
          path="/admin/cabs"
          element={
            <ProtectedRoutes adminOnly>
              <AdminLayout>
                <CabManagement />
              </AdminLayout>
            </ProtectedRoutes>
          }
        />

        <Route
          path="/admin/revenue"
          element={
            <ProtectedRoutes adminOnly>
              <AdminLayout>
                <RevenueDashboard />
              </AdminLayout>
            </ProtectedRoutes>
          }
        />

      </Routes>

    </BrowserRouter>
  );
};

export default AppRoutes;
