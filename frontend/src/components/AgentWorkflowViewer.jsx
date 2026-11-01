import React, { useState } from 'react';
import { 
  CheckCircle2, 
  Clock, 
  Cpu, 
  Palette, 
  Database, 
  Server, 
  Layout, 
  ShieldCheck,
  ChevronDown,
  ChevronUp
} from 'lucide-react';

export default function AgentWorkflowViewer({ timeline = [], qaStatus = 'PASS', executionTime = 0 }) {
  const [expandedIndex, setExpandedIndex] = useState(null);

  const getAgentIcon = (name) => {
    switch (name) {
      case 'Planner Agent': return <Cpu className="w-4 h-4 text-purple-500" />;
      case 'UI/UX Agent': return <Palette className="w-4 h-4 text-pink-500" />;
      case 'Database Agent': return <Database className="w-4 h-4 text-emerald-500" />;
      case 'Backend Agent': return <Server className="w-4 h-4 text-blue-500" />;
      case 'Frontend Agent': return <Layout className="w-4 h-4 text-amber-500" />;
      case 'QA Agent': return <ShieldCheck className="w-4 h-4 text-teal-500" />;
      default: return <Cpu className="w-4 h-4 text-gray-400" />;
    }
  };

  return (
    <div className="bg-white dark:bg-neutral-900 border border-gray-200 dark:border-neutral-800 rounded-2xl p-4 sm:p-5 space-y-4 shadow-sm">
      {/* Header */}
      <div className="flex items-center justify-between border-b border-gray-100 dark:border-neutral-800/80 pb-3">
        <div className="flex items-center gap-2">
          <div className="w-2.5 h-2.5 rounded-full bg-emerald-500 animate-pulse" />
          <h4 className="font-bold text-sm text-gray-900 dark:text-gray-100">
            Multi-Agent Orchestrator Pipeline
          </h4>
        </div>

        <div className="flex items-center gap-2">
          <span className="text-xs px-2.5 py-0.5 rounded-full font-bold bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border border-emerald-500/20">
            QA: {qaStatus}
          </span>
          <span className="text-xs text-gray-400 font-mono">
            {executionTime}ms
          </span>
        </div>
      </div>

      {/* Timeline items */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
        {timeline.map((step, idx) => {
          const isExpanded = expandedIndex === idx;
          return (
            <div
              key={idx}
              className="border border-gray-100 dark:border-neutral-800 rounded-xl p-3 bg-gray-50/50 dark:bg-neutral-800/30 hover:border-gray-300 dark:hover:border-neutral-700 transition-all flex flex-col justify-between"
            >
              <div className="flex items-start justify-between gap-2">
                <div className="flex items-center gap-2">
                  <div className="p-1.5 rounded-lg bg-white dark:bg-neutral-800 shadow-2xs">
                    {getAgentIcon(step.agent)}
                  </div>
                  <div>
                    <div className="font-bold text-xs text-gray-900 dark:text-gray-100 leading-tight">
                      {step.agent}
                    </div>
                    <div className="text-[10px] text-gray-400 truncate max-w-[130px]">
                      {step.role}
                    </div>
                  </div>
                </div>

                <div className="flex items-center gap-1">
                  <CheckCircle2 className="w-3.5 h-3.5 text-emerald-500 shrink-0" />
                  <span className="text-[10px] text-gray-400 font-mono">{step.execution_time_ms}ms</span>
                </div>
              </div>

              {/* Toggle Output */}
              <div className="pt-2 mt-2 border-t border-gray-100 dark:border-neutral-800/60 flex justify-between items-center text-[11px]">
                <button
                  type="button"
                  onClick={() => setExpandedIndex(isExpanded ? null : idx)}
                  className="text-indigo-600 dark:text-indigo-400 font-semibold hover:underline flex items-center gap-1"
                >
                  <span>{isExpanded ? 'Hide Spec' : 'View Spec'}</span>
                  {isExpanded ? <ChevronUp className="w-3 h-3" /> : <ChevronDown className="w-3 h-3" />}
                </button>
              </div>

              {/* Expanded JSON details */}
              {isExpanded && step.output && (
                <pre className="mt-2 p-2 rounded-lg bg-black/5 dark:bg-black/50 text-[10px] font-mono text-gray-700 dark:text-gray-300 overflow-x-auto max-h-36">
                  {JSON.stringify(step.output, null, 2)}
                </pre>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
