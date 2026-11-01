import axios from 'axios';

// When running Vite dev server or serving from FastAPI, proxy or relative path handles /api
// When deployed on Vercel with Render backend, VITE_API_BASE_URL points to https://<render-service>.onrender.com/api
const rawBase = (import.meta.env.VITE_API_BASE_URL || '').trim();

let normalizedBase = '/api';
if (rawBase) {
  // Strip trailing slashes
  const clean = rawBase.replace(/\/+$/, '');
  // If user passed root domain e.g. https://api.render.com, ensure /api is present
  normalizedBase = clean.endsWith('/api') ? clean : `${clean}/api`;
}

export const API_BASE_URL = normalizedBase;

export const client = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000,
});

export const api = {
  // Base URLs
  getBaseUrl: () => API_BASE_URL,

  getPreviewUrl: (projectId) => {
    if (API_BASE_URL.startsWith('http://') || API_BASE_URL.startsWith('https://')) {
      return `${API_BASE_URL}/projects/${projectId}/preview`;
    }
    return `/api/projects/${projectId}/preview`;
  },

  getExportUrl: (projectId) => {
    if (API_BASE_URL.startsWith('http://') || API_BASE_URL.startsWith('https://')) {
      return `${API_BASE_URL}/projects/${projectId}/export`;
    }
    return `/api/projects/${projectId}/export`;
  },

  // Health
  checkHealth: async () => {
    const res = await client.get('/health');
    return res.data;
  },

  // BuildPilot Projects (Multi-Agent Platform)
  getProjects: async () => {
    const res = await client.get('/projects');
    return res.data;
  },

  getProject: async (id) => {
    const res = await client.get(`/projects/${id}`);
    return res.data;
  },

  createProject: async (prompt, title) => {
    const res = await client.post('/projects', { prompt, title });
    return res.data;
  },

  getProjectFile: async (projectId, filePath) => {
    const res = await client.get(`/projects/${projectId}/files/${filePath}`);
    return res.data;
  },

  // Conversations (AI Assistant)
  getConversations: async () => {
    const res = await client.get('/conversations');
    return res.data;
  },

  createConversation: async (title = 'New Chat') => {
    const res = await client.post('/conversations', { title });
    return res.data;
  },

  getConversation: async (id) => {
    const res = await client.get(`/conversations/${id}`);
    return res.data;
  },

  deleteConversation: async (id) => {
    const res = await client.delete(`/conversations/${id}`);
    return res.data;
  },

  // Messages & Agent execution
  sendMessage: async (conversationId, content, documentIds = []) => {
    const res = await client.post(`/conversations/${conversationId}/messages`, {
      content,
      document_ids: documentIds,
    });
    return res.data;
  },

  confirmAction: async (conversationId, actionId, approved) => {
    const res = await client.post(`/conversations/${conversationId}/action-confirmation`, {
      action_id: actionId,
      approved,
    });
    return res.data;
  },

  // Documents
  uploadDocument: async (file, conversationId = null) => {
    const formData = new FormData();
    formData.append('file', file);
    if (conversationId) {
      formData.append('conversation_id', conversationId);
    }
    const res = await client.post('/documents/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return res.data;
  },

  listDocuments: async (conversationId = null) => {
    const params = conversationId ? { conversation_id: conversationId } : {};
    const res = await client.get('/documents', { params });
    return res.data;
  },

  deleteDocument: async (id) => {
    const res = await client.delete(`/documents/${id}`);
    return res.data;
  },
};
