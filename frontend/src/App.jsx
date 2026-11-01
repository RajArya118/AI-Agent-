import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Sidebar from './components/Sidebar';
import ChatArea from './components/ChatArea';
import FileUploadModal from './components/FileUploadModal';
import ActionConfirmModal from './components/ActionConfirmModal';
import ProjectCreatorModal from './components/ProjectCreatorModal';
import AgentWorkflowViewer from './components/AgentWorkflowViewer';
import LivePreviewPanel from './components/LivePreviewPanel';
import FileTreeViewer from './components/FileTreeViewer';
import { useTheme } from './hooks/useTheme';
import { api } from './services/api';
import { Sparkles, MessageSquare, Layers, Download, Plus, Eye, ChevronRight } from 'lucide-react';

export default function App() {
  const { theme, toggleTheme } = useTheme();

  // Mode: 'studio' (BuildPilot Multi-Agent Studio) | 'chat' (AI Personal Assistant)
  const [activeTab, setActiveTab] = useState('studio');

  // BuildPilot Projects state
  const [projects, setProjects] = useState([]);
  const [activeProject, setActiveProject] = useState(null);
  const [creatorModalOpen, setCreatorModalOpen] = useState(false);
  const [fileViewerOpen, setFileViewerOpen] = useState(false);
  const [generating, setGenerating] = useState(false);

  // Chat state
  const [conversations, setConversations] = useState([]);
  const [activeId, setActiveId] = useState(null);
  const [activeConversation, setActiveConversation] = useState(null);
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [uploadModalOpen, setUploadModalOpen] = useState(false);
  const [attachedDocs, setAttachedDocs] = useState([]);
  const [pendingAction, setPendingAction] = useState(null);
  const [actionLoading, setActionLoading] = useState(false);
  const [health, setHealth] = useState(null);

  // Initial load
  useEffect(() => {
    loadHealth();
    loadProjects();
    loadConversations();
  }, []);

  const loadHealth = async () => {
    try {
      const data = await api.checkHealth();
      setHealth(data);
    } catch (err) {
      console.warn('Backend health check error:', err);
    }
  };

  const loadProjects = async () => {
    try {
      const res = await axios.get('/api/projects');
      setProjects(res.data);
      if (res.data.length > 0 && !activeProject) {
        selectProject(res.data[0].id);
      }
    } catch (err) {
      console.error('Error fetching projects:', err);
    }
  };

  const selectProject = async (id) => {
    try {
      const res = await axios.get(`/api/projects/${id}`);
      setActiveProject(res.data);
    } catch (err) {
      console.error('Error loading project:', err);
    }
  };

  const handleGenerateProject = async (prompt, title) => {
    setGenerating(true);
    try {
      const res = await axios.post('/api/projects', { prompt, title });
      setProjects(prev => [res.data, ...prev]);
      setActiveProject(res.data);
      setCreatorModalOpen(false);
      setActiveTab('studio');
    } catch (err) {
      alert(`Generation failed: ${err?.response?.data?.detail || err.message}`);
    } finally {
      setGenerating(false);
    }
  };

  const handleExportZip = () => {
    if (!activeProject) return;
    window.location.href = `/api/projects/${activeProject.id}/export`;
  };

  // Chat operations
  const loadConversations = async () => {
    try {
      const list = await api.getConversations();
      setConversations(list);
      if (list.length > 0) {
        selectConversation(list[0].id);
      } else {
        createNewChat();
      }
    } catch (err) {
      console.error('Error fetching conversations:', err);
    }
  };

  const selectConversation = async (id) => {
    setActiveId(id);
    setSidebarOpen(false);
    try {
      const conv = await api.getConversation(id);
      setActiveConversation(conv);
      setMessages(conv.messages || []);
      const docs = await api.listDocuments(id);
      setAttachedDocs(docs);
    } catch (err) {
      console.error('Error loading conversation:', err);
    }
  };

  const createNewChat = async () => {
    try {
      const newConv = await api.createConversation('New Chat');
      setConversations(prev => [newConv, ...prev]);
      setActiveId(newConv.id);
      setActiveConversation(newConv);
      setMessages([]);
      setAttachedDocs([]);
      setSidebarOpen(false);
    } catch (err) {
      console.error('Error creating conversation:', err);
    }
  };

  const deleteConversation = async (id) => {
    try {
      await api.deleteConversation(id);
      const remaining = conversations.filter(c => c.id !== id);
      setConversations(remaining);
      if (activeId === id) {
        if (remaining.length > 0) {
          selectConversation(remaining[0].id);
        } else {
          createNewChat();
        }
      }
    } catch (err) {
      console.error('Error deleting conversation:', err);
    }
  };

  const handleSendMessage = async (text, docIds = []) => {
    if (!text.trim() || !activeId) return;

    const tempUserMsg = {
      id: `temp-${Date.now()}`,
      conversation_id: activeId,
      role: 'user',
      content: text,
      status: 'completed',
      created_at: new Date().toISOString()
    };
    setMessages(prev => [...prev, tempUserMsg]);
    setLoading(true);

    try {
      const assistantMsg = await api.sendMessage(activeId, text, docIds);
      setMessages(prev => [...prev, assistantMsg]);

      if (assistantMsg.status === 'pending_confirmation') {
        const actionResult = assistantMsg.tool_results?.find(r => r.status === 'requires_confirmation');
        if (actionResult?.result) {
          setPendingAction(actionResult.result);
        }
      }

      const updatedList = await api.getConversations();
      setConversations(updatedList);
    } catch (err) {
      console.error('Error sending message:', err);
      const errorMsg = {
        id: `err-${Date.now()}`,
        conversation_id: activeId,
        role: 'assistant',
        content: `❌ **Error**: ${err?.response?.data?.detail || err.message || 'Failed to process message.'}`,
        status: 'error',
        created_at: new Date().toISOString()
      };
      setMessages(prev => [...prev, errorMsg]);
    } finally {
      setLoading(false);
    }
  };

  const handleActionConfirm = async (approved) => {
    if (!pendingAction || !activeId) return;
    setActionLoading(true);
    try {
      await api.confirmAction(activeId, pendingAction.action_id, approved);
      setPendingAction(null);
      selectConversation(activeId);
    } catch (err) {
      console.error('Error confirming action:', err);
    } finally {
      setActionLoading(false);
    }
  };

  const handleUploadSuccess = async (file) => {
    const doc = await api.uploadDocument(file, activeId);
    setAttachedDocs(prev => [...prev, doc]);
  };

  const handleRemoveDoc = (docId) => {
    setAttachedDocs(prev => prev.filter(d => d.id !== docId));
  };

  return (
    <div className="flex h-screen w-screen overflow-hidden bg-white dark:bg-[#212121]">
      {/* Top Global Navigation Bar */}
      <div className="fixed top-0 left-0 right-0 h-14 bg-white/95 dark:bg-[#171717]/95 border-b border-gray-200 dark:border-neutral-800 z-30 flex items-center justify-between px-4 sm:px-6 backdrop-blur-md">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-xl bg-gradient-to-tr from-indigo-600 to-purple-600 flex items-center justify-center text-white font-black text-sm shadow-sm">
            BP
          </div>
          <div>
            <span className="font-extrabold text-base tracking-tight text-gray-900 dark:text-gray-100">
              BuildPilot AI
            </span>
            <span className="hidden sm:inline text-[10px] ml-2 px-2 py-0.5 rounded-full bg-indigo-500/10 text-indigo-600 dark:text-indigo-400 font-bold border border-indigo-500/20">
              v2.0 Multi-Agent
            </span>
          </div>
        </div>

        {/* View Mode Switcher */}
        <div className="flex items-center gap-1 bg-gray-100 dark:bg-neutral-800 p-1 rounded-xl">
          <button
            onClick={() => setActiveTab('studio')}
            className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-bold transition-all ${
              activeTab === 'studio'
                ? 'bg-white dark:bg-neutral-700 text-indigo-600 dark:text-white shadow-xs'
                : 'text-gray-500 hover:text-gray-900 dark:hover:text-gray-100'
            }`}
          >
            <Layers className="w-3.5 h-3.5" />
            <span>Multi-Agent Studio</span>
          </button>

          <button
            onClick={() => setActiveTab('chat')}
            className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-bold transition-all ${
              activeTab === 'chat'
                ? 'bg-white dark:bg-neutral-700 text-indigo-600 dark:text-white shadow-xs'
                : 'text-gray-500 hover:text-gray-900 dark:hover:text-gray-100'
            }`}
          >
            <MessageSquare className="w-3.5 h-3.5" />
            <span>Assistant Chat</span>
          </button>
        </div>

        {/* Top Right Actions */}
        <div className="flex items-center gap-2">
          {activeTab === 'studio' && (
            <button
              onClick={() => setCreatorModalOpen(true)}
              className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-indigo-600 hover:bg-indigo-700 text-white text-xs font-bold shadow-xs transition-colors"
            >
              <Plus className="w-3.5 h-3.5" />
              <span className="hidden sm:inline">New Project</span>
            </button>
          )}

          {/* Theme Toggle Button */}
          <button
            onClick={toggleTheme}
            className="p-2 rounded-xl text-gray-500 hover:bg-gray-100 dark:hover:bg-neutral-800 transition-colors"
            title="Toggle Dark/Light Mode"
          >
            {theme === 'dark' ? '☀️' : '🌙'}
          </button>
        </div>
      </div>

      {/* Main Container below navbar */}
      <div className="flex-1 flex pt-14 h-full w-full overflow-hidden">
        {/* VIEW 1: Multi-Agent Studio */}
        {activeTab === 'studio' ? (
          <div className="flex-1 flex flex-col lg:flex-row h-full w-full overflow-hidden">
            {/* Left Column: Projects & Orchestration Details */}
            <div className="w-full lg:w-[480px] xl:w-[540px] flex flex-col h-full bg-white dark:bg-[#1a1a1a] border-r border-gray-200 dark:border-neutral-800 overflow-y-auto p-4 sm:p-6 space-y-6 shrink-0">
              {/* Project Selector & Status */}
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-bold uppercase tracking-wider text-gray-400">
                    Active Project
                  </span>
                  <button
                    onClick={() => setCreatorModalOpen(true)}
                    className="text-xs text-indigo-600 dark:text-indigo-400 font-semibold hover:underline flex items-center gap-1"
                  >
                    <Plus className="w-3 h-3" /> Generate New
                  </button>
                </div>

                {projects.length > 0 ? (
                  <select
                    value={activeProject?.id || ''}
                    onChange={(e) => selectProject(e.target.value)}
                    className="w-full bg-gray-50 dark:bg-neutral-800 border border-gray-200 dark:border-neutral-700 rounded-xl p-2.5 text-sm font-semibold text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-indigo-500"
                  >
                    {projects.map((p) => (
                      <option key={p.id} value={p.id}>
                        {p.title} ({p.archetype})
                      </option>
                    ))}
                  </select>
                ) : (
                  <div className="p-4 rounded-2xl border border-dashed border-gray-200 dark:border-neutral-800 text-center space-y-2">
                    <p className="text-xs text-gray-500">No projects generated yet.</p>
                    <button
                      onClick={() => setCreatorModalOpen(true)}
                      className="px-3 py-1.5 rounded-lg bg-indigo-600 text-white text-xs font-bold"
                    >
                      Generate Your First Project
                    </button>
                  </div>
                )}
              </div>

              {/* Active Project Details */}
              {activeProject && (
                <>
                  <div className="bg-gray-50 dark:bg-neutral-900/60 border border-gray-100 dark:border-neutral-800 rounded-2xl p-4 space-y-2">
                    <div className="flex items-center justify-between">
                      <h3 className="font-extrabold text-base text-gray-900 dark:text-gray-100">
                        {activeProject.title}
                      </h3>
                      <span className="text-[11px] font-mono px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 font-bold">
                        {activeProject.status}
                      </span>
                    </div>
                    <p className="text-xs text-gray-600 dark:text-gray-400 leading-relaxed">
                      "{activeProject.prompt}"
                    </p>
                  </div>

                  {/* Multi-Agent Orchestrator Timeline */}
                  <AgentWorkflowViewer
                    timeline={activeProject.agent_timeline || []}
                    qaStatus={activeProject.qa_status || 'PASS'}
                    executionTime={activeProject.execution_time_ms || 0}
                  />
                </>
              )}
            </div>

            {/* Right Column: Live Interactive Preview */}
            <div className="flex-1 flex flex-col h-full overflow-hidden bg-gray-100 dark:bg-neutral-950">
              {activeProject ? (
                <LivePreviewPanel
                  projectId={activeProject.id}
                  projectTitle={activeProject.title}
                  onExportZip={handleExportZip}
                  onToggleCode={() => setFileViewerOpen(true)}
                />
              ) : (
                <div className="flex-1 flex flex-col items-center justify-center p-8 text-center space-y-4">
                  <div className="w-16 h-16 rounded-2xl bg-indigo-500/10 text-indigo-600 flex items-center justify-center">
                    <Eye className="w-8 h-8" />
                  </div>
                  <h3 className="text-lg font-bold text-gray-900 dark:text-gray-100">
                    No Live Preview Active
                  </h3>
                  <p className="text-xs text-gray-500 max-w-sm">
                    Select an existing generated project or launch the Multi-Agent Orchestrator to build one.
                  </p>
                  <button
                    onClick={() => setCreatorModalOpen(true)}
                    className="px-4 py-2 rounded-xl bg-indigo-600 text-white text-xs font-bold shadow-md"
                  >
                    Create Project with AI
                  </button>
                </div>
              )}
            </div>
          </div>
        ) : (
          /* VIEW 2: Assistant Chat (with Tools) */
          <div className="flex-1 flex h-full w-full overflow-hidden">
            <Sidebar
              conversations={conversations}
              activeId={activeId}
              onSelectConversation={selectConversation}
              onNewChat={createNewChat}
              onDeleteConversation={deleteConversation}
              theme={theme}
              toggleTheme={toggleTheme}
              isOpen={sidebarOpen}
              onToggleSidebar={() => setSidebarOpen(!sidebarOpen)}
              health={health}
            />

            <main className="flex-1 flex flex-col h-full overflow-hidden">
              <ChatArea
                conversation={activeConversation}
                messages={messages}
                loading={loading}
                onSendMessage={handleSendMessage}
                onToggleSidebar={() => setSidebarOpen(!sidebarOpen)}
                onOpenUpload={() => setUploadModalOpen(true)}
                attachedDocs={attachedDocs}
                onRemoveDoc={handleRemoveDoc}
                onTriggerConfirmation={(msg) => {
                  const actionResult = msg.tool_results?.find(r => r.status === 'requires_confirmation');
                  if (actionResult?.result) {
                    setPendingAction(actionResult.result);
                  }
                }}
                health={health}
              />
            </main>
          </div>
        )}
      </div>

      {/* Project Creator Modal */}
      <ProjectCreatorModal
        isOpen={creatorModalOpen}
        onClose={() => setCreatorModalOpen(false)}
        onGenerate={handleGenerateProject}
        loading={generating}
      />

      {/* File Tree & Code Viewer Modal */}
      <FileTreeViewer
        isOpen={fileViewerOpen}
        onClose={() => setFileViewerOpen(false)}
        projectId={activeProject?.id}
        fileTree={activeProject?.file_tree || []}
      />

      {/* Document Upload Modal */}
      <FileUploadModal
        isOpen={uploadModalOpen}
        onClose={() => setUploadModalOpen(false)}
        onUploadSuccess={handleUploadSuccess}
        attachedDocs={attachedDocs}
        onDeleteDoc={async (docId) => {
          await api.deleteDocument(docId);
          handleRemoveDoc(docId);
        }}
      />

      {/* Consequential Action Confirmation Modal */}
      <ActionConfirmModal
        action={pendingAction}
        onConfirm={() => handleActionConfirm(true)}
        onCancel={() => handleActionConfirm(false)}
        loading={actionLoading}
      />
    </div>
  );
}
