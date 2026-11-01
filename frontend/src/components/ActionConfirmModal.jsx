import React from 'react';
import { ShieldAlert, AlertTriangle, Check, X } from 'lucide-react';

export default function ActionConfirmModal({ action, onConfirm, onCancel, loading }) {
  if (!action) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm animate-in fade-in duration-200">
      <div className="bg-white dark:bg-neutral-900 border border-gray-200 dark:border-neutral-800 rounded-2xl max-w-md w-full shadow-2xl p-6 text-gray-900 dark:text-gray-100 space-y-4">
        {/* Header */}
        <div className="flex items-center gap-3">
          <div className="p-3 rounded-full bg-amber-500/10 text-amber-500">
            <ShieldAlert className="w-6 h-6" />
          </div>
          <div>
            <h3 className="text-lg font-semibold leading-tight">Confirmation Required</h3>
            <p className="text-xs text-gray-500 dark:text-gray-400">Security checkpoint for consequential action</p>
          </div>
        </div>

        {/* Warning Callout */}
        <div className="p-3.5 rounded-xl bg-amber-50 dark:bg-amber-950/30 border border-amber-200 dark:border-amber-800/40 text-xs text-amber-800 dark:text-amber-300 flex gap-2.5 items-start">
          <AlertTriangle className="w-4 h-4 shrink-0 mt-0.5" />
          <div>
            <span className="font-semibold block mb-0.5">Sensitive Action Warning</span>
            The assistant has requested permission to perform a consequential action. Review the description below before proceeding.
          </div>
        </div>

        {/* Action Details */}
        <div className="p-3.5 rounded-xl bg-gray-50 dark:bg-neutral-800/60 border border-gray-100 dark:border-neutral-800 space-y-1.5 text-xs sm:text-sm">
          <div className="text-gray-500 dark:text-gray-400 text-xs uppercase font-bold tracking-wider">Proposed Operation</div>
          <div className="font-medium text-gray-800 dark:text-gray-200">{action.description}</div>
          <div className="text-xs text-gray-400 font-mono">Type: {action.action_type || 'system_action'}</div>
        </div>

        {/* Action Buttons */}
        <div className="flex items-center gap-3 pt-2">
          <button
            type="button"
            disabled={loading}
            onClick={onCancel}
            className="flex-1 flex items-center justify-center gap-1.5 px-4 py-2.5 rounded-xl border border-gray-300 dark:border-neutral-700 hover:bg-gray-100 dark:hover:bg-neutral-800 text-gray-700 dark:text-gray-300 text-sm font-medium transition-colors disabled:opacity-50"
          >
            <X className="w-4 h-4" /> Reject
          </button>

          <button
            type="button"
            disabled={loading}
            onClick={onConfirm}
            className="flex-1 flex items-center justify-center gap-1.5 px-4 py-2.5 rounded-xl bg-amber-600 hover:bg-amber-700 text-white text-sm font-medium shadow-sm transition-colors disabled:opacity-50"
          >
            <Check className="w-4 h-4" /> Approve & Execute
          </button>
        </div>
      </div>
    </div>
  );
}
