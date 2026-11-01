import React, { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { Bot, User, Copy, Check, Sparkles } from 'lucide-react';
import ToolExecutionBadge from './ToolExecutionBadge';

export default function MessageItem({ message, onTriggerConfirmation }) {
  const isUser = message.role === 'user';
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText(message.content);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  // Combine tool calls and tool results
  const toolCalls = message.tool_calls || [];
  const toolResults = message.tool_results || [];

  return (
    <div
      className={`group w-full py-4 px-3 sm:px-6 transition-colors ${
        isUser
          ? 'bg-transparent'
          : 'bg-gray-50/70 dark:bg-[#1a1a1a]/60 border-y border-gray-100/80 dark:border-neutral-800/60'
      }`}
    >
      <div className="max-w-3xl mx-auto flex gap-3 sm:gap-4 items-start">
        {/* Avatar */}
        <div
          className={`shrink-0 w-8 h-8 rounded-full flex items-center justify-center text-xs font-semibold shadow-sm ${
            isUser
              ? 'bg-gradient-to-tr from-purple-600 to-indigo-600 text-white'
              : 'bg-emerald-600 dark:bg-emerald-600 text-white'
          }`}
        >
          {isUser ? <User className="w-4 h-4" /> : <Sparkles className="w-4 h-4" />}
        </div>

        {/* Content Area */}
        <div className="flex-1 min-w-0 space-y-2">
          {/* Header */}
          <div className="flex items-center justify-between text-xs text-gray-400 dark:text-gray-500 font-medium">
            <span>{isUser ? 'You' : 'Assistant'}</span>
            {!isUser && message.content && (
              <button
                onClick={handleCopy}
                className="opacity-0 group-hover:opacity-100 transition-opacity p-1 rounded hover:bg-gray-200 dark:hover:bg-neutral-800 text-gray-500 hover:text-gray-800 dark:hover:text-gray-200 flex items-center gap-1"
                title="Copy text"
              >
                {copied ? (
                  <>
                    <Check className="w-3.5 h-3.5 text-green-500" />
                    <span className="text-[11px] text-green-500">Copied</span>
                  </>
                ) : (
                  <>
                    <Copy className="w-3.5 h-3.5" />
                    <span className="text-[11px]">Copy</span>
                  </>
                )}
              </button>
            )}
          </div>

          {/* Tool Execution Badges */}
          {!isUser && (toolCalls.length > 0 || toolResults.length > 0) && (
            <div className="space-y-1 mb-2">
              {toolCalls.map((tc, idx) => {
                const tr = toolResults.find(r => r.call_id === tc.id || r.name === tc.name) || toolResults[idx];
                return (
                  <ToolExecutionBadge
                    key={tc.id || idx}
                    toolCall={tc}
                    toolResult={tr}
                  />
                );
              })}
              {/* Results without calls if any */}
              {toolResults
                .filter(tr => !toolCalls.some(tc => tc.id === tr.call_id || tc.name === tr.name))
                .map((tr, idx) => (
                  <ToolExecutionBadge key={`res-${idx}`} toolResult={tr} />
                ))}
            </div>
          )}

          {/* Main Message Markdown Content */}
          <div className="prose dark:prose-invert max-w-none text-sm sm:text-base leading-relaxed text-gray-800 dark:text-gray-200 break-words">
            <ReactMarkdown remarkPlugins={[remarkGfm]}>
              {message.content}
            </ReactMarkdown>
          </div>

          {/* Pending Confirmation Callout Action */}
          {message.status === 'pending_confirmation' && onTriggerConfirmation && (
            <div className="pt-2">
              <button
                onClick={() => onTriggerConfirmation(message)}
                className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-lg text-xs font-semibold bg-amber-500/10 hover:bg-amber-500/20 text-amber-600 dark:text-amber-400 border border-amber-300 dark:border-amber-700/50 transition-colors shadow-sm"
              >
                Respond to Consequential Action Request
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
