import axios from 'axios';

// When running Vite dev server, proxy handles /api to http://localhost:8000
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api';

const client = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const api = {
  // Health
  checkHealth: async () => {
    const res = await client.get('/health');
    return res.data;
  },

  // Conversations
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
