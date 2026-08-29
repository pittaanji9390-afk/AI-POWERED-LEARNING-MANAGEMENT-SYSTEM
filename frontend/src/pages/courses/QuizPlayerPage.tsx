import React, { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { Card } from "../../components/ui/card";
import { Button } from "../../components/ui/button";
import { Badge } from "../../components/ui/badge";
import { ProgressBar } from "../../components/ui/progress-bar";
import { Clock, CheckCircle2, XCircle, AlertCircle, Sparkles, ArrowRight, RotateCcw } from "lucide-react";

interface Question {
  id: string;
  text: string;
  options: { id: string; text: string }[];
  correctOptionId: string;
  explanation: string;
}

const mockQuizQuestions: Question[] = [
  {
    id: "q1",
    text: "Which vector index algorithm in PostgreSQL (pgvector) offers the lowest query latency for high-dimensional cosine distance similarity?",
    options: [
      { id: "a", text: "IVFFlat (Inverted File Flat)" },
      { id: "b", text: "HNSW (Hierarchical Navigable Small World)" },
      { id: "c", text: "B-Tree Standard Index" },
      { id: "d", text: "GIN Inverted Index" },
    ],
    correctOptionId: "b",
    explanation: "HNSW builds a multi-layer graph that enables logarithmic search time with very high recall, outperforming IVFFlat in query speed at the cost of higher build time and memory.",
  },
  {
    id: "q2",
    text: "How should cross-tenant data isolation be enforced in an enterprise SaaS application?",
    options: [
      { id: "a", text: "By filtering tenant IDs exclusively in the frontend React state" },
      { id: "b", text: "By enforcing row-level database filters, TenantContext interceptors, and strict repository boundaries" },
      { id: "c", text: "By creating a single shared unauthenticated cache key in Redis" },
      { id: "d", text: "By relying on DNS routing without backend query constraints" },
    ],
    correctOptionId: "b",
    explanation: "Multi-tenant isolation must never rely on frontend filtering. It requires server-side validation, thread-local TenantContext, and hard database query filters.",
  },
  {
    id: "q3",
    text: "What is the primary mechanism used in modern RAG pipelines to prevent indirect prompt injection from retrieved course documents?",
    options: [
      { id: "a", text: "Ignoring all system instructions in favor of document text" },
      { id: "b", text: "Embedding-time encryption without prompt delimiters" },
      { id: "c", text: "Strict boundary delimiters, system prompt sandboxing, and explicit non-execution instructions" },
      { id: "d", text: "Executing all scripts found inside uploaded PDF documents" },
    ],
    correctOptionId: "c",
    explanation: "Treating retrieved course context as untrusted input with explicit boundary tags (e.g. <<<COURSE_CONTEXT>>>) prevents document content from overriding system developer rules.",
  },
];

export const QuizPlayerPage: React.FC = () => {
  const { quizId } = useParams();
  const navigate = useNavigate();

  const [currentIndex, setCurrentIndex] = useState(0);
  const [selectedAnswers, setSelectedAnswers] = useState<Record<string, string>>({});
  const [timeLeft, setTimeLeft] = useState(300); // 5 minutes
  const [isSubmitted, setIsSubmitted] = useState(false);

  useEffect(() => {
    if (isSubmitted || timeLeft <= 0) return;
    const timer = setInterval(() => setTimeLeft((t) => (t > 0 ? t - 1 : 0)), 1000);
    return () => clearInterval(timer);
  }, [timeLeft, isSubmitted]);

  const currentQuestion = mockQuizQuestions[currentIndex];
  const progressPercent = ((currentIndex + 1) / mockQuizQuestions.length) * 100;

  const handleSelectOption = (optionId: string) => {
    if (isSubmitted) return;
    setSelectedAnswers((prev) => ({ ...prev, [currentQuestion.id]: optionId }));
  };

  const calculateScore = () => {
    let correct = 0;
    mockQuizQuestions.forEach((q) => {
      if (selectedAnswers[q.id] === q.correctOptionId) correct++;
    });
    return {
      correct,
      total: mockQuizQuestions.length,
      percentage: Math.round((correct / mockQuizQuestions.length) * 100),
    };
  };

  const formatTimer = (seconds: number) => {
    const m = Math.floor(seconds / 60);
    const s = seconds % 60;
    return `${m}:${s < 10 ? "0" : ""}${s}`;
  };

  const score = isSubmitted ? calculateScore() : null;

  return (
    <div className="max-w-3xl mx-auto space-y-6">
      {/* Top Bar */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-xl font-bold text-white">Module Assessment</h1>
          <p className="text-xs text-slate-400">Architectural Security & RAG Design</p>
        </div>
        {!isSubmitted && (
          <div className="flex items-center gap-2 bg-slate-900 border border-slate-800 px-3 py-1.5 rounded-lg text-sm">
            <Clock className="h-4 w-4 text-indigo-400" />
            <span className={`font-mono font-medium ${timeLeft < 60 ? "text-rose-400 animate-pulse" : "text-slate-200"}`}>
              {formatTimer(timeLeft)}
            </span>
          </div>
        )}
      </div>

      {/* Progress */}
      <div className="space-y-1.5">
        <div className="flex justify-between text-xs text-slate-400">
          <span>Question {currentIndex + 1} of {mockQuizQuestions.length}</span>
          <span>{Math.round(progressPercent)}% Complete</span>
        </div>
        <ProgressBar progress={progressPercent} />
      </div>

      {/* Main Quiz / Results Card */}
      {!isSubmitted ? (
        <Card className="p-6 space-y-6 bg-slate-900/80 border-slate-800">
          <div className="space-y-3">
            <Badge variant="primary">Question {currentIndex + 1}</Badge>
            <h2 className="text-base font-semibold text-white leading-relaxed">
              {currentQuestion.text}
            </h2>
          </div>

          <div className="space-y-3">
            {currentQuestion.options.map((opt) => {
              const isSelected = selectedAnswers[currentQuestion.id] === opt.id;
              return (
                <button
                  key={opt.id}
                  onClick={() => handleSelectOption(opt.id)}
                  className={`w-full text-left p-4 rounded-xl border transition-all text-sm flex items-start gap-3 ${
                    isSelected
                      ? "bg-indigo-600/20 border-indigo-500 text-white shadow-sm"
                      : "bg-slate-950/60 border-slate-800 text-slate-300 hover:bg-slate-800/60"
                  }`}
                >
                  <span className={`h-5 w-5 rounded-full border flex items-center justify-center text-xs font-semibold ${
                    isSelected ? "border-indigo-400 bg-indigo-500 text-white" : "border-slate-600 text-slate-400"
                  }`}>
                    {opt.id.toUpperCase()}
                  </span>
                  <span className="flex-1">{opt.text}</span>
                </button>
              );
            })}
          </div>

          <div className="flex items-center justify-between pt-4 border-t border-slate-800">
            <Button
              variant="outline"
              size="sm"
              disabled={currentIndex === 0}
              onClick={() => setCurrentIndex((i) => Math.max(0, i - 1))}
            >
              Previous
            </Button>

            {currentIndex < mockQuizQuestions.length - 1 ? (
              <Button
                variant="primary"
                size="sm"
                onClick={() => setCurrentIndex((i) => Math.min(mockQuizQuestions.length - 1, i + 1))}
              >
                Next Question
              </Button>
            ) : (
              <Button
                variant="primary"
                size="sm"
                onClick={() => setIsSubmitted(true)}
              >
                Submit Assessment
              </Button>
            )}
          </div>
        </Card>
      ) : (
        /* Results View */
        <Card className="p-8 space-y-6 bg-slate-900/90 border-slate-800 text-center">
          <div className="space-y-3">
            <div className={`h-16 w-16 rounded-full flex items-center justify-center mx-auto ${
              score && score.percentage >= 70 ? "bg-emerald-500/10 text-emerald-400" : "bg-amber-500/10 text-amber-400"
            }`}>
              {score && score.percentage >= 70 ? <CheckCircle2 className="h-8 w-8" /> : <AlertCircle className="h-8 w-8" />}
            </div>
            <h2 className="text-2xl font-bold text-white">
              {score && score.percentage >= 70 ? "Assessment Passed!" : "Needs Review"}
            </h2>
            <p className="text-sm text-slate-400">
              You scored <span className="font-semibold text-white">{score?.correct}</span> out of {score?.total} ({score?.percentage}%)
            </p>
          </div>

          <div className="space-y-4 text-left pt-4 border-t border-slate-800">
            <h3 className="text-sm font-semibold text-white">Answer Key & AI Explanations</h3>
            {mockQuizQuestions.map((q, idx) => {
              const userAns = selectedAnswers[q.id];
              const isCorrect = userAns === q.correctOptionId;
              return (
                <div key={q.id} className="p-4 bg-slate-950/70 rounded-xl border border-slate-800 space-y-2 text-xs">
                  <div className="flex items-start justify-between">
                    <span className="font-medium text-slate-200">{idx + 1}. {q.text}</span>
                    {isCorrect ? (
                      <span className="flex items-center gap-1 text-emerald-400 font-semibold"><CheckCircle2 className="h-3.5 w-3.5" /> Correct</span>
                    ) : (
                      <span className="flex items-center gap-1 text-rose-400 font-semibold"><XCircle className="h-3.5 w-3.5" /> Incorrect</span>
                    )}
                  </div>
                  <div className="text-slate-400 bg-slate-900/60 p-2.5 rounded-lg border border-slate-800/80 flex items-start gap-2">
                    <Sparkles className="h-4 w-4 text-indigo-400 flex-shrink-0 mt-0.5" />
                    <span><strong>Rationale:</strong> {q.explanation}</span>
                  </div>
                </div>
              );
            })}
          </div>

          <div className="flex items-center justify-center gap-3 pt-4">
            <Button variant="secondary" onClick={() => { setIsSubmitted(false); setCurrentIndex(0); setSelectedAnswers({}); setTimeLeft(300); }}>
              <RotateCcw className="h-4 w-4 mr-1.5" /> Retake Quiz
            </Button>
            <Button variant="primary" onClick={() => navigate("/dashboard")}>
              Continue to Dashboard <ArrowRight className="h-4 w-4 ml-1.5" />
            </Button>
          </div>
        </Card>
      )}
    </div>
  );
};
