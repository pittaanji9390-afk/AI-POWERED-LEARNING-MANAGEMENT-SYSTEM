import os

def write(filepath, content):
    dirpath = os.path.dirname(filepath)
    if dirpath:
        os.makedirs(dirpath, exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Wrote: {filepath}")

# Teacher Dashboard
write("frontend/src/pages/teacher/TeacherDashboard.tsx", """
import React from "react";
import { Card } from "../../components/ui/card";
import { Button } from "../../components/ui/button";
import { Badge } from "../../components/ui/badge";
import { BookOpen, Users, PlusCircle, Sparkles, CheckCircle2, TrendingUp } from "lucide-react";
import { useNavigate } from "react-router-dom";
import { mockCourses } from "../../services/api";

export const TeacherDashboard: React.FC = () => {
  const navigate = useNavigate();

  return (
    <div className="space-y-8 max-w-6xl mx-auto">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white">Teacher Studio</h1>
          <p className="text-sm text-slate-400">Manage your courses, AI quizzes, and student evaluations</p>
        </div>
        <div className="flex items-center gap-3">
          <Button variant="outline" onClick={() => navigate("/courses/create")} className="flex items-center gap-2">
            <PlusCircle className="h-4 w-4" />
            <span>Create Course</span>
          </Button>
          <Button variant="primary" onClick={() => navigate("/courses/create?ai=true")} className="flex items-center gap-2">
            <Sparkles className="h-4 w-4" />
            <span>AI Course Assistant</span>
          </Button>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card className="p-4">
          <div className="text-xs text-slate-400">Total Courses</div>
          <div className="text-2xl font-bold text-white mt-1">4</div>
        </Card>
        <Card className="p-4">
          <div className="text-xs text-slate-400">Active Students</div>
          <div className="text-2xl font-bold text-white mt-1">4,270</div>
        </Card>
        <Card className="p-4">
          <div className="text-xs text-slate-400">Pending Grading</div>
          <div className="text-2xl font-bold text-amber-400 mt-1">12</div>
        </Card>
        <Card className="p-4">
          <div className="text-xs text-slate-400">Avg Completion Rate</div>
          <div className="text-2xl font-bold text-emerald-400 mt-1">78.4%</div>
        </Card>
      </div>

      <div className="space-y-4">
        <h2 className="text-lg font-semibold text-white">Your Courses</h2>
        <div className="space-y-3">
          {mockCourses.map((c) => (
            <Card key={c.id} className="flex items-center justify-between p-4">
              <div className="flex items-center gap-4">
                <img src={c.thumbnailUrl} alt={c.title} className="h-14 w-20 object-cover rounded-lg" />
                <div>
                  <div className="flex items-center gap-2">
                    <h3 className="font-semibold text-white text-sm">{c.title}</h3>
                    <Badge variant="success">{c.status}</Badge>
                  </div>
                  <div className="text-xs text-slate-400 mt-1 flex items-center gap-4">
                    <span>{c.enrolledCount} learners</span>
                    <span>{c.lessonsCount} lessons</span>
                    <span>Rating: {c.rating}</span>
                  </div>
                </div>
              </div>
              <div className="flex items-center gap-2">
                <Button variant="secondary" size="sm" onClick={() => navigate(`/courses/${c.id}/edit`)}>
                  Edit Curriculum
                </Button>
                <Button variant="outline" size="sm" onClick={() => navigate(`/teacher/grading`)}>
                  Submissions
                </Button>
              </div>
            </Card>
          ))}
        </div>
      </div>
    </div>
  );
};
""")

# Course Builder Page
write("frontend/src/pages/courses/CourseBuilderPage.tsx", """
import React, { useState } from "react";
import { Card } from "../../components/ui/card";
import { Button } from "../../components/ui/button";
import { Input } from "../../components/ui/input";
import { Badge } from "../../components/ui/badge";
import { Plus, Trash2, GripVertical, Sparkles, Video, FileText, CheckCircle } from "lucide-react";
import { useNavigate } from "react-router-dom";

export const CourseBuilderPage: React.FC = () => {
  const navigate = useNavigate();
  const [sections, setSections] = useState([
    {
      id: "sec-1",
      title: "Module 1: High-Performance Architecture",
      lessons: [
        { id: "les-1", title: "1.1 System Architecture Deep-Dive", type: "VIDEO", duration: "18m" },
        { id: "les-2", title: "1.2 Database Partitioning & Vector Storage", type: "PDF", duration: "12m" },
      ],
    },
    {
      id: "sec-2",
      title: "Module 2: AI Retrieval-Augmented Generation",
      lessons: [
        { id: "les-3", title: "2.1 Semantic Search with pgvector", type: "VIDEO", duration: "24m" },
        { id: "les-4", title: "2.2 Module 2 Knowledge Assessment", type: "QUIZ", duration: "15m" },
      ],
    },
  ]);

  const [aiPrompt, setAiPrompt] = useState("");
  const [isGenerating, setIsGenerating] = useState(false);

  const handleAiGenerate = () => {
    setIsGenerating(true);
    setTimeout(() => {
      setSections(prev => [
        ...prev,
        {
          id: `sec-${Date.now()}`,
          title: "Module 3: AI-Generated Advanced Microservices",
          lessons: [
            { id: `les-${Date.now()}-1`, title: "3.1 Event-Driven Messaging with RabbitMQ", type: "VIDEO", duration: "20m" },
            { id: `les-${Date.now()}-2`, title: "3.2 Distributed Transactions & Sagas", type: "PDF", duration: "15m" },
          ],
        },
      ]);
      setIsGenerating(false);
      setAiPrompt("");
    }, 1000);
  };

  return (
    <div className="space-y-6 max-w-5xl mx-auto">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white">Course Curriculum Builder</h1>
          <p className="text-sm text-slate-400">Design sections, interactive lessons, and AI assessments</p>
        </div>
        <div className="flex items-center gap-3">
          <Button variant="outline" onClick={() => navigate("/teacher")}>Save Draft</Button>
          <Button variant="primary">Publish Course</Button>
        </div>
      </div>

      {/* AI Curriculum Generator Card */}
      <Card className="border-indigo-500/30 bg-indigo-950/20 p-5 space-y-3">
        <div className="flex items-center gap-2 text-indigo-400 font-semibold text-sm">
          <Sparkles className="h-4 w-4" />
          <span>AI Curriculum Generator</span>
        </div>
        <p className="text-xs text-slate-400">
          Enter a topic or syllabus outline and let the AI generate modules, video outlines, and quiz questions.
        </p>
        <div className="flex gap-2">
          <Input 
            placeholder="e.g. Distributed Consensus, Raft Algorithm, and Fault Tolerance..." 
            value={aiPrompt}
            onChange={(e) => setAiPrompt(e.target.value)}
          />
          <Button variant="primary" isLoading={isGenerating} onClick={handleAiGenerate}>
            Generate
          </Button>
        </div>
      </Card>

      {/* Section List */}
      <div className="space-y-4">
        {sections.map((section, sIdx) => (
          <Card key={section.id} className="p-5 space-y-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <GripVertical className="h-4 w-4 text-slate-500 cursor-move" />
                <h3 className="font-semibold text-white text-base">{section.title}</h3>
              </div>
              <Button variant="ghost" size="sm" className="text-slate-400 hover:text-rose-400">
                <Trash2 className="h-4 w-4" />
              </Button>
            </div>

            <div className="pl-6 space-y-2">
              {section.lessons.map((lesson) => (
                <div key={lesson.id} className="flex items-center justify-between p-3 bg-slate-950/50 rounded-lg border border-slate-800/80">
                  <div className="flex items-center gap-3">
                    {lesson.type === "VIDEO" ? <Video className="h-4 w-4 text-indigo-400" /> : <FileText className="h-4 w-4 text-emerald-400" />}
                    <span className="text-sm text-slate-200">{lesson.title}</span>
                    <Badge variant="neutral">{lesson.type}</Badge>
                  </div>
                  <span className="text-xs text-slate-500">{lesson.duration}</span>
                </div>
              ))}
              <Button variant="secondary" size="sm" className="w-full mt-2 flex items-center justify-center gap-1.5 text-xs">
                <Plus className="h-3.5 w-3.5" /> Add Lesson
              </Button>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
};
""")

# Admin Dashboard
write("frontend/src/pages/admin/AdminDashboard.tsx", """
import React from "react";
import { Card } from "../../components/ui/card";
import { Badge } from "../../components/ui/badge";
import { Button } from "../../components/ui/button";
import { Users, Building, ShieldAlert, DollarSign, Activity, Cpu } from "lucide-react";

export const AdminDashboard: React.FC = () => {
  return (
    <div className="space-y-8 max-w-6xl mx-auto">
      <div>
        <h1 className="text-2xl font-bold text-white">Platform Administration</h1>
        <p className="text-sm text-slate-400">Multi-tenant management, AI compute health, and platform governance</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card className="p-5 flex items-center gap-4">
          <div className="p-3 bg-indigo-500/10 text-indigo-400 rounded-xl">
            <Building className="h-6 w-6" />
          </div>
          <div>
            <div className="text-2xl font-bold text-white">18</div>
            <div className="text-xs text-slate-400">Active Organizations</div>
          </div>
        </Card>

        <Card className="p-5 flex items-center gap-4">
          <div className="p-3 bg-emerald-500/10 text-emerald-400 rounded-xl">
            <DollarSign className="h-6 w-6" />
          </div>
          <div>
            <div className="text-2xl font-bold text-white">$48,290</div>
            <div className="text-xs text-slate-400">Monthly SaaS ARR</div>
          </div>
        </Card>

        <Card className="p-5 flex items-center gap-4">
          <div className="p-3 bg-purple-500/10 text-purple-400 rounded-xl">
            <Cpu className="h-6 w-6" />
          </div>
          <div>
            <div className="text-2xl font-bold text-white">1.2M</div>
            <div className="text-xs text-slate-400">AI Tokens Processed Today</div>
          </div>
        </Card>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Card className="space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="font-semibold text-white text-base">Tenant Organizations</h3>
            <Badge variant="primary">18 Live</Badge>
          </div>
          <div className="space-y-2 text-sm">
            <div className="p-3 bg-slate-950/60 rounded-lg flex items-center justify-between border border-slate-800">
              <div>
                <p className="font-medium text-white">Acme University</p>
                <p className="text-xs text-slate-500">Tier: ENTERPRISE (1,500 seats)</p>
              </div>
              <Badge variant="success">Active</Badge>
            </div>
            <div className="p-3 bg-slate-950/60 rounded-lg flex items-center justify-between border border-slate-800">
              <div>
                <p className="font-medium text-white">TechCorp Academy</p>
                <p className="text-xs text-slate-500">Tier: PRO (300 seats)</p>
              </div>
              <Badge variant="success">Active</Badge>
            </div>
          </div>
        </Card>

        <Card className="space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="font-semibold text-white text-base">System Telemetry & Health</h3>
            <Badge variant="success">100% Operational</Badge>
          </div>
          <div className="space-y-3 text-xs text-slate-400">
            <div className="flex justify-between py-1 border-b border-slate-800">
              <span>PostgreSQL + pgvector Latency</span>
              <span className="text-emerald-400 font-mono">1.8ms</span>
            </div>
            <div className="flex justify-between py-1 border-b border-slate-800">
              <span>Redis L2 Cache Hit Ratio</span>
              <span className="text-emerald-400 font-mono">96.4%</span>
            </div>
            <div className="flex justify-between py-1 border-b border-slate-800">
              <span>AI Provider SPI Mesh</span>
              <span className="text-indigo-400 font-mono">Mock/OpenAI Primary</span>
            </div>
            <div className="flex justify-between py-1">
              <span>Ingress Security WAF</span>
              <span className="text-emerald-400 font-mono">Active (Zero Breaches)</span>
            </div>
          </div>
        </Card>
      </div>
    </div>
  );
};
""")

# Certificate Verification Page
write("frontend/src/pages/courses/CertificateVerifyPage.tsx", """
import React from "react";
import { useParams, Link } from "react-router-dom";
import { Card } from "../../components/ui/card";
import { Badge } from "../../components/ui/badge";
import { Award, ShieldCheck, CheckCircle, ExternalLink } from "lucide-react";

export const CertificateVerifyPage: React.FC = () => {
  const { verificationCode = "AILMS-CERT-98234-2026" } = useParams();

  return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center p-4">
      <Card className="max-w-lg w-full p-8 border-indigo-500/40 bg-slate-900/90 text-center space-y-6">
        <div className="h-16 w-16 bg-emerald-500/10 text-emerald-400 rounded-full flex items-center justify-center mx-auto">
          <ShieldCheck className="h-8 w-8" />
        </div>

        <div>
          <Badge variant="success" className="mb-2">Cryptographically Verified</Badge>
          <h1 className="text-2xl font-bold text-white">Certificate of Completion</h1>
          <p className="text-xs text-slate-400 mt-1">Verification Code: {verificationCode}</p>
        </div>

        <div className="p-4 bg-slate-950/80 rounded-xl border border-slate-800 text-left text-xs space-y-3">
          <div className="flex justify-between">
            <span className="text-slate-500">Student Name:</span>
            <span className="font-semibold text-white">Alex Learner</span>
          </div>
          <div className="flex justify-between">
            <span className="text-slate-500">Course:</span>
            <span className="font-semibold text-white">Advanced Distributed Systems</span>
          </div>
          <div className="flex justify-between">
            <span className="text-slate-500">Issued On:</span>
            <span className="font-semibold text-white">August 29, 2026</span>
          </div>
          <div className="flex justify-between">
            <span className="text-slate-500">Issuing Authority:</span>
            <span className="font-semibold text-indigo-400">Aegis Enterprise LMS</span>
          </div>
        </div>

        <Link to="/" className="text-xs text-indigo-400 hover:underline flex items-center justify-center gap-1">
          <span>Return to Learning Platform</span>
        </Link>
      </Card>
    </div>
  );
};
""")

# Discussions Board Page
write("frontend/src/pages/courses/DiscussionBoardPage.tsx", """
import React, { useState } from "react";
import { Card } from "../../components/ui/card";
import { Button } from "../../components/ui/button";
import { Input } from "../../components/ui/input";
import { Badge } from "../../components/ui/badge";
import { MessageSquare, ThumbsUp, Sparkles, Send } from "lucide-react";

export const DiscussionBoardPage: React.FC = () => {
  const [posts, setPosts] = useState([
    {
      id: "p1",
      title: "How does the pgvector HNSW indexing compare to IVFFlat for sub-millisecond retrieval?",
      author: "Samantha Ray",
      time: "2 hours ago",
      upvotes: 14,
      comments: 3,
      tag: "AI Architecture",
    },
    {
      id: "p2",
      title: "Handling distributed sagas vs two-phase commit in tenant-partitioned microservices",
      author: "David Chen",
      time: "5 hours ago",
      upvotes: 22,
      comments: 7,
      tag: "Architecture",
    },
  ]);

  const [newTitle, setNewTitle] = useState("");

  const handlePost = (e: React.FormEvent) => {
    e.preventDefault();
    if (!newTitle.trim()) return;
    setPosts(prev => [
      {
        id: `p-${Date.now()}`,
        title: newTitle,
        author: "Alex Learner",
        time: "Just now",
        upvotes: 1,
        comments: 0,
        tag: "Discussion",
      },
      ...prev,
    ]);
    setNewTitle("");
  };

  return (
    <div className="space-y-6 max-w-5xl mx-auto">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white">Course Discussions & Community</h1>
          <p className="text-sm text-slate-400">Collaborate with peers, ask instructors, and get AI-assisted answers</p>
        </div>
      </div>

      <Card className="p-4 bg-slate-900/60">
        <form onSubmit={handlePost} className="flex gap-2">
          <Input 
            placeholder="Start a new discussion topic or ask a technical question..." 
            value={newTitle}
            onChange={e => setNewTitle(e.target.value)}
          />
          <Button type="submit" variant="primary" className="flex items-center gap-1">
            <Send className="h-4 w-4" />
            <span>Post</span>
          </Button>
        </form>
      </Card>

      <div className="space-y-4">
        {posts.map(post => (
          <Card key={post.id} className="p-5 flex items-start justify-between">
            <div className="space-y-2">
              <div className="flex items-center gap-2">
                <Badge variant="primary">{post.tag}</Badge>
                <span className="text-xs text-slate-500">Posted by {post.author} • {post.time}</span>
              </div>
              <h3 className="text-base font-semibold text-white">{post.title}</h3>
            </div>
            <div className="flex items-center gap-4 text-xs text-slate-400">
              <button className="flex items-center gap-1 hover:text-indigo-400 transition-colors">
                <ThumbsUp className="h-4 w-4" />
                <span>{post.upvotes}</span>
              </button>
              <div className="flex items-center gap-1">
                <MessageSquare className="h-4 w-4" />
                <span>{post.comments}</span>
              </div>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
};
""")

# Update App.tsx with all new routes
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
import { TeacherDashboard } from "./pages/teacher/TeacherDashboard";
import { CourseBuilderPage } from "./pages/courses/CourseBuilderPage";
import { AdminDashboard } from "./pages/admin/AdminDashboard";
import { CertificateVerifyPage } from "./pages/courses/CertificateVerifyPage";
import { DiscussionBoardPage } from "./pages/courses/DiscussionBoardPage";

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

              {/* Main Authenticated Layout */}
              <Route element={<DashboardLayout />}>
                <Route path="/" element={<Navigate to="/dashboard" replace />} />
                <Route path="/dashboard" element={<StudentDashboard />} />
                <Route path="/courses" element={<CourseCatalogPage />} />
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
""")

print("Frontend full suite pages generated successfully.")
