import React from "react";
import { NavLink } from "react-router-dom";
import { BookOpen, LayoutDashboard, Sparkles, GraduationCap, Award, Settings, ShieldCheck, CheckSquare } from "lucide-react";
import { cn } from "../../lib/utils";

export const Sidebar: React.FC = () => {
  const links = [
    { to: "/dashboard", label: "Overview", icon: LayoutDashboard },
    { to: "/courses", label: "Course Catalog", icon: BookOpen },
    { to: "/my-learning", label: "My Learning", icon: GraduationCap },
    { to: "/ai-tutor", label: "AI Tutor Studio", icon: Sparkles },
    { to: "/certificates", label: "Certificates", icon: Award },
    { to: "/admin", label: "Administration", icon: ShieldCheck },
  ];

  return (
    <aside className="w-64 border-r border-slate-800/80 bg-slate-950/40 p-4 space-y-1">
      <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider px-3 mb-2">
        Platform Menu
      </div>
      {links.map((item) => {
        const Icon = item.icon;
        return (
          <NavLink
            key={item.to}
            to={item.to}
            className={({ isActive }) =>
              cn(
                "flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-medium transition-colors",
                isActive
                  ? "bg-indigo-600/10 text-indigo-400 border border-indigo-500/20"
                  : "text-slate-400 hover:text-slate-200 hover:bg-slate-900/60"
              )
            }
          >
            <Icon className="h-4 w-4" />
            <span>{item.label}</span>
          </NavLink>
        );
      })}
    </aside>
  );
};
