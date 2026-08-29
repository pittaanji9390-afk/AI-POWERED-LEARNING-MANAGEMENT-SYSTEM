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
