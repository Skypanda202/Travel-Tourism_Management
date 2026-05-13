import { Navigate } from "react-router-dom";

const ProtectedRoutes = ({
  children,
  adminOnly = false,
}) => {
  const token = localStorage.getItem("token");

  const userRole =
    localStorage.getItem("role");

  if (!token) {
    return <Navigate to="/login" />;
  }

  if (
    adminOnly &&
    userRole !== "admin"
  ) {
    return <Navigate to="/" />;
  }

  return children;
};

export default ProtectedRoutes;