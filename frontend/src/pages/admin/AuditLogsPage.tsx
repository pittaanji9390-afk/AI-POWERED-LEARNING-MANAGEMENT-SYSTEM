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
