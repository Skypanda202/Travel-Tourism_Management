import { Navigate } from "react-router-dom";

const ProtectedRoutes = ({
  children,
  adminOnly = false,
}) => {
  const token = localStorage.getItem("token");
  const userRole = localStorage.getItem("role");
  const isAdmin = localStorage.getItem("is_admin") === "true";

  if (!token) {
    return <Navigate to="/login" />;
  }

  if (
    adminOnly &&
    userRole !== "admin" &&
    !isAdmin
  ) {
    return <Navigate to="/" />;
  }

  return children;
};

export default ProtectedRoutes;
