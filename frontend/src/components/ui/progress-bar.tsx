import React from "react";
import { cn } from "../../lib/utils";

export const ProgressBar: React.FC<{ progress: number; className?: string }> = ({ progress, className }) => {
  const clamped = Math.min(100, Math.max(0, progress));
  return (
    <div className={cn("w-full bg-slate-800 rounded-full h-2 overflow-hidden", className)}>
      <div className="bg-indigo-500 h-2 rounded-full transition-all duration-300" style={{ width: `${clamped}%` }} />
    </div>
  );
};
