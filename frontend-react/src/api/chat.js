import apiClient from './client';

// Ask a question for a given chat session
export const askQuestion = async (sessionId, question) => {
  const response = await apiClient.post(`/sessions/${sessionId}/chat`, { question });
  return response.data;
};

// Fetch deployment model names from backend health/info endpoint
export const getModelInfo = async () => {
  try {
    const response = await apiClient.get('/health/info');
    return response.data;
  } catch (error) {
    return { chat_model: '—', embedding_model: '—', search_index: '—' };
  }
};
