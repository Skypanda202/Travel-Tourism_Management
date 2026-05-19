import { Navigate } from "react-router-dom";
import { getStoredUser, isAdminUser } from "../utils/auth";

const ProtectedRoutes = ({
  children,
  adminOnly = false,
}) => {
  const token = localStorage.getItem("token");
  const user = getStoredUser();
  const isAdmin = isAdminUser(user);

  if (!token || !user) {
    return <Navigate to="/login" />;
  }

  if (adminOnly && !isAdmin) {
    return <Navigate to="/" />;
  }

  return children;
};

export default ProtectedRoutes;
