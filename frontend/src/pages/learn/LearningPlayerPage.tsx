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
