import { useState } from "react";
import AuthContext from "./authContextValue";
import { clearAuthSession, getStoredUser, persistAuthSession } from "../utils/auth";

const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(() => getStoredUser());

  const login = (token, userData = {}) => {
    const nextUser = persistAuthSession(token, userData);
    setUser(nextUser);
    return nextUser;
  };

  const logout = () => {
    clearAuthSession();
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export default AuthProvider;
