import React, { useState, useRef } from 'react';
import { UploadCloud, File, FileText, CheckCircle2, X, AlertCircle, Trash2 } from 'lucide-react';

export default function FileUploadModal({ isOpen, onClose, onUploadSuccess, attachedDocs = [], onDeleteDoc }) {
  const [dragActive, setDragActive] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState(null);
  const fileInputRef = useRef(null);

  if (!isOpen) return null;

  const handleFiles = async (files) => {
    if (!files || files.length === 0) return;
    setError(null);
    setUploading(true);

    const file = files[0];
    const allowed = ['.pdf', '.txt', '.md', '.csv'];
    const ext = '.' + file.name.split('.').pop().toLowerCase();

    if (!allowed.includes(ext)) {
      setError(`Unsupported file type: ${ext}. Please upload .pdf, .txt, or .md files.`);
      setUploading(false);
      return;
    }

    if (file.size > 10 * 1024 * 1024) {
      setError('File exceeds the 10MB upload limit.');
      setUploading(false);
      return;
    }

    try {
      await onUploadSuccess(file);
      setUploading(false);
      onClose();
    } catch (err) {
      setError(err?.response?.data?.detail || 'Failed to upload document.');
      setUploading(false);
    }
  };

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFiles(e.dataTransfer.files);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm animate-in fade-in duration-200">
      <div className="bg-white dark:bg-neutral-900 border border-gray-200 dark:border-neutral-800 rounded-2xl max-w-lg w-full shadow-2xl p-6 text-gray-900 dark:text-gray-100 space-y-4">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2.5">
            <div className="p-2.5 rounded-xl bg-purple-500/10 text-purple-500">
              <UploadCloud className="w-5 h-5" />
            </div>
            <div>
              <h3 className="text-base font-semibold">Upload Document</h3>
              <p className="text-xs text-gray-500 dark:text-gray-400">Attach PDF or TXT files for the agent to analyze</p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 rounded-lg text-gray-400 hover:text-gray-600 dark:hover:text-gray-200 hover:bg-gray-100 dark:hover:bg-neutral-800 transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Dropzone */}
        <div
          onDragEnter={handleDrag}
          onDragLeave={handleDrag}
          onDragOver={handleDrag}
          onDrop={handleDrop}
          onClick={() => fileInputRef.current?.click()}
          className={`border-2 border-dashed rounded-xl p-6 sm:p-8 text-center cursor-pointer transition-all ${
            dragActive
              ? 'border-purple-500 bg-purple-500/5'
              : 'border-gray-200 dark:border-neutral-700 hover:border-purple-400 dark:hover:border-purple-500 hover:bg-gray-50 dark:hover:bg-neutral-800/50'
          }`}
        >
          <input
            ref={fileInputRef}
            type="file"
            accept=".pdf,.txt,.md,.csv"
            className="hidden"
            onChange={(e) => handleFiles(e.target.files)}
          />

          <div className="flex flex-col items-center gap-2">
            <UploadCloud className="w-10 h-10 text-purple-500 animate-bounce" />
            <div className="text-sm font-medium">
              Click to browse or drag & drop files here
            </div>
            <div className="text-xs text-gray-400">
              Supports PDF, TXT, MD (Max 10MB)
            </div>
          </div>
        </div>

        {/* Status / Error */}
        {uploading && (
          <div className="flex items-center gap-2 text-sm text-purple-600 dark:text-purple-400 animate-pulse">
            <div className="w-4 h-4 border-2 border-purple-600 border-t-transparent rounded-full animate-spin" />
            Extracting text and indexing document...
          </div>
        )}

        {error && (
          <div className="p-3 rounded-xl bg-red-50 dark:bg-red-950/30 border border-red-200 dark:border-red-800/40 text-xs text-red-700 dark:text-red-400 flex items-center gap-2">
            <AlertCircle className="w-4 h-4 shrink-0" />
            {error}
          </div>
        )}

        {/* Attached Documents List */}
        {attachedDocs.length > 0 && (
          <div className="space-y-2 pt-2 border-t border-gray-100 dark:border-neutral-800">
            <div className="text-xs font-semibold text-gray-500 uppercase tracking-wider">
              Attached Documents ({attachedDocs.length})
            </div>
            <div className="max-h-36 overflow-y-auto space-y-1.5">
              {attachedDocs.map((doc) => (
                <div
                  key={doc.id}
                  className="flex items-center justify-between p-2.5 rounded-lg bg-gray-50 dark:bg-neutral-800/50 text-xs text-gray-700 dark:text-gray-300 border border-gray-100 dark:border-neutral-800"
                >
                  <div className="flex items-center gap-2 truncate pr-2">
                    <FileText className="w-4 h-4 text-purple-500 shrink-0" />
                    <span className="font-medium truncate">{doc.filename}</span>
                    <span className="text-[10px] text-gray-400">
                      ({(doc.file_size / 1024).toFixed(1)} KB)
                    </span>
                  </div>
                  {onDeleteDoc && (
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        onDeleteDoc(doc.id);
                      }}
                      className="text-gray-400 hover:text-red-500 transition-colors p-1"
                      title="Remove document"
                    >
                      <Trash2 className="w-3.5 h-3.5" />
                    </button>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}

        <div className="flex justify-end pt-2">
          <button
            type="button"
            onClick={onClose}
            className="px-4 py-2 rounded-xl text-xs sm:text-sm font-medium border border-gray-200 dark:border-neutral-700 hover:bg-gray-100 dark:hover:bg-neutral-800 transition-colors"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
}
