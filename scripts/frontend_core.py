import os

def write(filepath, content):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Wrote: {filepath}")

# types/index.ts
write("frontend/src/types/index.ts", """
export type UserRole = 
  | 'SUPER_ADMIN'
  | 'PLATFORM_ADMIN'
  | 'ORGANIZATION_ADMIN'
  | 'TEACHER'
  | 'TEACHING_ASSISTANT'
  | 'STUDENT'
  | 'MODERATOR'
  | 'SUPPORT_AGENT';

export interface UserProfile {
  id: string;
  email: string;
  firstName: string;
  lastName: string;
  avatarUrl?: string;
  bio?: string;
  role: UserRole;
  organizationId?: string;
  organizationName?: string;
  permissions: string[];
}

export interface AuthState {
  user: UserProfile | null;
  accessToken: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
}

export interface Course {
  id: string;
  title: string;
  slug: string;
  shortDescription: string;
  description: string;
  thumbnailUrl: string;
  category: string;
  difficulty: 'BEGINNER' | 'INTERMEDIATE' | 'ADVANCED';
  durationMinutes: number;
  price: number;
  currency: string;
  instructorName: string;
  instructorAvatar?: string;
  status: 'DRAFT' | 'IN_REVIEW' | 'PUBLISHED' | 'ARCHIVED';
  rating: number;
  enrolledCount: number;
  sectionsCount: number;
  lessonsCount: number;
}

export interface Section {
  id: string;
  title: string;
  description?: string;
  sequenceOrder: number;
  lessons: Lesson[];
}

export interface Lesson {
  id: string;
  sectionId: string;
  title: string;
  lessonType: 'VIDEO' | 'PDF' | 'TEXT' | 'QUIZ' | 'ASSIGNMENT';
  durationSeconds: number;
  sequenceOrder: number;
  isCompleted?: boolean;
  contentBody?: string;
  mediaUrl?: string;
  isFreePreview?: boolean;
}

export interface AiChatMessage {
  id: string;
  senderType: 'USER' | 'AI' | 'SYSTEM';
  content: string;
  citations?: string[];
  createdAt: string;
  isStreaming?: boolean;
}
""")

# lib/utils.ts
write("frontend/src/lib/utils.ts", """
import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function formatCurrency(amount: number, currency = "USD") {
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency,
  }).format(amount);
}

export function formatDuration(minutes: number): string {
  const hours = Math.floor(minutes / 60);
  const remainingMinutes = minutes % 60;
  if (hours === 0) return `${remainingMinutes}m`;
  return remainingMinutes > 0 ? `${hours}h ${remainingMinutes}m` : `${hours}h`;
}
""")

# lib/axios.ts
write("frontend/src/lib/axios.ts", """
import axios from "axios";

export const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || "/api/v1",
  headers: {
    "Content-Type": "application/json",
  },
  withCredentials: true,
});

apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem("access_token");
  if (token && config.headers) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  const tenantId = localStorage.getItem("tenant_id");
  if (tenantId && config.headers) {
    config.headers["X-Tenant-ID"] = tenantId;
  }
  return config;
});

apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem("access_token");
      // Optional: emit unauthorized event or refresh token
    }
    return Promise.reject(error);
  }
);
""")

# lib/queryClient.ts
write("frontend/src/lib/queryClient.ts", """
import { QueryClient } from "@tanstack/react-query";

export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60 * 5, // 5 minutes
      retry: 1,
      refetchOnWindowFocus: false,
    },
  },
});
""")

# context/AuthContext.tsx
write("frontend/src/context/AuthContext.tsx", """
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
""")

# context/TenantContext.tsx
write("frontend/src/context/TenantContext.tsx", """
import React, { createContext, useContext, useState } from "react";

interface TenantContextType {
  tenantId: string | null;
  tenantName: string | null;
  setTenant: (id: string, name: string) => void;
}

const TenantContext = createContext<TenantContextType | undefined>(undefined);

export const TenantProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [tenantId, setTenantId] = useState<string | null>(null);
  const [tenantName, setTenantName] = useState<string | null>("Global Platform");

  const setTenant = (id: string, name: string) => {
    localStorage.setItem("tenant_id", id);
    setTenantId(id);
    setTenantName(name);
  };

  return (
    <TenantContext.Provider value={{ tenantId, tenantName, setTenant }}>
      {children}
    </TenantContext.Provider>
  );
};

export const useTenant = () => {
  const context = useContext(TenantContext);
  if (!context) throw new Error("useTenant must be used within a TenantProvider");
  return context;
};
""")

# UI Components
write("frontend/src/components/ui/button.tsx", """
import React from "react";
import { cn } from "../../lib/utils";

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "primary" | "secondary" | "outline" | "ghost" | "danger";
  size?: "sm" | "md" | "lg";
  isLoading?: boolean;
}

export const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant = "primary", size = "md", isLoading, children, disabled, ...props }, ref) => {
    const variants = {
      primary: "bg-indigo-600 hover:bg-indigo-500 text-white shadow-sm font-medium",
      secondary: "bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700",
      outline: "border border-slate-700 hover:bg-slate-800 text-slate-300",
      ghost: "hover:bg-slate-800/60 text-slate-300",
      danger: "bg-rose-600 hover:bg-rose-500 text-white",
    };

    const sizes = {
      sm: "px-3 py-1.5 text-xs rounded-md",
      md: "px-4 py-2 text-sm rounded-lg",
      lg: "px-6 py-3 text-base rounded-lg",
    };

    return (
      <button
        ref={ref}
        disabled={disabled || isLoading}
        className={cn(
          "inline-flex items-center justify-center transition-all duration-150 disabled:opacity-50 disabled:cursor-not-allowed select-none",
          variants[variant],
          sizes[size],
          className
        )}
        {...props}
      >
        {isLoading && (
          <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-current" fill="none" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z" />
          </svg>
        )}
        {children}
      </button>
    );
  }
);
""")

write("frontend/src/components/ui/input.tsx", """
import React from "react";
import { cn } from "../../lib/utils";

export interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
}

export const Input = React.forwardRef<HTMLInputElement, InputProps>(
  ({ className, label, error, ...props }, ref) => {
    return (
      <div className="w-full space-y-1.5">
        {label && <label className="text-xs font-medium text-slate-400">{label}</label>}
        <input
          ref={ref}
          className={cn(
            "w-full px-3.5 py-2 bg-slate-900 border border-slate-800 rounded-lg text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/50 focus:border-indigo-500 transition-all",
            error && "border-rose-500 focus:ring-rose-500/50",
            className
          )}
          {...props}
        />
        {error && <p className="text-xs text-rose-400">{error}</p>}
      </div>
    );
  }
);
""")

write("frontend/src/components/ui/card.tsx", """
import React from "react";
import { cn } from "../../lib/utils";

export const Card: React.FC<React.HTMLAttributes<HTMLDivElement>> = ({ className, children, ...props }) => (
  <div className={cn("bg-slate-900/70 backdrop-blur-sm border border-slate-800/80 rounded-xl p-5 shadow-sm", className)} {...props}>
    {children}
  </div>
);
""")

write("frontend/src/components/ui/badge.tsx", """
import React from "react";
import { cn } from "../../lib/utils";

export interface BadgeProps extends React.HTMLAttributes<HTMLSpanElement> {
  variant?: "primary" | "success" | "warning" | "danger" | "neutral";
}

export const Badge: React.FC<BadgeProps> = ({ className, variant = "neutral", children, ...props }) => {
  const variants = {
    primary: "bg-indigo-500/10 text-indigo-400 border-indigo-500/20",
    success: "bg-emerald-500/10 text-emerald-400 border-emerald-500/20",
    warning: "bg-amber-500/10 text-amber-400 border-amber-500/20",
    danger: "bg-rose-500/10 text-rose-400 border-rose-500/20",
    neutral: "bg-slate-800 text-slate-300 border-slate-700",
  };
  return (
    <span className={cn("inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium border", variants[variant], className)} {...props}>
      {children}
    </span>
  );
};
""")

write("frontend/src/components/ui/spinner.tsx", """
import React from "react";
import { cn } from "../../lib/utils";

export const Spinner: React.FC<{ size?: "sm" | "md" | "lg"; className?: string }> = ({ size = "md", className }) => {
  const sizes = { sm: "h-4 w-4", md: "h-6 w-6", lg: "h-8 w-8" };
  return (
    <svg className={cn("animate-spin text-indigo-500", sizes[size], className)} fill="none" viewBox="0 0 24 24">
      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z" />
    </svg>
  );
};
""")

write("frontend/src/components/ui/progress-bar.tsx", """
import React from "react";
import { cn } from "../../lib/utils";

export const ProgressBar: React.FC<{ progress: number; className?: string }> = ({ progress, className }) => {
  const clamped = Math.min(100, Math.max(0, progress));
  return (
    <div className={cn("w-full bg-slate-800 rounded-full h-2 overflow-hidden", className)}>
      <div className="bg-indigo-500 h-2 rounded-full transition-all duration-300" style={{ width: `${clamped}%` }} />
    </div>
  );
};
""")

print("Frontend core libraries and UI components created.")
