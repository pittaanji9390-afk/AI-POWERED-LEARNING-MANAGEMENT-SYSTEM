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
