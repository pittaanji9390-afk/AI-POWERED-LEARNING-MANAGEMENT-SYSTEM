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
import { TeacherDashboard } from "./pages/teacher/TeacherDashboard";
import { CourseBuilderPage } from "./pages/courses/CourseBuilderPage";
import { AdminDashboard } from "./pages/admin/AdminDashboard";
import { CertificateVerifyPage } from "./pages/courses/CertificateVerifyPage";
import { DiscussionBoardPage } from "./pages/courses/DiscussionBoardPage";
import { QuizPlayerPage } from "./pages/courses/QuizPlayerPage";
import { LearningPathPage } from "./pages/learn/LearningPathPage";
import { PricingPlansPage } from "./pages/payment/PricingPlansPage";
import { CodingLabPage } from "./pages/learn/CodingLabPage";
import { AssignmentSubmissionPage } from "./pages/learn/AssignmentSubmissionPage";

export const App: React.FC = () => {
  return (
    <QueryClientProvider client={queryClient}>
      <AuthProvider>
        <TenantProvider>
          <BrowserRouter>
            <Routes>
              {/* Public Routes */}
              <Route path="/login" element={<LoginPage />} />
              <Route path="/register" element={<RegisterPage />} />
              <Route path="/certificates/verify/:verificationCode" element={<CertificateVerifyPage />} />
              <Route path="/learn/:courseId/:lessonId" element={<LearningPlayerPage />} />
              <Route path="/quizzes/:quizId/take" element={<QuizPlayerPage />} />
              <Route path="/assignments/:id/submit" element={<AssignmentSubmissionPage />} />

              {/* Main Authenticated Layout */}
              <Route element={<DashboardLayout />}>
                <Route path="/" element={<Navigate to="/dashboard" replace />} />
                <Route path="/dashboard" element={<StudentDashboard />} />
                <Route path="/courses" element={<CourseCatalogPage />} />
                <Route path="/pricing" element={<PricingPlansPage />} />
                <Route path="/learning-path" element={<LearningPathPage />} />
                <Route path="/lab" element={<CodingLabPage />} />
                <Route path="/ai-tutor" element={<AiTutorPage />} />
                <Route path="/discussions" element={<DiscussionBoardPage />} />
                <Route path="/my-learning" element={<StudentDashboard />} />
                <Route path="/certificates" element={<StudentDashboard />} />

                {/* Teacher Routes */}
                <Route path="/teacher" element={<TeacherDashboard />} />
                <Route path="/courses/create" element={<CourseBuilderPage />} />
                <Route path="/courses/:id/edit" element={<CourseBuilderPage />} />
                <Route path="/teacher/grading" element={<TeacherDashboard />} />

                {/* Admin Routes */}
                <Route path="/admin" element={<AdminDashboard />} />
              </Route>
            </Routes>
          </BrowserRouter>
        </TenantProvider>
      </AuthProvider>
    </QueryClientProvider>
  );
};

export default App;
