import React, { useState } from "react";
import { Card } from "../../components/ui/card";
import { Button } from "../../components/ui/button";
import { Input } from "../../components/ui/input";
import { Badge } from "../../components/ui/badge";
import { User, Shield, Key, Bell, Check } from "lucide-react";
import { useAuth } from "../../context/AuthContext";

export const UserProfilePage: React.FC = () => {
  const { user } = useAuth();
  const [firstName, setFirstName] = useState(user?.firstName || "Alex");
  const [lastName, setLastName] = useState(user?.lastName || "Learner");
  const [isSaved, setIsSaved] = useState(false);

  const handleSave = (e: React.FormEvent) => {
    e.preventDefault();
    setIsSaved(true);
    setTimeout(() => setIsSaved(false), 2000);
  };

  return (
    <div className="space-y-6 max-w-4xl mx-auto">
      <div>
        <h1 className="text-2xl font-bold text-white">Learner Profile & Security</h1>
        <p className="text-sm text-slate-400">Manage account information, multi-factor authentication, and notifications</p>
      </div>

      <Card className="p-6 space-y-6 bg-slate-900/80 border-slate-800">
        <div className="flex items-center gap-4 border-b border-slate-800 pb-6">
          <div className="h-16 w-16 rounded-full bg-indigo-600/20 text-indigo-400 flex items-center justify-center text-xl font-bold border border-indigo-500/30">
            {firstName.charAt(0)}{lastName.charAt(0)}
          </div>
          <div>
            <h2 className="text-lg font-bold text-white">{firstName} {lastName}</h2>
            <p className="text-xs text-slate-400">{user?.email || "alex.learner@enterprise.com"}</p>
            <Badge variant="primary" className="mt-1">{user?.role || "STUDENT"}</Badge>
          </div>
        </div>

        <form onSubmit={handleSave} className="space-y-4">
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div className="space-y-1">
              <label className="text-xs text-slate-400 font-medium">First Name</label>
              <Input value={firstName} onChange={e => setFirstName(e.target.value)} />
            </div>
            <div className="space-y-1">
              <label className="text-xs text-slate-400 font-medium">Last Name</label>
              <Input value={lastName} onChange={e => setLastName(e.target.value)} />
            </div>
          </div>

          <div className="pt-4 flex items-center justify-between">
            {isSaved && <span className="text-xs text-emerald-400 flex items-center gap-1"><Check className="h-4 w-4" /> Profile changes saved</span>}
            <Button type="submit" variant="primary">Save Changes</Button>
          </div>
        </form>
      </Card>
    </div>
  );
};
