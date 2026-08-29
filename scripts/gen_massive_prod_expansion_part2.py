import os

def write(filepath, content):
    dirpath = os.path.dirname(filepath)
    if dirpath:
        os.makedirs(dirpath, exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Wrote: {filepath}")

# UI Components
write("frontend/src/components/ui/accordion.tsx", """
import React, { useState } from "react";
import { ChevronDown } from "lucide-react";
import { cn } from "../../lib/utils";

export interface AccordionItem {
  id: string;
  title: string;
  content: React.ReactNode;
}

export const Accordion: React.FC<{ items: AccordionItem[]; allowMultiple?: boolean }> = ({ items, allowMultiple = false }) => {
  const [openIds, setOpenIds] = useState<string[]>([items[0]?.id || ""]);

  const toggle = (id: string) => {
    if (allowMultiple) {
      setOpenIds(prev => prev.includes(id) ? prev.filter(i => i !== id) : [...prev, id]);
    } else {
      setOpenIds(prev => prev.includes(id) ? [] : [id]);
    }
  };

  return (
    <div className="space-y-2">
      {items.map(item => {
        const isOpen = openIds.includes(item.id);
        return (
          <div key={item.id} className="border border-slate-800 rounded-xl overflow-hidden bg-slate-950/60">
            <button
              onClick={() => toggle(item.id)}
              className="w-full p-4 text-left flex items-center justify-between text-sm font-semibold text-white hover:bg-slate-900/60 transition-colors"
            >
              <span>{item.title}</span>
              <ChevronDown className={cn("h-4 w-4 text-slate-400 transition-transform duration-200", isOpen && "transform rotate-180")} />
            </button>
            {isOpen && (
              <div className="p-4 pt-0 text-xs text-slate-300 border-t border-slate-800/60 bg-slate-900/20 leading-relaxed">
                {item.content}
              </div>
            )}
          </div>
        );
      })}
    </div>
  );
};
""")

write("frontend/src/components/ui/stats-card.tsx", """
import React from "react";
import { Card } from "./card";
import { LucideIcon } from "lucide-react";
import { cn } from "../../lib/utils";

export interface StatsCardProps {
  title: string;
  value: string | number;
  change?: string;
  isPositive?: boolean;
  icon: LucideIcon;
  iconColor?: string;
  iconBg?: string;
}

export const StatsCard: React.FC<StatsCardProps> = ({
  title,
  value,
  change,
  isPositive = true,
  icon: Icon,
  iconColor = "text-indigo-400",
  iconBg = "bg-indigo-500/10",
}) => {
  return (
    <Card className="p-5 flex items-center justify-between">
      <div className="space-y-1">
        <span className="text-xs text-slate-400 font-medium">{title}</span>
        <div className="text-2xl font-bold text-white">{value}</div>
        {change && (
          <p className={cn("text-[11px] font-medium flex items-center gap-1", isPositive ? "text-emerald-400" : "text-rose-400")}>
            <span>{isPositive ? "↑" : "↓"} {change}</span>
            <span className="text-slate-500 font-normal">vs last month</span>
          </p>
        )}
      </div>
      <div className={cn("p-3 rounded-xl", iconBg, iconColor)}>
        <Icon className="h-6 w-6" />
      </div>
    </Card>
  );
};
""")

write("frontend/src/pages/analytics/AnalyticsDashboardPage.tsx", """
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
""")

write("frontend/src/pages/admin/ModerationQueuePage.tsx", """
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
""")

write("frontend/src/pages/admin/AuditLogsPage.tsx", """
import React from "react";
import { Card } from "../../components/ui/card";
import { Badge } from "../../components/ui/badge";
import { Shield, Clock, Search } from "lucide-react";

export const AuditLogsPage: React.FC = () => {
  const logs = [
    { id: "1", action: "USER_AUTHENTICATION", actor: "admin@ailms.com", ip: "192.168.1.45", time: "2m ago", status: "SUCCESS" },
    { id: "2", action: "COURSE_STATE_TRANSITION", actor: "instructor@ailms.com", ip: "10.0.4.12", time: "15m ago", status: "SUCCESS" },
    { id: "3", action: "API_TOKEN_ROTATION", actor: "admin@ailms.com", ip: "192.168.1.45", time: "1h ago", status: "SUCCESS" },
    { id: "4", action: "FAILED_LOGIN_ATTEMPT", actor: "unknown@attacker.com", ip: "45.33.32.156", time: "3h ago", status: "BLOCKED" },
  ];

  return (
    <div className="space-y-6 max-w-5xl mx-auto">
      <div>
        <h1 className="text-2xl font-bold text-white">System Audit Trail</h1>
        <p className="text-sm text-slate-400">Immutable security logs, administrative events, and authentication attempts</p>
      </div>

      <Card className="p-0 overflow-hidden border-slate-800 bg-slate-950/60">
        <table className="w-full text-left text-xs">
          <thead className="bg-slate-900/80 text-slate-400 border-b border-slate-800">
            <tr>
              <th className="p-3.5">Action Event</th>
              <th className="p-3.5">Actor Identity</th>
              <th className="p-3.5">Source IP</th>
              <th className="p-3.5">Timestamp</th>
              <th className="p-3.5">Security Status</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800/60 text-slate-300">
            {logs.map(log => (
              <tr key={log.id} className="hover:bg-slate-900/40 transition-colors">
                <td className="p-3.5 font-mono font-medium text-white">{log.action}</td>
                <td className="p-3.5">{log.actor}</td>
                <td className="p-3.5 font-mono text-slate-400">{log.ip}</td>
                <td className="p-3.5 text-slate-500">{log.time}</td>
                <td className="p-3.5">
                  <Badge variant={log.status === "SUCCESS" ? "success" : "danger"}>{log.status}</Badge>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </Card>
    </div>
  );
};
""")

write("frontend/src/pages/profile/UserProfilePage.tsx", """
import React, { useState } from "react";
import { Card } from "../../components/ui/card";
import { Button } from "../../components/ui/button";
import { Input } from "../../components/ui/input";
import { Badge } from "../../components/ui/badge";
import { User, Shield, Key, Bell, Check } from "lucide-react";
import { useAuth } from "../../context/AuthContext";

export const UserProfilePage: React.FC = () => {
  const { user } = useAuth();
  const [firstName, setFirstName] = useState(user?.firstName || "Alex");
  const [lastName, setLastName] = useState(user?.lastName || "Learner");
  const [isSaved, setIsSaved] = useState(false);

  const handleSave = (e: React.FormEvent) => {
    e.preventDefault();
    setIsSaved(true);
    setTimeout(() => setIsSaved(false), 2000);
  };

  return (
    <div className="space-y-6 max-w-4xl mx-auto">
      <div>
        <h1 className="text-2xl font-bold text-white">Learner Profile & Security</h1>
        <p className="text-sm text-slate-400">Manage account information, multi-factor authentication, and notifications</p>
      </div>

      <Card className="p-6 space-y-6 bg-slate-900/80 border-slate-800">
        <div className="flex items-center gap-4 border-b border-slate-800 pb-6">
          <div className="h-16 w-16 rounded-full bg-indigo-600/20 text-indigo-400 flex items-center justify-center text-xl font-bold border border-indigo-500/30">
            {firstName.charAt(0)}{lastName.charAt(0)}
          </div>
          <div>
            <h2 className="text-lg font-bold text-white">{firstName} {lastName}</h2>
            <p className="text-xs text-slate-400">{user?.email || "alex.learner@enterprise.com"}</p>
            <Badge variant="primary" className="mt-1">{user?.role || "STUDENT"}</Badge>
          </div>
        </div>

        <form onSubmit={handleSave} className="space-y-4">
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div className="space-y-1">
              <label className="text-xs text-slate-400 font-medium">First Name</label>
              <Input value={firstName} onChange={e => setFirstName(e.target.value)} />
            </div>
            <div className="space-y-1">
              <label className="text-xs text-slate-400 font-medium">Last Name</label>
              <Input value={lastName} onChange={e => setLastName(e.target.value)} />
            </div>
          </div>

          <div className="pt-4 flex items-center justify-between">
            {isSaved && <span className="text-xs text-emerald-400 flex items-center gap-1"><Check className="h-4 w-4" /> Profile changes saved</span>}
            <Button type="submit" variant="primary">Save Changes</Button>
          </div>
        </form>
      </Card>
    </div>
  );
};
""")

print("Part 2 UI components and Pages written.")
