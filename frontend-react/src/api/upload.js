import apiClient from './client';

// Upload a single PDF file for a session
export const uploadPDF = async (sessionId, file) => {
  const formData = new FormData();

  // Ensure file object has valid MIME type if browser dropped file with generic/empty type
  const fileToUpload =
    file.name.toLowerCase().endsWith('.pdf') && (!file.type || file.type !== 'application/pdf')
      ? new File([file], file.name, { type: 'application/pdf' })
      : file;

  formData.append('file', fileToUpload);

  const response = await apiClient.post(`/sessions/${sessionId}/upload`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  return response.data;
};
