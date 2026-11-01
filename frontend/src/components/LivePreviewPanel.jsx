import React, { useState } from 'react';
import { 
  Smartphone, 
  Tablet, 
  Laptop, 
  Monitor, 
  RotateCw, 
  ExternalLink, 
  Download,
  Code2
} from 'lucide-react';
import { api } from '../services/api';

export default function LivePreviewPanel({ projectId, projectTitle, onExportZip, onToggleCode }) {
  const [viewport, setViewport] = useState('100%');
  const [key, setKey] = useState(0);

  const previewUrl = api.getPreviewUrl(projectId);

  const reloadIframe = () => {
    setKey(prev => prev + 1);
  };

  return (
    <div className="flex-1 flex flex-col h-full bg-gray-100 dark:bg-neutral-950 overflow-hidden border-l border-gray-200 dark:border-neutral-800">
      {/* Top Preview Controls Bar */}
      <div className="h-14 bg-white dark:bg-neutral-900 border-b border-gray-200 dark:border-neutral-800 px-4 flex items-center justify-between gap-2 shrink-0">
        {/* Viewport switchers */}
        <div className="flex items-center gap-1 bg-gray-100 dark:bg-neutral-800 p-1 rounded-xl">
          <button
            onClick={() => setViewport('360px')}
            className={`p-1.5 rounded-lg text-xs font-medium transition-all flex items-center gap-1 ${
              viewport === '360px' ? 'bg-white dark:bg-neutral-700 text-indigo-600 dark:text-white shadow-xs' : 'text-gray-500 hover:text-gray-800 dark:hover:text-gray-200'
            }`}
            title="Mobile (360px)"
          >
            <Smartphone className="w-3.5 h-3.5" />
            <span className="hidden sm:inline">360px</span>
          </button>

          <button
            onClick={() => setViewport('390px')}
            className={`p-1.5 rounded-lg text-xs font-medium transition-all flex items-center gap-1 ${
              viewport === '390px' ? 'bg-white dark:bg-neutral-700 text-indigo-600 dark:text-white shadow-xs' : 'text-gray-500 hover:text-gray-800 dark:hover:text-gray-200'
            }`}
            title="Mobile (390px)"
          >
            <Smartphone className="w-3.5 h-3.5" />
            <span className="hidden sm:inline">390px</span>
          </button>

          <button
            onClick={() => setViewport('768px')}
            className={`p-1.5 rounded-lg text-xs font-medium transition-all flex items-center gap-1 ${
              viewport === '768px' ? 'bg-white dark:bg-neutral-700 text-indigo-600 dark:text-white shadow-xs' : 'text-gray-500 hover:text-gray-800 dark:hover:text-gray-200'
            }`}
            title="Tablet (768px)"
          >
            <Tablet className="w-3.5 h-3.5" />
            <span className="hidden sm:inline">768px</span>
          </button>

          <button
            onClick={() => setViewport('1024px')}
            className={`p-1.5 rounded-lg text-xs font-medium transition-all flex items-center gap-1 ${
              viewport === '1024px' ? 'bg-white dark:bg-neutral-700 text-indigo-600 dark:text-white shadow-xs' : 'text-gray-500 hover:text-gray-800 dark:hover:text-gray-200'
            }`}
            title="Laptop (1024px)"
          >
            <Laptop className="w-3.5 h-3.5" />
            <span className="hidden sm:inline">1024px</span>
          </button>

          <button
            onClick={() => setViewport('100%')}
            className={`p-1.5 rounded-lg text-xs font-medium transition-all flex items-center gap-1 ${
              viewport === '100%' ? 'bg-white dark:bg-neutral-700 text-indigo-600 dark:text-white shadow-xs' : 'text-gray-500 hover:text-gray-800 dark:hover:text-gray-200'
            }`}
            title="Desktop Responsive"
          >
            <Monitor className="w-3.5 h-3.5" />
            <span className="hidden sm:inline">Full</span>
          </button>
        </div>

        {/* Action buttons */}
        <div className="flex items-center gap-2">
          <button
            onClick={reloadIframe}
            className="p-1.5 rounded-lg text-gray-500 hover:text-gray-800 dark:text-gray-400 dark:hover:text-gray-200 hover:bg-gray-100 dark:hover:bg-neutral-800 transition-colors"
            title="Refresh Live Preview"
          >
            <RotateCw className="w-4 h-4" />
          </button>

          {onToggleCode && (
            <button
              onClick={onToggleCode}
              className="px-2.5 py-1.5 rounded-lg border border-gray-200 dark:border-neutral-700 hover:bg-gray-100 dark:hover:bg-neutral-800 text-xs font-medium text-gray-700 dark:text-gray-300 transition-colors flex items-center gap-1"
            >
              <Code2 className="w-3.5 h-3.5 text-indigo-500" />
              <span>Files</span>
            </button>
          )}

          <a
            href={previewUrl}
            target="_blank"
            rel="noopener noreferrer"
            className="p-1.5 rounded-lg text-gray-500 hover:text-gray-800 dark:text-gray-400 dark:hover:text-gray-200 hover:bg-gray-100 dark:hover:bg-neutral-800 transition-colors"
            title="Open in New Tab"
          >
            <ExternalLink className="w-4 h-4" />
          </a>

          <button
            onClick={onExportZip}
            className="flex items-center gap-1 px-3 py-1.5 rounded-lg bg-indigo-600 hover:bg-indigo-700 text-white text-xs font-bold transition-all shadow-xs"
            title="Download ZIP"
          >
            <Download className="w-3.5 h-3.5" />
            <span className="hidden sm:inline">Export ZIP</span>
          </button>
        </div>
      </div>

      {/* Frame Container */}
      <div className="flex-1 overflow-auto flex justify-center items-center p-2 sm:p-4 bg-gray-200/50 dark:bg-black/40">
        <div
          style={{ width: viewport }}
          className="h-full bg-white rounded-2xl shadow-xl overflow-hidden transition-all duration-300 border border-gray-300 dark:border-neutral-800 flex flex-col"
        >
          <iframe
            key={key}
            src={previewUrl}
            title={projectTitle || 'BuildPilot Live Preview'}
            className="w-full h-full border-0"
            sandbox="allow-scripts allow-forms allow-modals allow-same-origin"
          />
        </div>
      </div>
    </div>
  );
}
