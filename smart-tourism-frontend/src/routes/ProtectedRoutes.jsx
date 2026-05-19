import { Navigate } from "react-router-dom";
import { useEffect, useState } from "react";
import axiosInstance from "../api/axiosInstance";
import { getStoredUser, isAdminUser } from "../utils/auth";

const ProtectedRoutes = ({
  children,
  adminOnly = false,
}) => {
  const [serverUser, setServerUser] = useState(null);
  const [checkingServerUser, setCheckingServerUser] = useState(adminOnly);
  const token = localStorage.getItem("token");
  const user = getStoredUser();
  const isAdmin = isAdminUser(serverUser || user);

  useEffect(() => {
    let active = true;

    const verifyAdmin = async () => {
      if (!adminOnly || !token || isAdminUser(user)) {
        setCheckingServerUser(false);
        return;
      }

      try {
        const response = await axiosInstance.get("users/profile/");
        const nextUser = response.data.data || null;
        if (!active) {
          return;
        }

        setServerUser(nextUser);
        if (isAdminUser(nextUser)) {
          localStorage.setItem("role", "admin");
          localStorage.setItem("is_admin", "true");
          localStorage.setItem("user", JSON.stringify({ ...nextUser, role: "admin", is_admin: true }));
        }
      } catch {
        if (active) {
          setServerUser(null);
        }
      } finally {
        if (active) {
          setCheckingServerUser(false);
        }
      }
    };

    verifyAdmin();

    return () => {
      active = false;
    };
  }, [adminOnly, token, user]);

  if (!token || !user) {
    return <Navigate to="/login" />;
  }

  if (adminOnly && checkingServerUser) {
    return null;
  }

  if (adminOnly && !isAdmin) {
    return <Navigate to="/" />;
  }

  return children;
};

export default ProtectedRoutes;
