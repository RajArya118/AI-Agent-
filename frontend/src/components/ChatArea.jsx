import React, { useRef, useEffect } from 'react';
import { 
  Menu, 
  Sparkles, 
  Calculator, 
  Globe, 
  FileText, 
  ShieldAlert, 
  Paperclip,
  ChevronDown
} from 'lucide-react';
import MessageItem from './MessageItem';
import ChatInput from './ChatInput';

export default function ChatArea({
  conversation,
  messages,
  loading,
  onSendMessage,
  onToggleSidebar,
  onOpenUpload,
  attachedDocs,
  onRemoveDoc,
  onTriggerConfirmation,
  health
}) {
  const scrollRef = useRef(null);

  // Auto scroll to bottom
  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages, loading]);

  const starterPrompts = [
    {
      title: 'Safe Calculator',
      prompt: 'Calculate 145 * 380 + sqrt(4096) - sin(pi / 4)',
      icon: <Calculator className="w-5 h-5 text-emerald-500" />,
    },
    {
      title: 'Live Web Search',
      prompt: 'Search the web for the latest artificial intelligence agent innovations in 2026',
      icon: <Globe className="w-5 h-5 text-blue-500" />,
    },
    {
      title: 'Document Reader',
      prompt: 'Summarize the attached document and extract the key takeaways',
      icon: <FileText className="w-5 h-5 text-purple-500" />,
    },
    {
      title: 'Safety Guard Check',
      prompt: 'Please delete all messages in this conversation history',
      icon: <ShieldAlert className="w-5 h-5 text-amber-500" />,
    },
  ];

  return (
    <div className="flex-1 flex flex-col h-full bg-white dark:bg-[#212121] relative overflow-hidden">
      {/* Top Header Bar */}
      <header className="h-14 border-b border-gray-200 dark:border-neutral-800 flex items-center justify-between px-3 sm:px-6 bg-white/80 dark:bg-[#212121]/80 backdrop-blur-md z-10 shrink-0">
        <div className="flex items-center gap-2 sm:gap-3 truncate">
          <button
            type="button"
            onClick={onToggleSidebar}
            className="p-2 rounded-xl text-gray-500 hover:text-gray-800 dark:text-gray-400 dark:hover:text-gray-100 hover:bg-gray-100 dark:hover:bg-neutral-800 transition-colors"
            title="Toggle Sidebar"
          >
            <Menu className="w-5 h-5" />
          </button>

          <div className="flex items-center gap-2 truncate">
            <span className="font-semibold text-sm sm:text-base text-gray-800 dark:text-gray-100 truncate">
              {conversation?.title || 'New Chat'}
            </span>
          </div>
        </div>

        {/* Right Header Controls */}
        <div className="flex items-center gap-2">
          {/* Document Upload Button */}
          <button
            type="button"
            onClick={onOpenUpload}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl border border-gray-200 dark:border-neutral-700 hover:bg-gray-100 dark:hover:bg-neutral-800 text-xs font-medium text-gray-700 dark:text-gray-300 transition-colors shadow-sm"
          >
            <Paperclip className="w-3.5 h-3.5 text-purple-500" />
            <span className="hidden sm:inline">Files</span>
            {attachedDocs.length > 0 && (
              <span className="w-4 h-4 rounded-full bg-purple-600 text-white flex items-center justify-center text-[10px] font-bold">
                {attachedDocs.length}
              </span>
            )}
          </button>
        </div>
      </header>

      {/* Message Feed / Welcome Screen */}
      <div ref={scrollRef} className="flex-1 overflow-y-auto">
        {messages.length === 0 ? (
          <div className="h-full flex flex-col items-center justify-center p-4 max-w-2xl mx-auto text-center space-y-6 animate-in fade-in duration-300">
            <div className="w-14 h-14 rounded-2xl bg-emerald-600 flex items-center justify-center text-white shadow-xl shadow-emerald-600/20">
              <Sparkles className="w-7 h-7" />
            </div>

            <div className="space-y-2">
              <h1 className="text-2xl sm:text-3xl font-bold tracking-tight text-gray-900 dark:text-gray-100">
                What can I help you with today?
              </h1>
              <p className="text-xs sm:text-sm text-gray-500 dark:text-gray-400 max-w-md mx-auto">
                Ask questions, compute complex mathematics, search the live web, or upload and summarize documents.
              </p>
            </div>

            {/* Starter Prompt Cards */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-2.5 w-full pt-4">
              {starterPrompts.map((item, idx) => (
                <button
                  key={idx}
                  type="button"
                  onClick={() => onSendMessage(item.prompt, attachedDocs.map(d => d.id))}
                  className="flex flex-col text-left p-3.5 rounded-2xl border border-gray-200 dark:border-neutral-800 bg-gray-50/70 dark:bg-neutral-900/60 hover:bg-gray-100 dark:hover:bg-neutral-800/80 transition-all text-xs sm:text-sm group hover:border-gray-300 dark:hover:border-neutral-700 shadow-sm"
                >
                  <div className="flex items-center gap-2 mb-1.5 font-medium text-gray-800 dark:text-gray-200">
                    {item.icon}
                    <span>{item.title}</span>
                  </div>
                  <div className="text-gray-500 dark:text-gray-400 text-xs line-clamp-2">
                    {item.prompt}
                  </div>
                </button>
              ))}
            </div>
          </div>
        ) : (
          <div className="divide-y divide-gray-100/50 dark:divide-neutral-800/40">
            {messages.map((msg) => (
              <MessageItem
                key={msg.id}
                message={msg}
                onTriggerConfirmation={onTriggerConfirmation}
              />
            ))}

            {/* Thinking / Running Tools Indicator */}
            {loading && (
              <div className="w-full py-4 px-3 sm:px-6 bg-gray-50/70 dark:bg-[#1a1a1a]/60">
                <div className="max-w-3xl mx-auto flex gap-3 sm:gap-4 items-center">
                  <div className="shrink-0 w-8 h-8 rounded-full bg-emerald-600 flex items-center justify-center text-white">
                    <Sparkles className="w-4 h-4 animate-spin" />
                  </div>
                  <div className="flex items-center gap-2 text-xs sm:text-sm text-gray-500 dark:text-gray-400">
                    <div className="flex gap-1 items-center">
                      <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-bounce" style={{ animationDelay: '0ms' }} />
                      <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-bounce" style={{ animationDelay: '150ms' }} />
                      <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-bounce" style={{ animationDelay: '300ms' }} />
                    </div>
                    <span>Agent is reasoning and executing tools...</span>
                  </div>
                </div>
              </div>
            )}
          </div>
        )}
      </div>

      {/* Floating Bottom Input Area */}
      <footer className="shrink-0 bg-gradient-to-t from-white via-white to-transparent dark:from-[#212121] dark:via-[#212121] dark:to-transparent pt-3">
        <ChatInput
          onSend={onSendMessage}
          loading={loading}
          onOpenUpload={onOpenUpload}
          attachedDocs={attachedDocs}
          onRemoveDoc={onRemoveDoc}
        />
      </footer>
    </div>
  );
}
