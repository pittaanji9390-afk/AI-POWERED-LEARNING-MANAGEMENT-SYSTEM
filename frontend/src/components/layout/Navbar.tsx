import React from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";
import { useTenant } from "../../context/TenantContext";
import { Button } from "../ui/button";
import { Badge } from "../ui/badge";
import { BookOpen, Sparkles, User, LogOut, Shield, CreditCard } from "lucide-react";

export const Navbar: React.FC = () => {
  const { user, isAuthenticated, logout } = useAuth();
  const { tenantName } = useTenant();
  const navigate = useNavigate();

  return (
    <header className="h-16 border-b border-slate-800 bg-slate-950/80 backdrop-blur sticky top-0 z-40 px-6 flex items-center justify-between">
      <div className="flex items-center gap-6">
        <Link to="/" className="flex items-center gap-2.5 text-white font-bold text-lg">
          <div className="h-8 w-8 rounded-lg bg-indigo-600 flex items-center justify-center text-white">
            <Sparkles className="h-4 w-4" />
          </div>
          <span className="bg-clip-text text-transparent bg-gradient-to-r from-white via-slate-200 to-indigo-300">
            AegisLMS
          </span>
        </Link>
        <Badge variant="primary">{tenantName}</Badge>
      </div>

      <nav className="hidden md:flex items-center gap-6 text-sm">
        <Link to="/courses" className="text-slate-400 hover:text-white transition-colors">Catalog</Link>
        <Link to="/pricing" className="text-slate-400 hover:text-white transition-colors">Pricing</Link>
        <Link to="/dashboard" className="text-slate-400 hover:text-white transition-colors">Dashboard</Link>
        <Link to="/ai-tutor" className="flex items-center gap-1 text-indigo-400 hover:text-indigo-300 transition-colors">
          <Sparkles className="h-3.5 w-3.5" />
          <span>AI Tutor</span>
        </Link>
      </nav>

      <div className="flex items-center gap-3">
        {isAuthenticated && user ? (
          <div className="flex items-center gap-3">
            <div className="text-right hidden sm:block">
              <p className="text-xs font-medium text-white">{user.firstName} {user.lastName}</p>
              <p className="text-[10px] text-slate-400 uppercase tracking-wider">{user.role}</p>
            </div>
            <button 
              onClick={logout}
              title="Sign out"
              className="p-2 rounded-lg hover:bg-slate-800 text-slate-400 hover:text-white transition-colors"
            >
              <LogOut className="h-4 w-4" />
            </button>
          </div>
        ) : (
          <div className="flex items-center gap-2">
            <Button variant="ghost" size="sm" onClick={() => navigate("/login")}>Sign In</Button>
            <Button variant="primary" size="sm" onClick={() => navigate("/register")}>Get Started</Button>
          </div>
        )}
      </div>
    </header>
  );
};
