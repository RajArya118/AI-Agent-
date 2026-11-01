import React, { useState } from 'react';
import { Sparkles, Hotel, ShoppingBag, Briefcase, CheckSquare, X, ArrowRight } from 'lucide-react';

export default function ProjectCreatorModal({ isOpen, onClose, onGenerate, loading }) {
  const [prompt, setPrompt] = useState('');
  const [title, setTitle] = useState('');

  if (!isOpen) return null;

  const presets = [
    {
      title: 'Hotel Booking Website',
      prompt: 'Build a luxury hotel booking website with interactive room selection, date picker, booking modal, and guest reviews.',
      icon: <Hotel className="w-5 h-5 text-teal-500" />,
      color: 'hover:border-teal-400 dark:hover:border-teal-500'
    },
    {
      title: 'E-Commerce with Admin',
      prompt: 'Build an e-commerce website with product catalog, search filtering, shopping cart drawer, and interactive admin analytics dashboard.',
      icon: <ShoppingBag className="w-5 h-5 text-indigo-500" />,
      color: 'hover:border-indigo-400 dark:hover:border-indigo-500'
    },
    {
      title: 'Developer Portfolio',
      prompt: 'Build a modern developer portfolio website with project showcase, skills breakdown, and interactive contact form.',
      icon: <Briefcase className="w-5 h-5 text-blue-500" />,
      color: 'hover:border-blue-400 dark:hover:border-blue-500'
    },
    {
      title: 'Task Management Kanban',
      prompt: 'Build a task management application featuring interactive Kanban columns (To Do, In Progress, Done) and task creation modal.',
      icon: <CheckSquare className="w-5 h-5 text-sky-500" />,
      color: 'hover:border-sky-400 dark:hover:border-sky-500'
    }
  ];

  const handleSelectPreset = (p) => {
    setTitle(p.title);
    setPrompt(p.prompt);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!prompt.trim() || loading) return;
    onGenerate(prompt.trim(), title.trim() || undefined);
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm animate-in fade-in duration-200">
      <div className="bg-white dark:bg-neutral-900 border border-gray-200 dark:border-neutral-800 rounded-3xl max-w-2xl w-full shadow-2xl p-6 text-gray-900 dark:text-gray-100 space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="p-2.5 rounded-2xl bg-indigo-500/10 text-indigo-600 dark:text-indigo-400">
              <Sparkles className="w-6 h-6" />
            </div>
            <div>
              <h3 className="text-xl font-bold">Generate Application with Multi-Agent AI</h3>
              <p className="text-xs text-gray-500 dark:text-gray-400">
                Orchestrates Planner, UI/UX, Database, Backend, Frontend & QA Agents
              </p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 rounded-xl text-gray-400 hover:text-gray-600 dark:hover:text-gray-200 hover:bg-gray-100 dark:hover:bg-neutral-800 transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Preset Cards */}
        <div className="space-y-2">
          <label className="text-xs font-semibold uppercase tracking-wider text-gray-400">
            Quick Architecture Presets
          </label>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
            {presets.map((preset, idx) => (
              <button
                key={idx}
                type="button"
                onClick={() => handleSelectPreset(preset)}
                className={`p-3 rounded-2xl border border-gray-200 dark:border-neutral-800 bg-gray-50/70 dark:bg-neutral-800/40 text-left transition-all ${preset.color} hover:shadow-sm flex items-start gap-3`}
              >
                <div className="p-2 rounded-xl bg-white dark:bg-neutral-800 shadow-xs shrink-0">
                  {preset.icon}
                </div>
                <div className="min-w-0 flex-1">
                  <div className="font-semibold text-xs text-gray-800 dark:text-gray-200">{preset.title}</div>
                  <div className="text-[11px] text-gray-500 dark:text-gray-400 line-clamp-1 mt-0.5">{preset.prompt}</div>
                </div>
              </button>
            ))}
          </div>
        </div>

        {/* Custom Input Form */}
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-xs font-semibold text-gray-700 dark:text-gray-300 mb-1">
              Project Title
            </label>
            <input
              type="text"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder="e.g. Grand Horizon Luxury Resort"
              className="w-full bg-gray-50 dark:bg-neutral-800/80 border border-gray-200 dark:border-neutral-700 rounded-xl p-2.5 text-sm focus:ring-2 focus:ring-indigo-500 focus:outline-none"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-gray-700 dark:text-gray-300 mb-1">
              Specification & Prompt
            </label>
            <textarea
              rows={3}
              required
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              placeholder="Describe your desired features, user flows, database models, and design aesthetics..."
              className="w-full bg-gray-50 dark:bg-neutral-800/80 border border-gray-200 dark:border-neutral-700 rounded-xl p-2.5 text-sm focus:ring-2 focus:ring-indigo-500 focus:outline-none"
            />
          </div>

          <div className="flex justify-end gap-3 pt-2">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2.5 rounded-xl text-xs sm:text-sm font-medium border border-gray-200 dark:border-neutral-700 hover:bg-gray-100 dark:hover:bg-neutral-800 transition-colors"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={!prompt.trim() || loading}
              className="flex items-center gap-2 px-5 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-700 text-white text-xs sm:text-sm font-bold shadow-md transition-all disabled:opacity-50"
            >
              {loading ? (
                <>
                  <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
                  <span>Multi-Agent Mesh Running...</span>
                </>
              ) : (
                <>
                  <span>Launch Agent Orchestrator</span>
                  <ArrowRight className="w-4 h-4" />
                </>
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
