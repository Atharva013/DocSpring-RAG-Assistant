import React, { useState, useEffect } from 'react';
import { Box, Container, Alert, Snackbar } from '@mui/material';
import Sidebar from './components/Sidebar';
import HeroHeader from './components/HeroHeader';
import DocumentsPanel from './components/DocumentsPanel';
import UploadPanel from './components/UploadPanel';
import MessageList from './components/MessageList';
import ChatInput from './components/ChatInput';
import DeleteDialog from './components/DeleteDialog';

import {
  getSessions,
  createSession,
  getSessionDetail,
  deleteSession,
} from './api/sessions';
import { uploadPDF } from './api/upload';
import { askQuestion, getModelInfo } from './api/chat';

export default function App() {
  const [sessions, setSessions] = useState([]);
  const [activeSessionId, setActiveSessionId] = useState(null);
  const [sessionDetail, setSessionDetail] = useState(null);
  const [modelInfo, setModelInfo] = useState({ chat_model: '—', embedding_model: '—' });

  const [isThinking, setIsThinking] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  const [isDeleting, setIsDeleting] = useState(false);

  const [uploadStatus, setUploadStatus] = useState(null);
  const [errorMessage, setErrorMessage] = useState(null);
  const [successMessage, setSuccessMessage] = useState(null);

  const [deleteModal, setDeleteModal] = useState({ open: false, target: null });

  // 1. Initial Load: Fetch Sessions & Model Info
  useEffect(() => {
    fetchInitialData();
  }, []);

  const fetchInitialData = async () => {
    try {
      const info = await getModelInfo();
      setModelInfo(info);

      const sessionList = await getSessions();
      setSessions(sessionList);

      if (sessionList.length > 0) {
        loadSession(sessionList[0].session_id);
      } else {
        handleNewChat();
      }
    } catch (err) {
      setErrorMessage('Could not connect to FastAPI backend. Please ensure uvicorn is running on http://localhost:8000.');
    }
  };

  // 2. Load Session Details
  const loadSession = async (sessionId) => {
    try {
      setActiveSessionId(sessionId);
      const detail = await getSessionDetail(sessionId);
      setSessionDetail(detail);
    } catch (err) {
      setErrorMessage(`Failed to load session ${sessionId}`);
    }
  };

  // 3. Create New Chat
  const handleNewChat = async () => {
    try {
      const newSession = await createSession();
      setSessions((prev) => [newSession, ...prev]);
      setActiveSessionId(newSession.session_id);
      setSessionDetail({
        session: newSession,
        documents: [],
        messages: [],
      });
    } catch (err) {
      setErrorMessage('Failed to create new chat session');
    }
  };

  // 4. Upload & Index PDF
  const handleUploadPDF = async (file) => {
    if (!activeSessionId) return;

    setIsUploading(true);
    setUploadStatus(null);
    try {
      const res = await uploadPDF(activeSessionId, file);
      setUploadStatus({
        type: 'success',
        message: `Successfully indexed ${res.filename} (${res.chunks_indexed} chunks)`,
      });
      // Refresh session detail & list
      await loadSession(activeSessionId);
      const updatedSessions = await getSessions();
      setSessions(updatedSessions);
    } catch (err) {
      setUploadStatus({
        type: 'error',
        message: err.response?.data?.detail || 'Failed to upload and index PDF.',
      });
    } finally {
      setIsUploading(false);
    }
  };

  // 5. Send Question
  const handleSendQuestion = async (questionText) => {
    if (!activeSessionId) return;

    // Optimistically append user message
    const tempUserMsg = { role: 'user', message: questionText };
    setSessionDetail((prev) => ({
      ...prev,
      messages: [...(prev?.messages || []), tempUserMsg],
    }));

    setIsThinking(true);
    try {
      const res = await askQuestion(activeSessionId, questionText);
      const assistantMsg = {
        role: 'assistant',
        message: res.answer,
        sources_detail: res.sources_detail || [],
      };
      setSessionDetail((prev) => ({
        ...prev,
        messages: [...prev.messages, assistantMsg],
      }));

      // Refresh sessions in case title was auto-renamed
      const updatedSessions = await getSessions();
      setSessions(updatedSessions);
    } catch (err) {
      setErrorMessage('Error fetching answer from backend');
    } finally {
      setIsThinking(false);
    }
  };

  // 6. Delete Session Confirmation
  const handleDeleteConfirm = async () => {
    if (!deleteModal.target) return;
    const targetId = deleteModal.target.session_id;

    setIsDeleting(true);
    try {
      await deleteSession(targetId);
      const remaining = sessions.filter((s) => s.session_id !== targetId);
      setSessions(remaining);
      setDeleteModal({ open: false, target: null });
      setSuccessMessage('Chat session deleted successfully.');

      if (remaining.length > 0) {
        loadSession(remaining[0].session_id);
      } else {
        handleNewChat();
      }
    } catch (err) {
      setErrorMessage('Failed to delete chat session');
    } finally {
      setIsDeleting(false);
    }
  };

  const activeSessionObj = sessionDetail?.session || {};
  const documents = sessionDetail?.documents || [];
  const messages = sessionDetail?.messages || [];
  const totalChunks = documents.reduce((acc, d) => acc + (d.chunks_indexed || d.chunk_count || 0), 0);

  return (
    <Box sx={{ display: 'flex', minHeight: '100vh', backgroundColor: '#f8fafc' }}>
      {/* Sidebar Navigation */}
      <Sidebar
        sessions={sessions}
        activeSessionId={activeSessionId}
        onSelectSession={loadSession}
        onNewChat={handleNewChat}
        onDeleteSession={(sess) => setDeleteModal({ open: true, target: sess })}
      />

      {/* Main Content Area */}
      <Box component="main" sx={{ flexGrow: 1, p: 3, pb: 14, overflowX: 'hidden' }}>
        <Container maxWidth="lg">
          {/* Top Hero Card Widget */}
          <HeroHeader
            title={activeSessionObj.title || 'New chat'}
            updatedAt={activeSessionObj.updated_at}
            chunkCount={totalChunks}
            chatModel={modelInfo.chat_model}
            embedModel={modelInfo.embedding_model}
            onDelete={() => setDeleteModal({ open: true, target: activeSessionObj })}
          />

          {/* Indexed Documents Panel */}
          <DocumentsPanel documents={documents} />

          {/* PDF Upload Widget */}
          <UploadPanel
            onUpload={handleUploadPDF}
            isUploading={isUploading}
            uploadStatus={uploadStatus}
          />

          {/* Chat Message History */}
          <MessageList messages={messages} isThinking={isThinking} onSelectSuggestion={handleSendQuestion} />

          {/* Message Input Pill */}
          <ChatInput onSend={handleSendQuestion} isDisabled={isThinking} />
        </Container>
      </Box>

      {/* Delete Modal Confirmation */}
      <DeleteDialog
        open={deleteModal.open}
        sessionTitle={deleteModal.target?.title}
        isDeleting={isDeleting}
        onClose={() => setDeleteModal({ open: false, target: null })}
        onConfirm={handleDeleteConfirm}
      />

      {/* Error Toast */}
      <Snackbar
        open={Boolean(errorMessage)}
        autoHideDuration={6000}
        onClose={() => setErrorMessage(null)}
      >
        <Alert severity="error" onClose={() => setErrorMessage(null)} sx={{ width: '100%' }}>
          {errorMessage}
        </Alert>
      </Snackbar>

      {/* Success Toast */}
      <Snackbar
        open={Boolean(successMessage)}
        autoHideDuration={4000}
        onClose={() => setSuccessMessage(null)}
      >
        <Alert severity="success" onClose={() => setSuccessMessage(null)} sx={{ width: '100%' }}>
          {successMessage}
        </Alert>
      </Snackbar>
    </Box>
  );
}
