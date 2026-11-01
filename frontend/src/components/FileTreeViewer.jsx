import React, { useState, useEffect } from 'react';
import { FileCode, FileText, X, Copy, Check } from 'lucide-react';
import { api } from '../services/api';

export default function FileTreeViewer({ isOpen, onClose, projectId, fileTree = [] }) {
  const [selectedFile, setSelectedFile] = useState(null);
  const [content, setContent] = useState('');
  const [loading, setLoading] = useState(false);
  const [copied, setCopied] = useState(false);

  useEffect(() => {
    if (fileTree.length > 0 && !selectedFile) {
      loadFile(fileTree[0].path);
    }
  }, [fileTree]);

  const loadFile = async (filePath) => {
    setSelectedFile(filePath);
    setLoading(true);
    try {
      const data = await api.getProjectFile(projectId, filePath);
      setContent(data.content);
    } catch (err) {
      setContent(`// Failed loading file: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  const handleCopy = () => {
    navigator.clipboard.writeText(content);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm animate-in fade-in duration-200">
      <div className="bg-white dark:bg-neutral-900 border border-gray-200 dark:border-neutral-800 rounded-3xl max-w-4xl w-full h-[80vh] shadow-2xl flex flex-col overflow-hidden text-gray-900 dark:text-gray-100">
        {/* Header */}
        <div className="h-14 border-b border-gray-200 dark:border-neutral-800 px-6 flex items-center justify-between shrink-0">
          <div className="flex items-center gap-2">
            <FileCode className="w-5 h-5 text-indigo-500" />
            <h3 className="font-bold text-sm">Generated Project Workspace Files</h3>
            <span className="text-xs text-gray-400">({fileTree.length} files)</span>
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={handleCopy}
              className="px-3 py-1.5 rounded-lg border border-gray-200 dark:border-neutral-700 hover:bg-gray-100 dark:hover:bg-neutral-800 text-xs font-medium text-gray-700 dark:text-gray-300 transition-colors flex items-center gap-1.5"
            >
              {copied ? <Check className="w-3.5 h-3.5 text-emerald-500" /> : <Copy className="w-3.5 h-3.5" />}
              <span>{copied ? 'Copied' : 'Copy Code'}</span>
            </button>
            <button
              onClick={onClose}
              className="p-1.5 rounded-xl text-gray-400 hover:text-gray-600 dark:hover:text-gray-200 hover:bg-gray-100 dark:hover:bg-neutral-800 transition-colors"
            >
              <X className="w-5 h-5" />
            </button>
          </div>
        </div>

        {/* Content split */}
        <div className="flex-1 flex overflow-hidden">
          {/* File sidebar */}
          <div className="w-64 border-r border-gray-200 dark:border-neutral-800 bg-gray-50 dark:bg-neutral-950/60 p-3 overflow-y-auto space-y-1">
            <div className="text-[11px] font-bold text-gray-400 uppercase tracking-wider px-2 py-1">Project Tree</div>
            {fileTree.map((f) => (
              <button
                key={f.path}
                type="button"
                onClick={() => loadFile(f.path)}
                className={`w-full flex items-center justify-between px-2.5 py-1.5 rounded-lg text-xs transition-colors text-left ${
                  selectedFile === f.path
                    ? 'bg-indigo-600 text-white font-semibold'
                    : 'text-gray-600 dark:text-gray-400 hover:bg-gray-200/60 dark:hover:bg-neutral-800'
                }`}
              >
                <div className="flex items-center gap-2 truncate">
                  <FileText className="w-3.5 h-3.5 shrink-0" />
                  <span className="truncate">{f.path}</span>
                </div>
                <span className="text-[10px] opacity-60">{(f.size / 1024).toFixed(1)}k</span>
              </button>
            ))}
          </div>

          {/* Editor view */}
          <div className="flex-1 bg-gray-900 text-gray-100 p-4 overflow-auto font-mono text-xs">
            {loading ? (
              <div className="flex items-center justify-center h-full text-gray-400">Loading file...</div>
            ) : (
              <pre className="whitespace-pre-wrap">{content}</pre>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
