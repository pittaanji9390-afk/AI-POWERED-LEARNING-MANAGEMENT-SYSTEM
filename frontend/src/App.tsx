import React from "react";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { QueryClientProvider } from "@tanstack/react-query";
import { queryClient } from "./lib/queryClient";
import { AuthProvider } from "./context/AuthContext";
import { TenantProvider } from "./context/TenantContext";

import { DashboardLayout } from "./components/layout/DashboardLayout";
import { LoginPage } from "./pages/auth/LoginPage";
import { RegisterPage } from "./pages/auth/RegisterPage";
import { StudentDashboard } from "./pages/dashboard/StudentDashboard";
import { CourseCatalogPage } from "./pages/courses/CourseCatalogPage";
import { LearningPlayerPage } from "./pages/learn/LearningPlayerPage";
import { AiTutorPage } from "./pages/tutor/AiTutorPage";

export const App: React.FC = () => {
  return (
    <QueryClientProvider client={queryClient}>
      <AuthProvider>
        <TenantProvider>
          <BrowserRouter>
            <Routes>
              <Route path="/login" element={<LoginPage />} />
              <Route path="/register" element={<RegisterPage />} />
              <Route path="/learn/:courseId/:lessonId" element={<LearningPlayerPage />} />

              <Route element={<DashboardLayout />}>
                <Route path="/" element={<Navigate to="/dashboard" replace />} />
                <Route path="/dashboard" element={<StudentDashboard />} />
                <Route path="/courses" element={<CourseCatalogPage />} />
                <Route path="/ai-tutor" element={<AiTutorPage />} />
                <Route path="/my-learning" element={<StudentDashboard />} />
                <Route path="/certificates" element={<StudentDashboard />} />
                <Route path="/admin" element={<StudentDashboard />} />
              </Route>
            </Routes>
          </BrowserRouter>
        </TenantProvider>
      </AuthProvider>
    </QueryClientProvider>
  );
};

export default App;
