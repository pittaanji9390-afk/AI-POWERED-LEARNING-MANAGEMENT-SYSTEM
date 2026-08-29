import React, { useState } from "react";
import { Card } from "../../components/ui/card";
import { Button } from "../../components/ui/button";
import { Input } from "../../components/ui/input";
import { Badge } from "../../components/ui/badge";
import { MessageSquare, ThumbsUp, Sparkles, Send } from "lucide-react";

export const DiscussionBoardPage: React.FC = () => {
  const [posts, setPosts] = useState([
    {
      id: "p1",
      title: "How does the pgvector HNSW indexing compare to IVFFlat for sub-millisecond retrieval?",
      author: "Samantha Ray",
      time: "2 hours ago",
      upvotes: 14,
      comments: 3,
      tag: "AI Architecture",
    },
    {
      id: "p2",
      title: "Handling distributed sagas vs two-phase commit in tenant-partitioned microservices",
      author: "David Chen",
      time: "5 hours ago",
      upvotes: 22,
      comments: 7,
      tag: "Architecture",
    },
  ]);

  const [newTitle, setNewTitle] = useState("");

  const handlePost = (e: React.FormEvent) => {
    e.preventDefault();
    if (!newTitle.trim()) return;
    setPosts(prev => [
      {
        id: `p-${Date.now()}`,
        title: newTitle,
        author: "Alex Learner",
        time: "Just now",
        upvotes: 1,
        comments: 0,
        tag: "Discussion",
      },
      ...prev,
    ]);
    setNewTitle("");
  };

  return (
    <div className="space-y-6 max-w-5xl mx-auto">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white">Course Discussions & Community</h1>
          <p className="text-sm text-slate-400">Collaborate with peers, ask instructors, and get AI-assisted answers</p>
        </div>
      </div>

      <Card className="p-4 bg-slate-900/60">
        <form onSubmit={handlePost} className="flex gap-2">
          <Input 
            placeholder="Start a new discussion topic or ask a technical question..." 
            value={newTitle}
            onChange={e => setNewTitle(e.target.value)}
          />
          <Button type="submit" variant="primary" className="flex items-center gap-1">
            <Send className="h-4 w-4" />
            <span>Post</span>
          </Button>
        </form>
      </Card>

      <div className="space-y-4">
        {posts.map(post => (
          <Card key={post.id} className="p-5 flex items-start justify-between">
            <div className="space-y-2">
              <div className="flex items-center gap-2">
                <Badge variant="primary">{post.tag}</Badge>
                <span className="text-xs text-slate-500">Posted by {post.author} • {post.time}</span>
              </div>
              <h3 className="text-base font-semibold text-white">{post.title}</h3>
            </div>
            <div className="flex items-center gap-4 text-xs text-slate-400">
              <button className="flex items-center gap-1 hover:text-indigo-400 transition-colors">
                <ThumbsUp className="h-4 w-4" />
                <span>{post.upvotes}</span>
              </button>
              <div className="flex items-center gap-1">
                <MessageSquare className="h-4 w-4" />
                <span>{post.comments}</span>
              </div>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
};
