import apiClient from './client';

// Fetch all active chat sessions for the sidebar list
export const getSessions = async () => {
  const response = await apiClient.get('/sessions');
  return response.data;
};

// Create a new chat session
export const createSession = async () => {
  const response = await apiClient.post('/sessions');
  return response.data;
};

// Get details for a specific chat session (messages and documents)
export const getSessionDetail = async (sessionId) => {
  const response = await apiClient.get(`/sessions/${sessionId}`);
  return response.data;
};

// Delete a session and its associated documents/vectors
export const deleteSession = async (sessionId) => {
  const response = await apiClient.delete(`/sessions/${sessionId}`);
  return response.data;
};

// Rename a session title
export const renameSession = async (sessionId, title) => {
  const response = await apiClient.patch(`/sessions/${sessionId}/title`, { title });
  return response.data;
};
