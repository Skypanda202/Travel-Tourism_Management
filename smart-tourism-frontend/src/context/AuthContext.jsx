import { useState } from "react";
import { jwtDecode } from "jwt-decode";
import AuthContext from "./authContextValue";

const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(() => {
    const token = localStorage.getItem("token");

    if (token) {
      try {
        return jwtDecode(token);
      } catch {
        localStorage.removeItem("token");
        localStorage.removeItem("role");
        localStorage.removeItem("is_admin");
      }
    }

    return null;
  });

  const login = (token) => {
    localStorage.setItem("token", token);

    const decoded = jwtDecode(token);
    const isAdmin = decoded.is_admin || decoded.role === "admin";

    localStorage.setItem("role", decoded.role || (isAdmin ? "admin" : "visitor"));
    localStorage.setItem("is_admin", String(isAdmin));

    setUser(decoded);
    return decoded;
  };

  const logout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("role");
    localStorage.removeItem("is_admin");
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export default AuthProvider;
