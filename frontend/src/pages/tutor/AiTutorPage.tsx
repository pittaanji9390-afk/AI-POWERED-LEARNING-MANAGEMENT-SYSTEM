import React, { useState } from "react";
import { Card } from "../../components/ui/card";
import { Button } from "../../components/ui/button";
import { Input } from "../../components/ui/input";
import { Badge } from "../../components/ui/badge";
import { Sparkles, Send, BookOpen, ShieldCheck } from "lucide-react";
import { AiChatMessage } from "../../types";

export const AiTutorPage: React.FC = () => {
  const [messages, setMessages] = useState<AiChatMessage[]>([
    {
      id: "m1",
      senderType: "AI",
      content: "Hello! I am your AI Course Assistant. I am grounded in your enrolled course documents. Ask me anything about distributed architectures, RAG, or quiz topics!",
      citations: ["Course Overview - Section 1"],
      createdAt: new Date().toISOString(),
    },
  ]);
  const [input, setInput] = useState("");

  const handleSend = (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMsg: AiChatMessage = {
      id: `usr-${Date.now()}`,
      senderType: "USER",
      content: input,
      createdAt: new Date().toISOString(),
    };

    const aiReply: AiChatMessage = {
      id: `ai-${Date.now()}`,
      senderType: "AI",
      content: `Based on your course materials on "${input}": Distributed caching with Redis and tenant-partitioned JPA repositories ensure sub-10ms query execution and strict isolation.`,
      citations: ["Advanced Distributed Systems - Module 2, Page 14"],
      createdAt: new Date().toISOString(),
    };

    setMessages(prev => [...prev, userMsg, aiReply]);
    setInput("");
  };

  return (
    <div className="max-w-4xl mx-auto h-[calc(100vh-8rem)] flex flex-col space-y-4">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="h-9 w-9 rounded-lg bg-indigo-600/20 text-indigo-400 flex items-center justify-center">
            <Sparkles className="h-5 w-5" />
          </div>
          <div>
            <h1 className="text-lg font-bold text-white">AI Tutor Studio</h1>
            <p className="text-xs text-slate-400">Contextual RAG Assistant & Socratic Mentor</p>
          </div>
        </div>
        <Badge variant="success" className="flex items-center gap-1">
          <ShieldCheck className="h-3.5 w-3.5" />
          <span>Grounded in Course Material</span>
        </Badge>
      </div>

      <Card className="flex-1 flex flex-col overflow-hidden p-4 border-slate-800 bg-slate-900/60">
        <div className="flex-1 overflow-y-auto space-y-4 pr-2">
          {messages.map(msg => (
            <div key={msg.id} className={`flex ${msg.senderType === "USER" ? "justify-end" : "justify-start"}`}>
              <div className={`max-w-[80%] rounded-xl p-4 text-sm ${
                msg.senderType === "USER" 
                  ? "bg-indigo-600 text-white" 
                  : "bg-slate-800/80 text-slate-200 border border-slate-700/60"
              }`}>
                <p className="leading-relaxed">{msg.content}</p>
                {msg.citations && msg.citations.length > 0 && (
                  <div className="mt-3 pt-2 border-t border-slate-700/40 text-[11px] text-indigo-300 flex items-center gap-1.5">
                    <BookOpen className="h-3.5 w-3.5" />
                    <span>Citation: {msg.citations.join(", ")}</span>
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>

        <form onSubmit={handleSend} className="pt-4 border-t border-slate-800 flex gap-2">
          <Input 
            value={input} 
            onChange={e => setInput(e.target.value)} 
            placeholder="Ask a concept question, request a quiz hint, or summarize a topic..." 
            className="flex-1"
          />
          <Button type="submit" variant="primary" className="px-5">
            <Send className="h-4 w-4" />
          </Button>
        </form>
      </Card>
    </div>
  );
};
