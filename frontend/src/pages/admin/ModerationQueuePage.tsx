import React, { useState } from "react";
import { Card } from "../../components/ui/card";
import { Badge } from "../../components/ui/badge";
import { Button } from "../../components/ui/button";
import { ShieldAlert, Check, X, Eye, AlertTriangle } from "lucide-react";

export const ModerationQueuePage: React.FC = () => {
  const [reports, setReports] = useState([
    {
      id: "rep-1",
      targetType: "DISCUSSION",
      content: "Is there any leaked exam dump or solution file for Chapter 3 quiz?",
      reporter: "Learner @student_99",
      reason: "Academic Integrity Violation / Exam Leaks",
      time: "15m ago",
      status: "PENDING",
    },
    {
      id: "rep-2",
      targetType: "COMMENT",
      content: "Check out this external link for free crypto prizes: https://spam.fake",
      reporter: "Automated AI Guardrail",
      reason: "Spam & Malicious Link",
      time: "1h ago",
      status: "PENDING",
    },
  ]);

  const handleAction = (id: string, action: "HIDE" | "DISMISS") => {
    setReports(prev => prev.filter(r => r.id !== id));
  };

  return (
    <div className="space-y-6 max-w-5xl mx-auto">
      <div>
        <h1 className="text-2xl font-bold text-white">Content Moderation Queue</h1>
        <p className="text-sm text-slate-400">Review flagged comments, academic violations, and automated AI security reports</p>
      </div>

      <div className="space-y-4">
        {reports.length > 0 ? (
          reports.map(rep => (
            <Card key={rep.id} className="p-5 space-y-3 bg-slate-900/80 border-slate-800">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <Badge variant="warning" className="flex items-center gap-1">
                    <AlertTriangle className="h-3.5 w-3.5" /> Flagged
                  </Badge>
                  <span className="text-xs text-slate-400">Reported by {rep.reporter} • {rep.time}</span>
                </div>
                <Badge variant="neutral">{rep.targetType}</Badge>
              </div>

              <div className="p-3.5 bg-slate-950/80 rounded-lg border border-slate-800 text-xs text-slate-200 font-mono">
                "{rep.content}"
              </div>

              <div className="flex items-center justify-between pt-2">
                <span className="text-xs text-amber-400 font-medium">Reason: {rep.reason}</span>
                <div className="flex items-center gap-2">
                  <Button variant="secondary" size="sm" onClick={() => handleAction(rep.id, "DISMISS")}>
                    Dismiss Report
                  </Button>
                  <Button variant="danger" size="sm" onClick={() => handleAction(rep.id, "HIDE")}>
                    Hide & Shadowban
                  </Button>
                </div>
              </div>
            </Card>
          ))
        ) : (
          <Card className="p-12 text-center text-slate-500 space-y-2">
            <Check className="h-8 w-8 text-emerald-400 mx-auto" />
            <p className="text-sm font-medium text-white">Moderation Queue Clear</p>
            <p className="text-xs">No pending flagged items to review.</p>
          </Card>
        )}
      </div>
    </div>
  );
};
