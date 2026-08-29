import React, { useState } from "react";
import { Card } from "../../components/ui/card";
import { Badge } from "../../components/ui/badge";
import { Button } from "../../components/ui/button";
import { ProgressBar } from "../../components/ui/progress-bar";
import { Sparkles, CheckCircle2, Lock, ArrowRight, Target, Brain, BookOpen } from "lucide-react";
import { useNavigate } from "react-router-dom";

interface SkillNode {
  id: string;
  name: string;
  category: string;
  masteryLevel: "MASTERED" | "PROFICIENT" | "PRACTICING" | "LOCKED";
  scorePercent: number;
  prerequisites: string[];
  recommendedActivity: string;
}

const mockSkills: SkillNode[] = [
  {
    id: "s1",
    name: "Distributed Systems Fundamentals",
    category: "Architecture",
    masteryLevel: "MASTERED",
    scorePercent: 95,
    prerequisites: [],
    recommendedActivity: "Completed (Mastery Verified)",
  },
  {
    id: "s2",
    name: "Vector Embeddings & Cosine Search",
    category: "AI Engineering",
    masteryLevel: "PROFICIENT",
    scorePercent: 82,
    prerequisites: ["s1"],
    recommendedActivity: "Practice Quiz: High-Dimensional HNSW Tuning",
  },
  {
    id: "s3",
    name: "RAG Guardrails & Anti-Prompt-Injection",
    category: "AI Security",
    masteryLevel: "PRACTICING",
    scorePercent: 64,
    prerequisites: ["s2"],
    recommendedActivity: "Interactive Lab: Delimiter Boundary Testing",
  },
  {
    id: "s4",
    name: "Multi-Tenant Distributed Sagas",
    category: "Architecture",
    masteryLevel: "LOCKED",
    scorePercent: 0,
    prerequisites: ["s1", "s3"],
    recommendedActivity: "Unlock by reaching 80% on RAG Guardrails",
  },
];

export const LearningPathPage: React.FC = () => {
  const navigate = useNavigate();
  const [selectedSkill, setSelectedSkill] = useState<SkillNode>(mockSkills[1]);

  return (
    <div className="space-y-8 max-w-6xl mx-auto">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white">Adaptive Learning Path</h1>
          <p className="text-sm text-slate-400">AI-tailored skill progression and mastery milestones</p>
        </div>
        <Badge variant="primary" className="flex items-center gap-1">
          <Brain className="h-3.5 w-3.5" />
          <span>Personalization Engine Active</span>
        </Badge>
      </div>

      {/* AI Recommendation Banner */}
      <Card className="border-indigo-500/30 bg-gradient-to-r from-indigo-950/40 via-slate-900 to-slate-900 p-6 flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div className="space-y-1">
          <div className="flex items-center gap-2 text-indigo-400 text-xs font-semibold uppercase tracking-wider">
            <Sparkles className="h-4 w-4" /> Next Recommended Action
          </div>
          <h2 className="text-lg font-bold text-white">
            Level up "RAG Guardrails & Anti-Prompt-Injection"
          </h2>
          <p className="text-xs text-slate-300">
            Based on your recent quiz attempt, strengthening prompt injection boundaries will unlock Distributed Sagas.
          </p>
        </div>
        <Button variant="primary" onClick={() => navigate("/quizzes/rag-sec-1/take")}>
          Launch Recommended Activity <ArrowRight className="h-4 w-4 ml-1.5" />
        </Button>
      </Card>

      {/* Skill Node Graph */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-4">
          <h3 className="text-base font-semibold text-white">Skill Dependency Graph</h3>
          <div className="space-y-3">
            {mockSkills.map((skill, idx) => {
              const isSelected = selectedSkill.id === skill.id;
              return (
                <div
                  key={skill.id}
                  onClick={() => skill.masteryLevel !== "LOCKED" && setSelectedSkill(skill)}
                  className={`p-4 rounded-xl border transition-all cursor-pointer flex items-center justify-between ${
                    isSelected
                      ? "bg-indigo-950/30 border-indigo-500 shadow-md"
                      : skill.masteryLevel === "LOCKED"
                      ? "bg-slate-950/40 border-slate-800/60 opacity-60 cursor-not-allowed"
                      : "bg-slate-900/60 border-slate-800 hover:border-slate-700"
                  }`}
                >
                  <div className="flex items-center gap-4">
                    <div className={`h-10 w-10 rounded-xl flex items-center justify-center font-bold text-sm ${
                      skill.masteryLevel === "MASTERED"
                        ? "bg-emerald-500/10 text-emerald-400"
                        : skill.masteryLevel === "PROFICIENT"
                        ? "bg-indigo-500/10 text-indigo-400"
                        : skill.masteryLevel === "PRACTICING"
                        ? "bg-amber-500/10 text-amber-400"
                        : "bg-slate-800 text-slate-500"
                    }`}>
                      {skill.masteryLevel === "MASTERED" ? <CheckCircle2 className="h-5 w-5" /> : skill.masteryLevel === "LOCKED" ? <Lock className="h-5 w-5" /> : `${idx + 1}`}
                    </div>
                    <div>
                      <div className="flex items-center gap-2">
                        <span className="font-semibold text-sm text-white">{skill.name}</span>
                        <Badge variant={
                          skill.masteryLevel === "MASTERED" ? "success" : skill.masteryLevel === "PROFICIENT" ? "primary" : skill.masteryLevel === "PRACTICING" ? "warning" : "neutral"
                        }>
                          {skill.masteryLevel}
                        </Badge>
                      </div>
                      <p className="text-xs text-slate-400 mt-0.5">{skill.category}</p>
                    </div>
                  </div>

                  <div className="text-right">
                    <span className="text-sm font-bold text-white">{skill.scorePercent}%</span>
                    <p className="text-[10px] text-slate-500">Mastery</p>
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Skill Details Sidebar */}
        <div>
          <h3 className="text-base font-semibold text-white mb-4">Target Skill Details</h3>
          <Card className="p-5 space-y-5 bg-slate-900/80 border-slate-800">
            <div>
              <Badge variant="primary">{selectedSkill.category}</Badge>
              <h4 className="text-lg font-bold text-white mt-2">{selectedSkill.name}</h4>
              <p className="text-xs text-slate-400 mt-1">Current Mastery Score: {selectedSkill.scorePercent}%</p>
            </div>

            <div className="space-y-1.5">
              <div className="flex justify-between text-xs text-slate-400">
                <span>Progress to Mastery</span>
                <span>{selectedSkill.scorePercent}%</span>
              </div>
              <ProgressBar progress={selectedSkill.scorePercent} />
            </div>

            <div className="p-3 bg-slate-950/70 rounded-lg border border-slate-800 text-xs space-y-1.5">
              <span className="text-slate-500 font-medium">Next Recommended Activity:</span>
              <p className="text-slate-200 font-medium">{selectedSkill.recommendedActivity}</p>
            </div>

            <Button variant="primary" className="w-full" onClick={() => navigate("/ai-tutor")}>
              Practice with AI Tutor
            </Button>
          </Card>
        </div>
      </div>
    </div>
  );
};
