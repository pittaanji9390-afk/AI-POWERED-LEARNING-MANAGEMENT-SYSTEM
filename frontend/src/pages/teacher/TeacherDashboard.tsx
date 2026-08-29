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
