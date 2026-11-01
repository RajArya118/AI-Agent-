import React from 'react';
import { 
  Plus, 
  MessageSquare, 
  Trash2, 
  Sparkles, 
  ChevronLeft, 
  ChevronRight,
  ShieldCheck,
  Cpu
} from 'lucide-react';
import ThemeToggle from './ThemeToggle';

export default function Sidebar({
  conversations,
  activeId,
  onSelectConversation,
  onNewChat,
  onDeleteConversation,
  theme,
  toggleTheme,
  isOpen,
  onToggleSidebar,
  health
}) {
  return (
    <>
      {/* Mobile Backdrop Overlay */}
      {isOpen && (
        <div
          className="fixed inset-0 z-40 bg-black/50 lg:hidden"
          onClick={onToggleSidebar}
        />
      )}

      {/* Sidebar Drawer */}
      <aside
        className={`fixed lg:static top-0 bottom-0 left-0 z-40 flex flex-col w-72 bg-[#f9f9f9] dark:bg-[#171717] border-r border-gray-200 dark:border-neutral-800 transition-transform duration-300 ease-in-out ${
          isOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'
        }`}
      >
        {/* Top Header & New Chat Button */}
        <div className="p-3 border-b border-gray-200 dark:border-neutral-800/80 space-y-2">
          <div className="flex items-center justify-between px-2 py-1">
            <div className="flex items-center gap-2">
              <div className="w-7 h-7 rounded-lg bg-emerald-600 flex items-center justify-center text-white font-bold text-xs shadow-sm">
                AI
              </div>
              <span className="font-semibold text-sm tracking-tight text-gray-800 dark:text-gray-100">
                Personal Assistant
              </span>
            </div>

            <button
              onClick={onToggleSidebar}
              className="lg:hidden p-1.5 rounded-lg text-gray-500 hover:bg-gray-200 dark:hover:bg-neutral-800"
            >
              <ChevronLeft className="w-5 h-5" />
            </button>
          </div>

          <button
            onClick={onNewChat}
            className="w-full flex items-center justify-between px-3.5 py-2.5 rounded-xl border border-gray-200 dark:border-neutral-700 bg-white dark:bg-neutral-800 hover:bg-gray-100 dark:hover:bg-neutral-700/80 text-gray-800 dark:text-gray-100 text-sm font-medium transition-all shadow-sm"
          >
            <div className="flex items-center gap-2">
              <Plus className="w-4 h-4 text-emerald-600 dark:text-emerald-400" />
              <span>New Chat</span>
            </div>
            <span className="text-[10px] text-gray-400 font-mono">⌘N</span>
          </button>
        </div>

        {/* Conversation History List */}
        <div className="flex-1 overflow-y-auto px-2 py-2 space-y-1">
          <div className="px-2 py-1 text-[11px] font-semibold text-gray-400 dark:text-gray-500 uppercase tracking-wider">
            Recent Conversations
          </div>

          {conversations.length === 0 ? (
            <div className="text-center py-8 text-xs text-gray-400 dark:text-gray-600 px-4">
              No conversations yet. Start a new chat to begin!
            </div>
          ) : (
            conversations.map((conv) => {
              const isActive = conv.id === activeId;
              return (
                <div
                  key={conv.id}
                  onClick={() => onSelectConversation(conv.id)}
                  className={`group relative flex items-center justify-between px-3 py-2 rounded-xl text-xs sm:text-sm cursor-pointer transition-all ${
                    isActive
                      ? 'bg-gray-200/90 dark:bg-neutral-800 text-gray-900 dark:text-gray-100 font-medium'
                      : 'text-gray-600 dark:text-gray-400 hover:bg-gray-200/50 dark:hover:bg-neutral-800/50 hover:text-gray-900 dark:hover:text-gray-200'
                  }`}
                >
                  <div className="flex items-center gap-2.5 truncate pr-2">
                    <MessageSquare className={`w-4 h-4 shrink-0 ${isActive ? 'text-emerald-500' : 'text-gray-400'}`} />
                    <span className="truncate">{conv.title || 'New Chat'}</span>
                  </div>

                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      onDeleteConversation(conv.id);
                    }}
                    className="opacity-0 group-hover:opacity-100 p-1 rounded hover:text-red-500 transition-all text-gray-400 shrink-0"
                    title="Delete conversation"
                  >
                    <Trash2 className="w-3.5 h-3.5" />
                  </button>
                </div>
              );
            })
          )}
        </div>

        {/* Bottom Panel */}
        <div className="p-3 border-t border-gray-200 dark:border-neutral-800/80 space-y-2 bg-[#f4f4f4] dark:bg-[#141414]">
          {/* Health & Engine status pill */}
          <div className="px-2.5 py-1.5 rounded-lg bg-white dark:bg-neutral-900 border border-gray-200 dark:border-neutral-800 flex items-center justify-between text-[11px]">
            <div className="flex items-center gap-1.5">
              <span className={`w-2 h-2 rounded-full ${health?.gemini_configured ? 'bg-emerald-500 animate-pulse' : 'bg-amber-500'}`} />
              <span className="text-gray-600 dark:text-gray-300 font-medium">
                {health?.gemini_configured ? health.gemini_model : 'Local Agent Tools'}
              </span>
            </div>
            <span className="text-[10px] text-gray-400">
              {health?.gemini_configured ? 'AI Studio' : 'Active'}
            </span>
          </div>

          {/* Theme switcher */}
          <ThemeToggle theme={theme} toggleTheme={toggleTheme} />
        </div>
      </aside>
    </>
  );
}
