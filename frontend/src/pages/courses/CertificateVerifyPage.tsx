import React from "react";
import { useParams, Link } from "react-router-dom";
import { Card } from "../../components/ui/card";
import { Badge } from "../../components/ui/badge";
import { Award, ShieldCheck, CheckCircle, ExternalLink } from "lucide-react";

export const CertificateVerifyPage: React.FC = () => {
  const { verificationCode = "AILMS-CERT-98234-2026" } = useParams();

  return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center p-4">
      <Card className="max-w-lg w-full p-8 border-indigo-500/40 bg-slate-900/90 text-center space-y-6">
        <div className="h-16 w-16 bg-emerald-500/10 text-emerald-400 rounded-full flex items-center justify-center mx-auto">
          <ShieldCheck className="h-8 w-8" />
        </div>

        <div>
          <Badge variant="success" className="mb-2">Cryptographically Verified</Badge>
          <h1 className="text-2xl font-bold text-white">Certificate of Completion</h1>
          <p className="text-xs text-slate-400 mt-1">Verification Code: {verificationCode}</p>
        </div>

        <div className="p-4 bg-slate-950/80 rounded-xl border border-slate-800 text-left text-xs space-y-3">
          <div className="flex justify-between">
            <span className="text-slate-500">Student Name:</span>
            <span className="font-semibold text-white">Alex Learner</span>
          </div>
          <div className="flex justify-between">
            <span className="text-slate-500">Course:</span>
            <span className="font-semibold text-white">Advanced Distributed Systems</span>
          </div>
          <div className="flex justify-between">
            <span className="text-slate-500">Issued On:</span>
            <span className="font-semibold text-white">August 29, 2026</span>
          </div>
          <div className="flex justify-between">
            <span className="text-slate-500">Issuing Authority:</span>
            <span className="font-semibold text-indigo-400">Aegis Enterprise LMS</span>
          </div>
        </div>

        <Link to="/" className="text-xs text-indigo-400 hover:underline flex items-center justify-center gap-1">
          <span>Return to Learning Platform</span>
        </Link>
      </Card>
    </div>
  );
};
