import React, { useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { Card } from "../../components/ui/card";
import { Badge } from "../../components/ui/badge";
import { Button } from "../../components/ui/button";
import { FileText, Upload, Sparkles, CheckCircle2, AlertTriangle, ArrowLeft, Clock } from "lucide-react";

export const AssignmentSubmissionPage: React.FC = () => {
  const { id } = useParams();
  const navigate = useNavigate();

  const [submissionText, setSubmissionText] = useState("");
  const [fileName, setFileName] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isSubmitted, setIsSubmitted] = useState(false);
  const [aiPreCheck, setAiPreCheck] = useState<{
    score: number;
    feedback: string;
    strengths: string[];
    suggestions: string[];
  } | null>(null);

  const rubricCriteria = [
    { title: "Architectural Correctness & Fault Tolerance", weight: "40%", max: 40 },
    { title: "pgvector & HNSW Query Optimization", weight: "30%", max: 30 },
    { title: "Multi-Tenant Isolation & Security Controls", weight: "30%", max: 30 },
  ];

  const handleRunAiPreCheck = () => {
    if (!submissionText.trim()) {
      alert("Please write or paste your solution text before running AI Pre-Evaluation.");
      return;
    }
    setAiPreCheck({
      score: 92,
      feedback: "Strong architectural design. The use of tenant-partitioned JPA filters and HNSW cosine vector indexing aligns with enterprise standards.",
      strengths: [
        "Explicit handling of cross-tenant authorization checks before vector query",
        "Clear demarcation between system prompts and user-uploaded course documents",
      ],
      suggestions: [
        "Consider adding circuit-breaker fallback parameters for external LLM timeouts",
      ],
    });
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    setTimeout(() => {
      setIsSubmitting(false);
      setIsSubmitted(true);
    }, 1000);
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <button onClick={() => navigate("/dashboard")} className="flex items-center gap-2 text-xs text-slate-400 hover:text-white">
        <ArrowLeft className="h-4 w-4" /> Back to Dashboard
      </button>

      {/* Header */}
      <div className="flex items-start justify-between">
        <div>
          <Badge variant="primary">Assignment</Badge>
          <h1 className="text-2xl font-bold text-white mt-1">
            Enterprise RAG Pipeline & Multi-Tenant Partitioning
          </h1>
          <p className="text-xs text-slate-400 mt-1 flex items-center gap-2">
            <Clock className="h-3.5 w-3.5 text-amber-400" /> Due in 3 days • Maximum Score: 100 pts
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Main Submission Form */}
        <div className="lg:col-span-2 space-y-6">
          <Card className="p-5 space-y-4 bg-slate-900/80 border-slate-800">
            <h3 className="text-sm font-semibold text-white">Instructions</h3>
            <p className="text-xs text-slate-300 leading-relaxed">
              Design and document a high-throughput RAG pipeline in Java and PostgreSQL (pgvector).
              Explain how you isolate vectors per tenant and prevent prompt injection from PDF uploads.
            </p>
          </Card>

          {!isSubmitted ? (
            <Card className="p-5 space-y-4 bg-slate-900/80 border-slate-800">
              <h3 className="text-sm font-semibold text-white">Your Submission</h3>

              {/* Text Submission Area */}
              <div className="space-y-1.5">
                <label className="text-xs text-slate-400 font-medium">Technical Writeup & Code Architecture</label>
                <textarea
                  value={submissionText}
                  onChange={(e) => setSubmissionText(e.target.value)}
                  placeholder="Paste your architecture specification, SQL schema definitions, and Java controller logic here..."
                  className="w-full h-48 p-3.5 bg-slate-950 border border-slate-800 rounded-lg font-mono text-xs text-slate-200 focus:outline-none focus:ring-1 focus:ring-indigo-500 leading-relaxed"
                />
                <div className="flex justify-between text-[11px] text-slate-500">
                  <span>{submissionText.split(/\s+/).filter(Boolean).length} words</span>
                  <button type="button" onClick={handleRunAiPreCheck} className="text-indigo-400 hover:underline flex items-center gap-1 font-sans">
                    <Sparkles className="h-3.5 w-3.5" /> Run AI Pre-Submission Check
                  </button>
                </div>
              </div>

              {/* File Attachment Upload */}
              <div className="p-4 border border-dashed border-slate-800 rounded-xl bg-slate-950/40 text-center space-y-2">
                <Upload className="h-6 w-6 text-slate-500 mx-auto" />
                <div className="text-xs text-slate-400">
                  {fileName ? (
                    <span className="text-indigo-400 font-medium">{fileName}</span>
                  ) : (
                    <span>Drag and drop project zip/PDF or <button type="button" onClick={() => setFileName("rag-architecture-solution.pdf")} className="text-indigo-400 underline">browse files</button></span>
                  )}
                </div>
                <p className="text-[10px] text-slate-500">Allowed: .pdf, .zip, .docx (Max: 50MB)</p>
              </div>

              {/* AI Pre-Check Feedback Banner */}
              {aiPreCheck && (
                <div className="p-4 bg-indigo-950/20 border border-indigo-500/30 rounded-xl space-y-3 text-xs">
                  <div className="flex items-center justify-between">
                    <span className="font-semibold text-indigo-300 flex items-center gap-1.5">
                      <Sparkles className="h-4 w-4" /> AI Pre-Grading Estimation
                    </span>
                    <Badge variant="success">Estimated: {aiPreCheck.score}/100</Badge>
                  </div>
                  <p className="text-slate-300 leading-relaxed">{aiPreCheck.feedback}</p>
                  <div className="space-y-1">
                    <span className="text-emerald-400 font-medium">Key Strengths:</span>
                    {aiPreCheck.strengths.map((s, i) => (
                      <p key={i} className="text-slate-400 pl-3">✓ {s}</p>
                    ))}
                  </div>
                </div>
              )}

              <Button variant="primary" className="w-full" isLoading={isSubmitting} onClick={handleSubmit}>
                Submit Assignment for Instructor Grading
              </Button>
            </Card>
          ) : (
            <Card className="p-8 text-center space-y-4 bg-slate-900 border-slate-800">
              <div className="h-14 w-14 rounded-full bg-emerald-500/10 text-emerald-400 flex items-center justify-center mx-auto">
                <CheckCircle2 className="h-7 w-7" />
              </div>
              <h2 className="text-xl font-bold text-white">Assignment Submitted!</h2>
              <p className="text-xs text-slate-400">
                Your submission has been queued for instructor review and AI rubric pre-evaluation.
              </p>
              <Button variant="secondary" size="sm" onClick={() => setIsSubmitted(false)}>
                Resubmit Solution
              </Button>
            </Card>
          )}
        </div>

        {/* Rubric Criteria Sidebar */}
        <div className="space-y-4">
          <h3 className="text-sm font-semibold text-white">Grading Rubric</h3>
          <Card className="p-4 space-y-4 bg-slate-900/80 border-slate-800 text-xs">
            {rubricCriteria.map((crit, idx) => (
              <div key={idx} className="space-y-1 pb-3 border-b border-slate-800/80 last:border-0 last:pb-0">
                <div className="flex justify-between font-semibold text-slate-200">
                  <span>{crit.title}</span>
                  <span className="text-indigo-400">{crit.max} pts</span>
                </div>
                <p className="text-[11px] text-slate-500">Weight: {crit.weight}</p>
              </div>
            ))}
          </Card>
        </div>
      </div>
    </div>
  );
};
