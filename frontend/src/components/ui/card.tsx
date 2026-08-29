import React from "react";
import { cn } from "../../lib/utils";

export const Card: React.FC<React.HTMLAttributes<HTMLDivElement>> = ({ className, children, ...props }) => (
  <div className={cn("bg-slate-900/70 backdrop-blur-sm border border-slate-800/80 rounded-xl p-5 shadow-sm", className)} {...props}>
    {children}
  </div>
);
