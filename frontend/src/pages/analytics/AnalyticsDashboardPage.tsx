import React from "react";
import { StatsCard } from "../../components/ui/stats-card";
import { Card } from "../../components/ui/card";
import { Badge } from "../../components/ui/badge";
import { Users, GraduationCap, Award, Brain, Clock, Zap, TrendingUp } from "lucide-react";

export const AnalyticsDashboardPage: React.FC = () => {
  return (
    <div className="space-y-8 max-w-6xl mx-auto">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white">Platform Learning Analytics</h1>
          <p className="text-sm text-slate-400">Real-time learning telemetry, assessment distributions, and AI metrics</p>
        </div>
        <Badge variant="primary" className="flex items-center gap-1">
          <Zap className="h-3.5 w-3.5" /> Live Telemetry
        </Badge>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <StatsCard title="Total Active Learners" value="4,270" change="+14.2%" isPositive={true} icon={Users} />
        <StatsCard title="Avg Course Completion" value="78.4%" change="+3.8%" isPositive={true} icon={GraduationCap} iconColor="text-emerald-400" iconBg="bg-emerald-500/10" />
        <StatsCard title="Certificates Verified" value="1,894" change="+22.1%" isPositive={true} icon={Award} iconColor="text-purple-400" iconBg="bg-purple-500/10" />
        <StatsCard title="AI Socratic Queries" value="128.4k" change="+34.5%" isPositive={true} icon={Brain} iconColor="text-cyan-400" iconBg="bg-cyan-500/10" />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card className="p-5 space-y-4">
          <h3 className="text-sm font-semibold text-white">Weekly Learning Minutes</h3>
          <div className="h-48 flex items-end justify-between gap-2 pt-8 px-2 border-b border-slate-800">
            {[
              { day: "Mon", val: "65%" },
              { day: "Tue", val: "80%" },
              { day: "Wed", val: "95%" },
              { day: "Thu", val: "75%" },
              { day: "Fri", val: "90%" },
              { day: "Sat", val: "40%" },
              { day: "Sun", val: "55%" },
            ].map((d, i) => (
              <div key={i} className="flex-1 flex flex-col items-center gap-2">
                <div className="w-full bg-indigo-600 rounded-t-md transition-all hover:bg-indigo-500" style={{ height: d.val }} />
                <span className="text-[10px] text-slate-500">{d.day}</span>
              </div>
            ))}
          </div>
        </Card>

        <Card className="p-5 space-y-4">
          <h3 className="text-sm font-semibold text-white">Assessment Mastery Scores</h3>
          <div className="space-y-3 text-xs">
            <div className="flex justify-between items-center p-3 bg-slate-950/60 rounded-lg border border-slate-800">
              <span className="text-slate-200">Distributed Consensus & Raft</span>
              <Badge variant="success">88.4% Avg Score</Badge>
            </div>
            <div className="flex justify-between items-center p-3 bg-slate-950/60 rounded-lg border border-slate-800">
              <span className="text-slate-200">pgvector HNSW Cosine Indexing</span>
              <Badge variant="primary">82.1% Avg Score</Badge>
            </div>
            <div className="flex justify-between items-center p-3 bg-slate-950/60 rounded-lg border border-slate-800">
              <span className="text-slate-200">Multi-Tenant Database Isolation</span>
              <Badge variant="success">91.6% Avg Score</Badge>
            </div>
          </div>
        </Card>
      </div>
    </div>
  );
};
