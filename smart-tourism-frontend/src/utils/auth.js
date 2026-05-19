import { jwtDecode } from "jwt-decode";

export const clearAuthSession = () => {
  localStorage.removeItem("token");
  localStorage.removeItem("role");
  localStorage.removeItem("is_admin");
  localStorage.removeItem("user");
};

export const isAdminUser = (user) =>
  Boolean(
    user?.is_admin ||
      user?.is_staff ||
      user?.is_superuser ||
      user?.role === "admin"
  );

export const persistAuthSession = (token, userData = {}) => {
  const decoded = jwtDecode(token);
  const user = {
    ...decoded,
    ...userData,
  };
  const isAdmin = isAdminUser(user);
  const role = isAdmin ? "admin" : user.role || "visitor";

  localStorage.setItem("token", token);
  localStorage.setItem("role", role);
  localStorage.setItem("is_admin", String(isAdmin));
  localStorage.setItem("user", JSON.stringify({ ...user, role, is_admin: isAdmin }));

  return { ...user, role, is_admin: isAdmin };
};

export const getStoredUser = () => {
  const token = localStorage.getItem("token");
  if (!token) {
    return null;
  }

  try {
    const savedUser = JSON.parse(localStorage.getItem("user") || "{}");
    const decoded = jwtDecode(token);
    const user = { ...decoded, ...savedUser };
    const isAdmin = isAdminUser(user);
    return {
      ...user,
      role: isAdmin ? "admin" : user.role || "visitor",
      is_admin: isAdmin,
    };
  } catch {
    clearAuthSession();
    return null;
  }
};
