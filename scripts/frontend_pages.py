import os

def write(filepath, content):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Wrote: {filepath}")

# Layout: Navbar
write("frontend/src/components/layout/Navbar.tsx", """
import React from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";
import { useTenant } from "../../context/TenantContext";
import { Button } from "../ui/button";
import { Badge } from "../ui/badge";
import { BookOpen, Sparkles, User, LogOut, Shield } from "lucide-react";

export const Navbar: React.FC = () => {
  const { user, isAuthenticated, logout } = useAuth();
  const { tenantName } = useTenant();
  const navigate = useNavigate();

  return (
    <header className="h-16 border-b border-slate-800 bg-slate-950/80 backdrop-blur sticky top-0 z-40 px-6 flex items-center justify-between">
      <div className="flex items-center gap-6">
        <Link to="/" className="flex items-center gap-2.5 text-white font-bold text-lg">
          <div className="h-8 w-8 rounded-lg bg-indigo-600 flex items-center justify-center text-white">
            <Sparkles className="h-4 w-4" />
          </div>
          <span className="bg-clip-text text-transparent bg-gradient-to-r from-white via-slate-200 to-indigo-300">
            AegisLMS
          </span>
        </Link>
        <Badge variant="primary">{tenantName}</Badge>
      </div>

      <nav className="hidden md:flex items-center gap-6 text-sm">
        <Link to="/courses" className="text-slate-400 hover:text-white transition-colors">Catalog</Link>
        <Link to="/dashboard" className="text-slate-400 hover:text-white transition-colors">Dashboard</Link>
        <Link to="/ai-tutor" className="flex items-center gap-1 text-indigo-400 hover:text-indigo-300 transition-colors">
          <Sparkles className="h-3.5 w-3.5" />
          <span>AI Tutor</span>
        </Link>
      </nav>

      <div className="flex items-center gap-3">
        {isAuthenticated && user ? (
          <div className="flex items-center gap-3">
            <div className="text-right hidden sm:block">
              <p className="text-xs font-medium text-white">{user.firstName} {user.lastName}</p>
              <p className="text-[10px] text-slate-400 uppercase tracking-wider">{user.role}</p>
            </div>
            <button 
              onClick={logout}
              title="Sign out"
              className="p-2 rounded-lg hover:bg-slate-800 text-slate-400 hover:text-white transition-colors"
            >
              <LogOut className="h-4 w-4" />
            </button>
          </div>
        ) : (
          <div className="flex items-center gap-2">
            <Button variant="ghost" size="sm" onClick={() => navigate("/login")}>Sign In</Button>
            <Button variant="primary" size="sm" onClick={() => navigate("/register")}>Get Started</Button>
          </div>
        )}
      </div>
    </header>
  );
};
""")

# Layout: Sidebar
write("frontend/src/components/layout/Sidebar.tsx", """
import React from "react";
import { NavLink } from "react-router-dom";
import { BookOpen, LayoutDashboard, Sparkles, GraduationCap, Award, Settings, ShieldCheck, CheckSquare } from "lucide-react";
import { cn } from "../../lib/utils";

export const Sidebar: React.FC = () => {
  const links = [
    { to: "/dashboard", label: "Overview", icon: LayoutDashboard },
    { to: "/courses", label: "Course Catalog", icon: BookOpen },
    { to: "/my-learning", label: "My Learning", icon: GraduationCap },
    { to: "/ai-tutor", label: "AI Tutor Studio", icon: Sparkles },
    { to: "/certificates", label: "Certificates", icon: Award },
    { to: "/admin", label: "Administration", icon: ShieldCheck },
  ];

  return (
    <aside className="w-64 border-r border-slate-800/80 bg-slate-950/40 p-4 space-y-1">
      <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider px-3 mb-2">
        Platform Menu
      </div>
      {links.map((item) => {
        const Icon = item.icon;
        return (
          <NavLink
            key={item.to}
            to={item.to}
            className={({ isActive }) =>
              cn(
                "flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-medium transition-colors",
                isActive
                  ? "bg-indigo-600/10 text-indigo-400 border border-indigo-500/20"
                  : "text-slate-400 hover:text-slate-200 hover:bg-slate-900/60"
              )
            }
          >
            <Icon className="h-4 w-4" />
            <span>{item.label}</span>
          </NavLink>
        );
      })}
    </aside>
  );
};
""")

# Layout: DashboardLayout
write("frontend/src/components/layout/DashboardLayout.tsx", """
import React from "react";
import { Outlet } from "react-router-dom";
import { Navbar } from "./Navbar";
import { Sidebar } from "./Sidebar";

export const DashboardLayout: React.FC = () => {
  return (
    <div className="min-h-screen flex flex-col bg-slate-950 text-slate-100">
      <Navbar />
      <div className="flex flex-1">
        <Sidebar />
        <main className="flex-1 p-8 overflow-y-auto">
          <Outlet />
        </main>
      </div>
    </div>
  );
};
""")

# Services: api.ts
write("frontend/src/services/api.ts", """
import { apiClient } from "../lib/axios";
import { Course, AiChatMessage } from "../types";

export const mockCourses: Course[] = [
  {
    id: "c1",
    title: "Advanced Distributed Systems with Java & Spring Boot",
    slug: "advanced-distributed-systems",
    shortDescription: "Architect resilient, high-throughput cloud applications with Kafka, Redis, and Postgres.",
    description: "Master enterprise SaaS engineering, microservices partitioning, and zero-downtime deployments.",
    thumbnailUrl: "https://images.unsplash.com/photo-1517694712202-14dd9538aa97?w=800&auto=format&fit=crop&q=60",
    category: "Software Engineering",
    difficulty: "ADVANCED",
    durationMinutes: 1440,
    price: 99.00,
    currency: "USD",
    instructorName: "Dr. Elena Rostova",
    status: "PUBLISHED",
    rating: 4.9,
    enrolledCount: 1420,
    sectionsCount: 8,
    lessonsCount: 42,
  },
  {
    id: "c2",
    title: "AI-Powered RAG Architecture & Vector Search",
    slug: "ai-rag-vector-search",
    shortDescription: "Build production RAG pipelines with embeddings, hybrid search, and hallucination guardrails.",
    description: "Deep dive into vector databases, semantic caching, token optimization, and LLM orchestration.",
    thumbnailUrl: "https://images.unsplash.com/photo-1620712943543-bcc4688e7485?w=800&auto=format&fit=crop&q=60",
    category: "Artificial Intelligence",
    difficulty: "INTERMEDIATE",
    durationMinutes: 960,
    price: 129.00,
    currency: "USD",
    instructorName: "Marcus Vance",
    status: "PUBLISHED",
    rating: 4.95,
    enrolledCount: 2850,
    sectionsCount: 6,
    lessonsCount: 30,
  }
];

export const courseService = {
  getCatalog: async (): Promise<Course[]> => {
    return Promise.resolve(mockCourses);
  },
  getCourseById: async (id: string): Promise<Course | undefined> => {
    return Promise.resolve(mockCourses.find(c => c.id === id));
  }
};
""")

# Pages: LoginPage & RegisterPage
write("frontend/src/pages/auth/LoginPage.tsx", """
import React, { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";
import { Button } from "../../components/ui/button";
import { Input } from "../../components/ui/input";
import { Card } from "../../components/ui/card";
import { Sparkles } from "lucide-react";

export const LoginPage: React.FC = () => {
  const [email, setEmail] = useState("alex.learner@ailms.platform");
  const [password, setPassword] = useState("Password@123");
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    login("mock-token", {
      id: "usr-1",
      email,
      firstName: "Alex",
      lastName: "Learner",
      role: "STUDENT",
      permissions: ["course:read"],
    });
    navigate("/dashboard");
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-950 p-4">
      <Card className="w-full max-w-md p-8 border-slate-800 bg-slate-900/90">
        <div className="flex flex-col items-center text-center mb-8">
          <div className="h-12 w-12 rounded-xl bg-indigo-600 flex items-center justify-center text-white mb-3">
            <Sparkles className="h-6 w-6" />
          </div>
          <h1 className="text-2xl font-bold text-white">Welcome Back</h1>
          <p className="text-sm text-slate-400 mt-1">Sign in to your enterprise learning workspace</p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <Input 
            label="Email Address" 
            type="email" 
            value={email} 
            onChange={(e) => setEmail(e.target.value)} 
            required 
          />
          <Input 
            label="Password" 
            type="password" 
            value={password} 
            onChange={(e) => setPassword(e.target.value)} 
            required 
          />
          <Button type="submit" className="w-full mt-2" variant="primary">
            Sign In
          </Button>
        </form>

        <div className="mt-6 text-center text-xs text-slate-500">
          Demo platform initialized with mock security credentials.
        </div>
      </Card>
    </div>
  );
};
""")

write("frontend/src/pages/auth/RegisterPage.tsx", """
import React, { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { Button } from "../../components/ui/button";
import { Input } from "../../components/ui/input";
import { Card } from "../../components/ui/card";
import { Sparkles } from "lucide-react";

export const RegisterPage: React.FC = () => {
  const [email, setEmail] = useState("");
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const navigate = useNavigate();

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    navigate("/login");
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-950 p-4">
      <Card className="w-full max-w-md p-8 border-slate-800 bg-slate-900/90">
        <div className="flex flex-col items-center text-center mb-8">
          <div className="h-12 w-12 rounded-xl bg-indigo-600 flex items-center justify-center text-white mb-3">
            <Sparkles className="h-6 w-6" />
          </div>
          <h1 className="text-2xl font-bold text-white">Create Account</h1>
          <p className="text-sm text-slate-400 mt-1">Start your AI-powered learning journey</p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="grid grid-cols-2 gap-3">
            <Input label="First Name" value={firstName} onChange={e => setFirstName(e.target.value)} required />
            <Input label="Last Name" value={lastName} onChange={e => setLastName(e.target.value)} required />
          </div>
          <Input label="Email Address" type="email" value={email} onChange={e => setEmail(e.target.value)} required />
          <Input label="Password" type="password" required />
          <Button type="submit" className="w-full mt-2" variant="primary">
            Register
          </Button>
        </form>

        <div className="mt-4 text-center text-xs text-slate-400">
          Already have an account? <Link to="/login" className="text-indigo-400 hover:underline">Sign In</Link>
        </div>
      </Card>
    </div>
  );
};
""")

# Dashboard & Pages
write("frontend/src/pages/dashboard/StudentDashboard.tsx", """
import React from "react";
import { Card } from "../../components/ui/card";
import { Badge } from "../../components/ui/badge";
import { Button } from "../../components/ui/button";
import { ProgressBar } from "../../components/ui/progress-bar";
import { BookOpen, Award, Sparkles, Clock, PlayCircle } from "lucide-react";
import { mockCourses } from "../../services/api";
import { useNavigate } from "react-router-dom";

export const StudentDashboard: React.FC = () => {
  const navigate = useNavigate();

  return (
    <div className="space-y-8 max-w-6xl mx-auto">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white">Student Dashboard</h1>
          <p className="text-sm text-slate-400">Track your progress and continue learning</p>
        </div>
        <Button variant="primary" onClick={() => navigate("/ai-tutor")} className="flex items-center gap-2">
          <Sparkles className="h-4 w-4" />
          <span>Launch AI Tutor</span>
        </Button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card className="flex items-center gap-4">
          <div className="p-3 bg-indigo-500/10 text-indigo-400 rounded-xl">
            <BookOpen className="h-6 w-6" />
          </div>
          <div>
            <div className="text-2xl font-bold text-white">2</div>
            <div className="text-xs text-slate-400">Active Enrolled Courses</div>
          </div>
        </Card>

        <Card className="flex items-center gap-4">
          <div className="p-3 bg-emerald-500/10 text-emerald-400 rounded-xl">
            <Award className="h-6 w-6" />
          </div>
          <div>
            <div className="text-2xl font-bold text-white">1</div>
            <div className="text-xs text-slate-400">Certificates Earned</div>
          </div>
        </Card>

        <Card className="flex items-center gap-4">
          <div className="p-3 bg-amber-500/10 text-amber-400 rounded-xl">
            <Clock className="h-6 w-6" />
          </div>
          <div>
            <div className="text-2xl font-bold text-white">18.5 hrs</div>
            <div className="text-xs text-slate-400">Total Learning Time</div>
          </div>
        </Card>
      </div>

      <div className="space-y-4">
        <h2 className="text-lg font-semibold text-white">Continue Learning</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {mockCourses.map(course => (
            <Card key={course.id} className="space-y-4">
              <div className="flex items-start justify-between">
                <div>
                  <Badge variant="primary">{course.category}</Badge>
                  <h3 className="text-base font-semibold text-white mt-2">{course.title}</h3>
                </div>
              </div>
              <div className="space-y-2">
                <div className="flex justify-between text-xs text-slate-400">
                  <span>Progress</span>
                  <span>45% Completed</span>
                </div>
                <ProgressBar progress={45} />
              </div>
              <Button variant="secondary" size="sm" onClick={() => navigate(`/learn/${course.id}/lesson-1`)} className="w-full flex items-center justify-center gap-2">
                <PlayCircle className="h-4 w-4" />
                <span>Resume Course</span>
              </Button>
            </Card>
          ))}
        </div>
      </div>
    </div>
  );
};
""")

write("frontend/src/pages/courses/CourseCatalogPage.tsx", """
import React from "react";
import { mockCourses } from "../../services/api";
import { Card } from "../../components/ui/card";
import { Badge } from "../../components/ui/badge";
import { Button } from "../../components/ui/button";
import { formatCurrency, formatDuration } from "../../lib/utils";
import { Clock, Star, Users } from "lucide-react";
import { useNavigate } from "react-router-dom";

export const CourseCatalogPage: React.FC = () => {
  const navigate = useNavigate();

  return (
    <div className="space-y-8 max-w-6xl mx-auto">
      <div>
        <h1 className="text-2xl font-bold text-white">Explore Course Catalog</h1>
        <p className="text-sm text-slate-400">Curated enterprise courses with AI-grounded tutoring</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {mockCourses.map((course) => (
          <Card key={course.id} className="flex flex-col justify-between overflow-hidden p-0 border-slate-800">
            <img src={course.thumbnailUrl} alt={course.title} className="h-44 w-full object-cover" />
            <div className="p-5 flex-1 flex flex-col justify-between space-y-4">
              <div>
                <div className="flex items-center justify-between mb-2">
                  <Badge variant="primary">{course.category}</Badge>
                  <span className="text-xs font-semibold text-indigo-400">{course.difficulty}</span>
                </div>
                <h3 className="font-semibold text-white text-base line-clamp-2">{course.title}</h3>
                <p className="text-xs text-slate-400 mt-2 line-clamp-2">{course.shortDescription}</p>
              </div>

              <div className="pt-4 border-t border-slate-800 flex items-center justify-between text-xs text-slate-400">
                <span className="flex items-center gap-1"><Clock className="h-3.5 w-3.5" /> {formatDuration(course.durationMinutes)}</span>
                <span className="flex items-center gap-1"><Star className="h-3.5 w-3.5 text-amber-400 fill-amber-400" /> {course.rating}</span>
                <span className="text-base font-bold text-white">{formatCurrency(course.price)}</span>
              </div>

              <Button variant="primary" size="sm" onClick={() => navigate(`/learn/${course.id}/lesson-1`)} className="w-full">
                Enroll Now
              </Button>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
};
""")

write("frontend/src/pages/learn/LearningPlayerPage.tsx", """
import React, { useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { Card } from "../../components/ui/card";
import { Button } from "../../components/ui/button";
import { Badge } from "../../components/ui/badge";
import { ProgressBar } from "../../components/ui/progress-bar";
import { PlayCircle, CheckCircle, ChevronLeft, ChevronRight, Sparkles, FileText } from "lucide-react";

export const LearningPlayerPage: React.FC = () => {
  const { courseId, lessonId } = useParams();
  const navigate = useNavigate();
  const [completed, setCompleted] = useState(false);

  return (
    <div className="min-h-screen bg-slate-950 flex flex-col text-slate-100">
      {/* Header */}
      <header className="h-14 border-b border-slate-800 bg-slate-900/60 px-6 flex items-center justify-between">
        <button onClick={() => navigate("/dashboard")} className="flex items-center gap-2 text-xs text-slate-400 hover:text-white">
          <ChevronLeft className="h-4 w-4" /> Back to Dashboard
        </button>
        <span className="text-sm font-medium text-white">Lesson 1: Architecture Overview</span>
        <Button variant="primary" size="sm" onClick={() => navigate("/ai-tutor")} className="flex items-center gap-1.5 text-xs">
          <Sparkles className="h-3.5 w-3.5" /> Ask AI Tutor
        </Button>
      </header>

      {/* Main Player Grid */}
      <div className="flex-1 flex flex-col lg:flex-row">
        {/* Content View */}
        <div className="flex-1 p-6 space-y-6">
          <div className="aspect-video bg-slate-900 rounded-xl border border-slate-800 flex items-center justify-center">
            <div className="text-center space-y-2">
              <PlayCircle className="h-16 w-16 text-indigo-500 mx-auto" />
              <p className="text-sm text-slate-400">Enterprise High-Throughput Video Stream Player</p>
            </div>
          </div>

          <div className="flex items-center justify-between">
            <Button variant="outline" size="sm"><ChevronLeft className="h-4 w-4 mr-1" /> Previous Lesson</Button>
            <Button 
              variant={completed ? "secondary" : "primary"} 
              size="sm"
              onClick={() => setCompleted(!completed)}
            >
              {completed ? "Completed" : "Mark as Complete"}
            </Button>
            <Button variant="outline" size="sm">Next Lesson <ChevronRight className="h-4 w-4 ml-1" /></Button>
          </div>
        </div>

        {/* Sidebar Syllabus */}
        <div className="w-full lg:w-80 border-l border-slate-800 bg-slate-900/30 p-4 space-y-4">
          <h3 className="text-sm font-semibold text-white">Course Syllabus</h3>
          <div className="space-y-2 text-xs">
            <div className="p-2.5 rounded-lg bg-indigo-600/20 text-indigo-300 border border-indigo-500/30 flex items-center gap-2">
              <PlayCircle className="h-4 w-4" />
              <span>1. System Architecture Overview</span>
            </div>
            <div className="p-2.5 rounded-lg bg-slate-900 text-slate-400 hover:text-white flex items-center gap-2">
              <FileText className="h-4 w-4" />
              <span>2. Multi-Tenant Partitioning</span>
            </div>
            <div className="p-2.5 rounded-lg bg-slate-900 text-slate-400 hover:text-white flex items-center gap-2">
              <FileText className="h-4 w-4" />
              <span>3. Vector Search & RAG</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
""")

write("frontend/src/pages/tutor/AiTutorPage.tsx", """
import React, { useState } from "react";
import { Card } from "../../components/ui/card";
import { Button } from "../../components/ui/button";
import { Input } from "../../components/ui/input";
import { Badge } from "../../components/ui/badge";
import { Sparkles, Send, BookOpen, ShieldCheck } from "lucide-react";
import { AiChatMessage } from "../../types";

export const AiTutorPage: React.FC = () => {
  const [messages, setMessages] = useState<AiChatMessage[]>([
    {
      id: "m1",
      senderType: "AI",
      content: "Hello! I am your AI Course Assistant. I am grounded in your enrolled course documents. Ask me anything about distributed architectures, RAG, or quiz topics!",
      citations: ["Course Overview - Section 1"],
      createdAt: new Date().toISOString(),
    },
  ]);
  const [input, setInput] = useState("");

  const handleSend = (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMsg: AiChatMessage = {
      id: `usr-${Date.now()}`,
      senderType: "USER",
      content: input,
      createdAt: new Date().toISOString(),
    };

    const aiReply: AiChatMessage = {
      id: `ai-${Date.now()}`,
      senderType: "AI",
      content: `Based on your course materials on "${input}": Distributed caching with Redis and tenant-partitioned JPA repositories ensure sub-10ms query execution and strict isolation.`,
      citations: ["Advanced Distributed Systems - Module 2, Page 14"],
      createdAt: new Date().toISOString(),
    };

    setMessages(prev => [...prev, userMsg, aiReply]);
    setInput("");
  };

  return (
    <div className="max-w-4xl mx-auto h-[calc(100vh-8rem)] flex flex-col space-y-4">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="h-9 w-9 rounded-lg bg-indigo-600/20 text-indigo-400 flex items-center justify-center">
            <Sparkles className="h-5 w-5" />
          </div>
          <div>
            <h1 className="text-lg font-bold text-white">AI Tutor Studio</h1>
            <p className="text-xs text-slate-400">Contextual RAG Assistant & Socratic Mentor</p>
          </div>
        </div>
        <Badge variant="success" className="flex items-center gap-1">
          <ShieldCheck className="h-3.5 w-3.5" />
          <span>Grounded in Course Material</span>
        </Badge>
      </div>

      <Card className="flex-1 flex flex-col overflow-hidden p-4 border-slate-800 bg-slate-900/60">
        <div className="flex-1 overflow-y-auto space-y-4 pr-2">
          {messages.map(msg => (
            <div key={msg.id} className={`flex ${msg.senderType === "USER" ? "justify-end" : "justify-start"}`}>
              <div className={`max-w-[80%] rounded-xl p-4 text-sm ${
                msg.senderType === "USER" 
                  ? "bg-indigo-600 text-white" 
                  : "bg-slate-800/80 text-slate-200 border border-slate-700/60"
              }`}>
                <p className="leading-relaxed">{msg.content}</p>
                {msg.citations && msg.citations.length > 0 && (
                  <div className="mt-3 pt-2 border-t border-slate-700/40 text-[11px] text-indigo-300 flex items-center gap-1.5">
                    <BookOpen className="h-3.5 w-3.5" />
                    <span>Citation: {msg.citations.join(", ")}</span>
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>

        <form onSubmit={handleSend} className="pt-4 border-t border-slate-800 flex gap-2">
          <Input 
            value={input} 
            onChange={e => setInput(e.target.value)} 
            placeholder="Ask a concept question, request a quiz hint, or summarize a topic..." 
            className="flex-1"
          />
          <Button type="submit" variant="primary" className="px-5">
            <Send className="h-4 w-4" />
          </Button>
        </form>
      </Card>
    </div>
  );
};
""")

# App.tsx & main.tsx
write("frontend/src/App.tsx", """
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
""")

write("frontend/src/main.tsx", """
import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";
import "./index.css";

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
""")

print("Frontend pages and application routing created.")
