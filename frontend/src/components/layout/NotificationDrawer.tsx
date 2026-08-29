import React, { useState } from "react";
import { Bell, Check, Trash2, BookOpen, Award, Sparkles, AlertCircle, X } from "lucide-react";
import { Badge } from "../ui/badge";
import { Button } from "../ui/button";

interface NotificationItem {
  id: string;
  title: string;
  body: string;
  type: "GRADE" | "ENROLLMENT" | "CERTIFICATE" | "AI_TIP";
  isRead: boolean;
  time: string;
}

const mockNotifications: NotificationItem[] = [
  {
    id: "n1",
    title: "Assessment Graded: Distributed Sagas",
    body: "Your submission received a score of 96/100 with detailed AI & instructor feedback.",
    type: "GRADE",
    isRead: false,
    time: "10m ago",
  },
  {
    id: "n2",
    title: "New AI Learning Path Recommendation",
    body: "Based on your progress, we unlocked 'High-Dimensional HNSW Vector Indexing'.",
    type: "AI_TIP",
    isRead: false,
    time: "1h ago",
  },
  {
    id: "n3",
    title: "Certificate Generated",
    body: "Congratulations! Your certificate for 'Advanced Distributed Systems' is now verified and available.",
    type: "CERTIFICATE",
    isRead: true,
    time: "1d ago",
  },
];

export const NotificationDrawer: React.FC<{ isOpen: boolean; onClose: () => void }> = ({ isOpen, onClose }) => {
  const [notifications, setNotifications] = useState(mockNotifications);

  if (!isOpen) return null;

  const unreadCount = notifications.filter((n) => !n.isRead).length;

  const markAllAsRead = () => {
    setNotifications((prev) => prev.map((n) => ({ ...n, isRead: true })));
  };

  const clearAll = () => {
    setNotifications([]);
  };

  const getTypeIcon = (type: NotificationItem["type"]) => {
    switch (type) {
      case "GRADE":
        return <Award className="h-4 w-4 text-emerald-400" />;
      case "CERTIFICATE":
        return <Award className="h-4 w-4 text-indigo-400" />;
      case "AI_TIP":
        return <Sparkles className="h-4 w-4 text-purple-400" />;
      default:
        return <Bell className="h-4 w-4 text-slate-400" />;
    }
  };

  return (
    <div className="fixed inset-y-0 right-0 z-50 w-full max-w-sm bg-slate-900 border-l border-slate-800 shadow-2xl flex flex-col">
      {/* Drawer Header */}
      <div className="p-4 border-b border-slate-800 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Bell className="h-4 w-4 text-indigo-400" />
          <h3 className="font-semibold text-white text-sm">Notifications</h3>
          {unreadCount > 0 && <Badge variant="primary">{unreadCount} new</Badge>}
        </div>
        <button onClick={onClose} className="p-1 rounded-lg hover:bg-slate-800 text-slate-400 hover:text-white">
          <X className="h-4 w-4" />
        </button>
      </div>

      {/* Action Bar */}
      {notifications.length > 0 && (
        <div className="px-4 py-2 bg-slate-950/60 border-b border-slate-800 flex items-center justify-between text-xs text-slate-400">
          <button onClick={markAllAsRead} className="hover:text-indigo-400 transition-colors">
            Mark all read
          </button>
          <button onClick={clearAll} className="hover:text-rose-400 transition-colors">
            Clear all
          </button>
        </div>
      )}

      {/* Notifications List */}
      <div className="flex-1 overflow-y-auto p-4 space-y-3">
        {notifications.length > 0 ? (
          notifications.map((item) => (
            <div
              key={item.id}
              className={`p-3.5 rounded-xl border transition-all space-y-1.5 ${
                item.isRead
                  ? "bg-slate-950/40 border-slate-800/60 opacity-70"
                  : "bg-slate-950/90 border-slate-800 shadow-sm"
              }`}
            >
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <div className="p-1.5 bg-slate-900 rounded-lg">{getTypeIcon(item.type)}</div>
                  <span className="text-xs font-semibold text-white">{item.title}</span>
                </div>
                <span className="text-[10px] text-slate-500">{item.time}</span>
              </div>
              <p className="text-xs text-slate-400 leading-relaxed pl-8">{item.body}</p>
            </div>
          ))
        ) : (
          <div className="h-full flex flex-col items-center justify-center text-center text-slate-500 space-y-2">
            <Bell className="h-8 w-8 text-slate-600" />
            <p className="text-xs">No new notifications</p>
          </div>
        )}
      </div>
    </div>
  );
};
