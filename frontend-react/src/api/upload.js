import apiClient from './client';

// Upload a single PDF file for a session
export const uploadPDF = async (sessionId, file) => {
  const formData = new FormData();
  formData.append('file', file);

  const response = await apiClient.post(`/sessions/${sessionId}/upload`, formData);
  return response.data;
};
