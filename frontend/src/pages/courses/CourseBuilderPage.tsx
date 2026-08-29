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
