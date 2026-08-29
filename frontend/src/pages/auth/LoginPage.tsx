import React, { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";
import { Button } from "../../components/ui/button";
import { Input } from "../../components/ui/input";
import { Card } from "../../components/ui/card";
import { Sparkles } from "lucide-react";

export const LoginPage: React.FC = () => {
  const [email, setEmail] = useState("alex.learner@ailms.platform");
  const [password, setPassword] = useState("Password@123");
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    login("mock-token", {
      id: "usr-1",
      email,
      firstName: "Alex",
      lastName: "Learner",
      role: "STUDENT",
      permissions: ["course:read"],
    });
    navigate("/dashboard");
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-950 p-4">
      <Card className="w-full max-w-md p-8 border-slate-800 bg-slate-900/90">
        <div className="flex flex-col items-center text-center mb-8">
          <div className="h-12 w-12 rounded-xl bg-indigo-600 flex items-center justify-center text-white mb-3">
            <Sparkles className="h-6 w-6" />
          </div>
          <h1 className="text-2xl font-bold text-white">Welcome Back</h1>
          <p className="text-sm text-slate-400 mt-1">Sign in to your enterprise learning workspace</p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <Input 
            label="Email Address" 
            type="email" 
            value={email} 
            onChange={(e) => setEmail(e.target.value)} 
            required 
          />
          <Input 
            label="Password" 
            type="password" 
            value={password} 
            onChange={(e) => setPassword(e.target.value)} 
            required 
          />
          <Button type="submit" className="w-full mt-2" variant="primary">
            Sign In
          </Button>
        </form>

        <div className="mt-6 text-center text-xs text-slate-500">
          Demo platform initialized with mock security credentials.
        </div>
      </Card>
    </div>
  );
};
