import React, { createContext, useContext, useState, useEffect } from "react";
import { UserProfile, AuthState } from "../types";

interface AuthContextType extends AuthState {
  login: (token: string, user: UserProfile) => void;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [state, setState] = useState<AuthState>({
    user: {
      id: "usr-demo-123",
      email: "alex.learner@ailms.platform",
      firstName: "Alex",
      lastName: "Learner",
      role: "STUDENT",
      permissions: ["course:read", "ai:tutor:access"],
    },
    accessToken: "demo-token",
    isAuthenticated: true,
    isLoading: false,
  });

  const login = (token: string, user: UserProfile) => {
    localStorage.setItem("access_token", token);
    setState({ user, accessToken: token, isAuthenticated: true, isLoading: false });
  };

  const logout = () => {
    localStorage.removeItem("access_token");
    setState({ user: null, accessToken: null, isAuthenticated: false, isLoading: false });
  };

  return (
    <AuthContext.Provider value={{ ...state, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) throw new Error("useAuth must be used within an AuthProvider");
  return context;
};
