import React, { useState, useRef, useEffect } from 'react';
import { ArrowUp, Paperclip, FileText, X } from 'lucide-react';

export default function ChatInput({ onSend, loading, onOpenUpload, attachedDocs = [], onRemoveDoc }) {
  const [text, setText] = useState('');
  const textareaRef = useRef(null);

  // Auto-resize textarea
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 180)}px`;
    }
  }, [text]);

  const handleSubmit = (e) => {
    e?.preventDefault();
    if (!text.trim() || loading) return;
    onSend(text.trim(), attachedDocs.map(d => d.id));
    setText('');
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  const canSend = text.trim().length > 0 && !loading;

  return (
    <div className="w-full max-w-3xl mx-auto px-3 sm:px-4 pb-4">
      {/* Attached Files Badges */}
      {attachedDocs.length > 0 && (
        <div className="flex flex-wrap gap-2 mb-2 px-1">
          {attachedDocs.map((doc) => (
            <div
              key={doc.id}
              className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-lg text-xs font-medium bg-purple-50 dark:bg-purple-950/40 text-purple-700 dark:text-purple-300 border border-purple-200 dark:border-purple-800/40 shadow-sm"
            >
              <FileText className="w-3.5 h-3.5" />
              <span className="truncate max-w-[140px]">{doc.filename}</span>
              <button
                type="button"
                onClick={() => onRemoveDoc(doc.id)}
                className="hover:text-purple-900 dark:hover:text-purple-100 p-0.5 rounded"
                title="Remove attachment"
              >
                <X className="w-3 h-3" />
              </button>
            </div>
          ))}
        </div>
      )}

      {/* Input Container Box */}
      <div className="relative flex items-end w-full rounded-2xl border border-gray-200 dark:border-neutral-700 bg-white dark:bg-[#2f2f2f] shadow-lg focus-within:border-gray-400 dark:focus-within:border-neutral-500 transition-colors p-2 sm:p-2.5">
        {/* Attach File Button */}
        <button
          type="button"
          onClick={onOpenUpload}
          className="p-2 rounded-xl text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200 hover:bg-gray-100 dark:hover:bg-neutral-800 transition-colors"
          title="Attach PDF or TXT Document"
        >
          <Paperclip className="w-5 h-5" />
        </button>

        {/* Text Input Area */}
        <textarea
          ref={textareaRef}
          value={text}
          onChange={(e) => setText(e.target.value)}
          onKeyDown={handleKeyDown}
          disabled={loading}
          rows={1}
          placeholder="Ask anything, calculate math, search the web, or read files..."
          className="flex-1 max-h-44 bg-transparent border-0 resize-none px-3 py-1.5 text-sm sm:text-base text-gray-900 dark:text-gray-100 placeholder-gray-400 focus:outline-none focus:ring-0 leading-relaxed"
        />

        {/* Send Button */}
        <button
          type="button"
          onClick={handleSubmit}
          disabled={!canSend}
          className={`p-2 rounded-xl transition-all ${
            canSend
              ? 'bg-black text-white dark:bg-white dark:text-black hover:opacity-90 shadow-sm'
              : 'bg-gray-100 text-gray-300 dark:bg-neutral-800 dark:text-neutral-600 cursor-not-allowed'
          }`}
          title="Send message"
        >
          {loading ? (
            <div className="w-4 h-4 border-2 border-current border-t-transparent rounded-full animate-spin" />
          ) : (
            <ArrowUp className="w-4 h-4 stroke-[2.5]" />
          )}
        </button>
      </div>

      <div className="text-[11px] text-center text-gray-400 dark:text-gray-500 mt-2">
        AI Assistant can use tools (Calculator, Web Search, Document Reader). Verify critical info.
      </div>
    </div>
  );
}
