import React from "react";
import { Card } from "../../components/ui/card";
import { Badge } from "../../components/ui/badge";
import { Button } from "../../components/ui/button";
import { Users, Building, ShieldAlert, DollarSign, Activity, Cpu } from "lucide-react";

export const AdminDashboard: React.FC = () => {
  return (
    <div className="space-y-8 max-w-6xl mx-auto">
      <div>
        <h1 className="text-2xl font-bold text-white">Platform Administration</h1>
        <p className="text-sm text-slate-400">Multi-tenant management, AI compute health, and platform governance</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card className="p-5 flex items-center gap-4">
          <div className="p-3 bg-indigo-500/10 text-indigo-400 rounded-xl">
            <Building className="h-6 w-6" />
          </div>
          <div>
            <div className="text-2xl font-bold text-white">18</div>
            <div className="text-xs text-slate-400">Active Organizations</div>
          </div>
        </Card>

        <Card className="p-5 flex items-center gap-4">
          <div className="p-3 bg-emerald-500/10 text-emerald-400 rounded-xl">
            <DollarSign className="h-6 w-6" />
          </div>
          <div>
            <div className="text-2xl font-bold text-white">$48,290</div>
            <div className="text-xs text-slate-400">Monthly SaaS ARR</div>
          </div>
        </Card>

        <Card className="p-5 flex items-center gap-4">
          <div className="p-3 bg-purple-500/10 text-purple-400 rounded-xl">
            <Cpu className="h-6 w-6" />
          </div>
          <div>
            <div className="text-2xl font-bold text-white">1.2M</div>
            <div className="text-xs text-slate-400">AI Tokens Processed Today</div>
          </div>
        </Card>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Card className="space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="font-semibold text-white text-base">Tenant Organizations</h3>
            <Badge variant="primary">18 Live</Badge>
          </div>
          <div className="space-y-2 text-sm">
            <div className="p-3 bg-slate-950/60 rounded-lg flex items-center justify-between border border-slate-800">
              <div>
                <p className="font-medium text-white">Acme University</p>
                <p className="text-xs text-slate-500">Tier: ENTERPRISE (1,500 seats)</p>
              </div>
              <Badge variant="success">Active</Badge>
            </div>
            <div className="p-3 bg-slate-950/60 rounded-lg flex items-center justify-between border border-slate-800">
              <div>
                <p className="font-medium text-white">TechCorp Academy</p>
                <p className="text-xs text-slate-500">Tier: PRO (300 seats)</p>
              </div>
              <Badge variant="success">Active</Badge>
            </div>
          </div>
        </Card>

        <Card className="space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="font-semibold text-white text-base">System Telemetry & Health</h3>
            <Badge variant="success">100% Operational</Badge>
          </div>
          <div className="space-y-3 text-xs text-slate-400">
            <div className="flex justify-between py-1 border-b border-slate-800">
              <span>PostgreSQL + pgvector Latency</span>
              <span className="text-emerald-400 font-mono">1.8ms</span>
            </div>
            <div className="flex justify-between py-1 border-b border-slate-800">
              <span>Redis L2 Cache Hit Ratio</span>
              <span className="text-emerald-400 font-mono">96.4%</span>
            </div>
            <div className="flex justify-between py-1 border-b border-slate-800">
              <span>AI Provider SPI Mesh</span>
              <span className="text-indigo-400 font-mono">Mock/OpenAI Primary</span>
            </div>
            <div className="flex justify-between py-1">
              <span>Ingress Security WAF</span>
              <span className="text-emerald-400 font-mono">Active (Zero Breaches)</span>
            </div>
          </div>
        </Card>
      </div>
    </div>
  );
};
