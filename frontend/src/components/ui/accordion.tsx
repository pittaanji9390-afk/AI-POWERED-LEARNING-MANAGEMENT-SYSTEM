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
