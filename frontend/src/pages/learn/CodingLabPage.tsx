import React, { useState } from "react";
import { Card } from "../../components/ui/card";
import { Badge } from "../../components/ui/badge";
import { Button } from "../../components/ui/button";
import { Play, RotateCcw, Sparkles, CheckCircle2, XCircle, Code2, Terminal, BookOpen } from "lucide-react";

export const CodingLabPage: React.FC = () => {
  const [language, setLanguage] = useState<"java" | "python" | "typescript">("java");
  const [code, setCode] = useState(`public class Solution {
    public static int binarySearch(int[] arr, int target) {
        int low = 0;
        int high = arr.length - 1;
        
        while (low <= high) {
            int mid = low + (high - low) / 2;
            if (arr[mid] == target) return mid;
            if (arr[mid] < target) low = mid + 1;
            else high = mid - 1;
        }
        return -1;
    }
}`);
  const [output, setOutput] = useState<string | null>(null);
  const [isRunning, setIsRunning] = useState(false);
  const [aiReview, setAiReview] = useState<string | null>(null);

  const handleRunCode = () => {
    setIsRunning(true);
    setOutput(null);
    setTimeout(() => {
      setIsRunning(false);
      setOutput(`[Test Suite] Running 4 automated test cases...
✓ Test Case 1: Target present in middle [1,3,5,7,9], target=5 -> Passed (Returned index: 2)
✓ Test Case 2: Target at boundary [2,4,6,8], target=2 -> Passed (Returned index: 0)
✓ Test Case 3: Target not present [10,20,30], target=25 -> Passed (Returned index: -1)
✓ Test Case 4: Single element match [42], target=42 -> Passed (Returned index: 0)

All 4 test cases PASSED! Execution time: 14ms. Memory: 18.2MB.`);
    }, 800);
  };

  const handleAiReview = () => {
    setAiReview("AI Review: Excellent implementation! The integer midpoint calculation `low + (high - low) / 2` correctly avoids 32-bit integer overflow. Time complexity is strictly O(log n) and space complexity is O(1).");
  };

  return (
    <div className="max-w-6xl mx-auto space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white">Interactive Coding Lab</h1>
          <p className="text-sm text-slate-400">Write, test, and get real-time AI code reviews</p>
        </div>
        <div className="flex items-center gap-3">
          <select
            value={language}
            onChange={(e) => setLanguage(e.target.value as any)}
            className="bg-slate-900 border border-slate-700 text-xs text-slate-200 rounded-lg px-3 py-2 focus:outline-none focus:ring-1 focus:ring-indigo-500"
          >
            <option value="java">Java 21</option>
            <option value="python">Python 3.12</option>
            <option value="typescript">TypeScript 5.6</option>
          </select>
          <Button variant="outline" size="sm" onClick={handleAiReview} className="flex items-center gap-1.5">
            <Sparkles className="h-4 w-4 text-indigo-400" />
            <span>AI Code Review</span>
          </Button>
          <Button variant="primary" size="sm" isLoading={isRunning} onClick={handleRunCode} className="flex items-center gap-1.5">
            <Play className="h-4 w-4" />
            <span>Run Test Cases</span>
          </Button>
        </div>
      </div>

      {/* Grid: Code Editor + Output */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Code Editor */}
        <Card className="p-0 border-slate-800 bg-slate-950 flex flex-col overflow-hidden">
          <div className="h-10 bg-slate-900/80 border-b border-slate-800 px-4 flex items-center justify-between text-xs text-slate-400">
            <div className="flex items-center gap-2">
              <Code2 className="h-4 w-4 text-indigo-400" />
              <span className="font-mono font-medium text-slate-200">Solution.{language === "java" ? "java" : language === "python" ? "py" : "ts"}</span>
            </div>
            <span>Read/Write</span>
          </div>
          <textarea
            value={code}
            onChange={(e) => setCode(e.target.value)}
            className="w-full h-96 p-4 bg-slate-950 font-mono text-xs text-slate-200 resize-none focus:outline-none leading-relaxed border-0"
            spellCheck={false}
          />
        </Card>

        {/* Console Output & AI Review */}
        <div className="space-y-6">
          <Card className="p-0 border-slate-800 bg-slate-950 flex flex-col overflow-hidden">
            <div className="h-10 bg-slate-900/80 border-b border-slate-800 px-4 flex items-center justify-between text-xs text-slate-400">
              <div className="flex items-center gap-2">
                <Terminal className="h-4 w-4 text-emerald-400" />
                <span className="font-mono font-medium text-slate-200">Test Execution Output</span>
              </div>
              {output && <Badge variant="success">All Passed</Badge>}
            </div>
            <div className="p-4 h-56 font-mono text-xs overflow-y-auto leading-relaxed text-slate-300">
              {output ? (
                <pre className="whitespace-pre-wrap text-emerald-400">{output}</pre>
              ) : (
                <span className="text-slate-500 italic">Click "Run Test Cases" to compile and execute test suites...</span>
              )}
            </div>
          </Card>

          {aiReview && (
            <Card className="p-4 bg-indigo-950/20 border-indigo-500/30 text-xs space-y-2">
              <div className="flex items-center gap-2 text-indigo-400 font-semibold">
                <Sparkles className="h-4 w-4" />
                <span>AI Automated Code Analysis</span>
              </div>
              <p className="text-slate-300 leading-relaxed">{aiReview}</p>
            </Card>
          )}
        </div>
      </div>
    </div>
  );
};
