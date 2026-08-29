import React, { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { Button } from "../../components/ui/button";
import { Input } from "../../components/ui/input";
import { Card } from "../../components/ui/card";
import { Sparkles } from "lucide-react";

export const RegisterPage: React.FC = () => {
  const [email, setEmail] = useState("");
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const navigate = useNavigate();

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    navigate("/login");
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-950 p-4">
      <Card className="w-full max-w-md p-8 border-slate-800 bg-slate-900/90">
        <div className="flex flex-col items-center text-center mb-8">
          <div className="h-12 w-12 rounded-xl bg-indigo-600 flex items-center justify-center text-white mb-3">
            <Sparkles className="h-6 w-6" />
          </div>
          <h1 className="text-2xl font-bold text-white">Create Account</h1>
          <p className="text-sm text-slate-400 mt-1">Start your AI-powered learning journey</p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="grid grid-cols-2 gap-3">
            <Input label="First Name" value={firstName} onChange={e => setFirstName(e.target.value)} required />
            <Input label="Last Name" value={lastName} onChange={e => setLastName(e.target.value)} required />
          </div>
          <Input label="Email Address" type="email" value={email} onChange={e => setEmail(e.target.value)} required />
          <Input label="Password" type="password" required />
          <Button type="submit" className="w-full mt-2" variant="primary">
            Register
          </Button>
        </form>

        <div className="mt-4 text-center text-xs text-slate-400">
          Already have an account? <Link to="/login" className="text-indigo-400 hover:underline">Sign In</Link>
        </div>
      </Card>
    </div>
  );
};
