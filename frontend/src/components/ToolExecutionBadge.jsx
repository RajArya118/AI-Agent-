import React, { useState } from 'react';
import { 
  Calculator, 
  Globe, 
  FileText, 
  ShieldAlert, 
  ChevronDown, 
  ChevronUp, 
  CheckCircle2, 
  AlertCircle,
  Clock,
  ExternalLink
} from 'lucide-react';

export default function ToolExecutionBadge({ toolCall, toolResult }) {
  const [expanded, setExpanded] = useState(false);
  const toolName = toolCall?.name || toolResult?.name || 'tool';
  const status = toolResult?.status || 'running';
  const executionTime = toolResult?.execution_time_ms;

  const getToolMeta = () => {
    switch (toolName) {
      case 'calculator':
        return {
          title: 'Calculator',
          icon: <Calculator className="w-4 h-4 text-emerald-500" />,
          bgColor: 'bg-emerald-50 dark:bg-emerald-950/30 border-emerald-200 dark:border-emerald-800/50',
          badgeColor: 'bg-emerald-500/10 text-emerald-700 dark:text-emerald-400',
          preview: toolCall?.arguments?.expression 
            ? `calc: ${toolCall.arguments.expression}`
            : 'Mathematical computation'
        };
      case 'web_search':
        return {
          title: 'Web Search',
          icon: <Globe className="w-4 h-4 text-blue-500" />,
          bgColor: 'bg-blue-50 dark:bg-blue-950/30 border-blue-200 dark:border-blue-800/50',
          badgeColor: 'bg-blue-500/10 text-blue-700 dark:text-blue-400',
          preview: toolCall?.arguments?.query 
            ? `query: "${toolCall.arguments.query}"`
            : 'Web search lookup'
        };
      case 'read_document':
        return {
          title: 'Document Reader',
          icon: <FileText className="w-4 h-4 text-purple-500" />,
          bgColor: 'bg-purple-50 dark:bg-purple-950/30 border-purple-200 dark:border-purple-800/50',
          badgeColor: 'bg-purple-500/10 text-purple-700 dark:text-purple-400',
          preview: toolResult?.result?.document_name
            ? `read: ${toolResult.result.document_name}`
            : 'Document content inspection'
        };
      case 'request_consequential_action':
        return {
          title: 'Security Guard',
          icon: <ShieldAlert className="w-4 h-4 text-amber-500" />,
          bgColor: 'bg-amber-50 dark:bg-amber-950/30 border-amber-200 dark:border-amber-800/50',
          badgeColor: 'bg-amber-500/10 text-amber-700 dark:text-amber-400',
          preview: 'Consequential action confirmation'
        };
      default:
        return {
          title: toolName,
          icon: <Clock className="w-4 h-4 text-gray-500" />,
          bgColor: 'bg-gray-50 dark:bg-neutral-800 border-gray-200 dark:border-neutral-700',
          badgeColor: 'bg-gray-500/10 text-gray-700 dark:text-gray-400',
          preview: 'Tool execution'
        };
    }
  };

  const meta = getToolMeta();

  return (
    <div className={`my-2 rounded-xl border ${meta.bgColor} transition-all overflow-hidden text-xs sm:text-sm`}>
      {/* Header bar */}
      <button
        type="button"
        onClick={() => setExpanded(!expanded)}
        className="w-full flex items-center justify-between p-2.5 sm:px-3 text-left hover:bg-black/5 dark:hover:bg-white/5 transition-colors"
      >
        <div className="flex items-center gap-2 overflow-hidden pr-2">
          {meta.icon}
          <span className="font-semibold text-gray-800 dark:text-gray-200">
            {meta.title}
          </span>
          <span className="text-gray-500 dark:text-gray-400 truncate text-xs">
            {meta.preview}
          </span>
        </div>

        <div className="flex items-center gap-2 shrink-0">
          {executionTime != null && (
            <span className="text-[11px] text-gray-400 dark:text-gray-500 hidden sm:inline">
              {executionTime}ms
            </span>
          )}
          {status === 'success' ? (
            <span className="flex items-center gap-1 text-[11px] px-2 py-0.5 rounded-full font-medium bg-green-500/10 text-green-600 dark:text-green-400">
              <CheckCircle2 className="w-3 h-3" /> Done
            </span>
          ) : status === 'requires_confirmation' ? (
            <span className="flex items-center gap-1 text-[11px] px-2 py-0.5 rounded-full font-medium bg-amber-500/10 text-amber-600 dark:text-amber-400">
              <AlertCircle className="w-3 h-3" /> Confirmation Required
            </span>
          ) : (
            <span className="flex items-center gap-1 text-[11px] px-2 py-0.5 rounded-full font-medium bg-blue-500/10 text-blue-600 dark:text-blue-400">
              <Clock className="w-3 h-3 animate-spin" /> In Progress
            </span>
          )}
          {expanded ? (
            <ChevronUp className="w-4 h-4 text-gray-400" />
          ) : (
            <ChevronDown className="w-4 h-4 text-gray-400" />
          )}
        </div>
      </button>

      {/* Expanded Details Body */}
      {expanded && (
        <div className="p-3 border-t border-black/5 dark:border-white/5 bg-white/50 dark:bg-black/20 space-y-2 text-xs">
          {/* Tool Arguments */}
          {toolCall?.arguments && (
            <div>
              <div className="font-medium text-gray-500 dark:text-gray-400 mb-1">Input Parameters:</div>
              <pre className="p-2 rounded bg-black/5 dark:bg-black/40 overflow-x-auto text-gray-800 dark:text-gray-200 font-mono">
                {JSON.stringify(toolCall.arguments, null, 2)}
              </pre>
            </div>
          )}

          {/* Specific tool result views */}
          {toolName === 'web_search' && toolResult?.result?.results && (
            <div>
              <div className="font-medium text-gray-500 dark:text-gray-400 mb-1">Discovered Sources:</div>
              <div className="space-y-1.5 max-h-48 overflow-y-auto">
                {toolResult.result.results.map((res, i) => (
                  <div key={i} className="p-2 rounded bg-black/5 dark:bg-black/30">
                    <a
                      href={res.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="font-medium text-blue-600 dark:text-blue-400 hover:underline flex items-center gap-1"
                    >
                      {res.title} <ExternalLink className="w-3 h-3 inline" />
                    </a>
                    <p className="text-gray-600 dark:text-gray-300 text-[11px] mt-0.5 line-clamp-2">
                      {res.snippet}
                    </p>
                  </div>
                ))}
              </div>
            </div>
          )}

          {toolName === 'calculator' && toolResult?.result && (
            <div>
              <div className="font-medium text-gray-500 dark:text-gray-400 mb-1">Calculation:</div>
              <div className="p-2 rounded bg-black/5 dark:bg-black/40 font-mono text-emerald-600 dark:text-emerald-400 font-bold">
                {toolResult.result.expression} = {toolResult.result.result}
              </div>
            </div>
          )}

          {toolName === 'read_document' && toolResult?.result && (
            <div>
              <div className="font-medium text-gray-500 dark:text-gray-400 mb-1">
                Document Content Preview ({toolResult.result.document_name}):
              </div>
              <div className="p-2 rounded bg-black/5 dark:bg-black/40 max-h-40 overflow-y-auto font-mono text-[11px] text-gray-700 dark:text-gray-300 whitespace-pre-wrap">
                {toolResult.result.content}
              </div>
            </div>
          )}

          {/* Fallback raw output */}
          {toolResult?.result && !['web_search', 'calculator', 'read_document'].includes(toolName) && (
            <div>
              <div className="font-medium text-gray-500 dark:text-gray-400 mb-1">Output Result:</div>
              <pre className="p-2 rounded bg-black/5 dark:bg-black/40 overflow-x-auto text-gray-800 dark:text-gray-200 font-mono">
                {JSON.stringify(toolResult.result, null, 2)}
              </pre>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
