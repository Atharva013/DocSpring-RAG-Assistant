import React, { useState } from 'react';
import { Paper, InputBase, IconButton, CircularProgress } from '@mui/material';
import SendIcon from '@mui/icons-material/Send';

/**
 * ChatInput component for user question entry in Claude glassmorphism style.
 * Dynamically adjusts position when sidebar opens or closes.
 */
export default function ChatInput({ onSend, isDisabled, isSidebarOpen = true }) {
  const [question, setQuestion] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (question.trim() && !isDisabled) {
      onSend(question.trim());
      setQuestion('');
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  return (
    <Paper
      component="form"
      onSubmit={handleSubmit}
      elevation={6}
      sx={{
        position: 'fixed',
        bottom: 24,
        left: isSidebarOpen ? { xs: 16, md: 324 } : { xs: 16, md: 32 },
        right: { xs: 16, md: 32 },
        maxWidth: 920,
        margin: '0 auto',
        p: '6px 10px 6px 22px',
        display: 'flex',
        alignItems: 'center',
        borderRadius: 60,
        backgroundColor: 'rgba(24, 24, 27, 0.92)',
        backdropFilter: 'blur(20px)',
        border: '1px solid rgba(16, 185, 129, 0.4)',
        boxShadow: '0 12px 40px rgba(0, 0, 0, 0.4)',
        zIndex: 1100,
        animation: 'slideUpFade 0.45s ease-out forwards',
        transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
        '&:focus-within': {
          borderColor: '#10b981',
          boxShadow: '0 16px 50px rgba(16, 185, 129, 0.35)',
          transform: 'translateY(-2px)',
        },
      }}
    >
      <InputBase
        sx={{
          ml: 1,
          flex: 1,
          fontSize: '0.98rem',
          fontWeight: 500,
          color: '#ffffff',
          '& input::placeholder': {
            color: '#a1a1aa',
            opacity: 0.9,
          },
        }}
        placeholder="Ask about your PDFs…"
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        onKeyDown={handleKeyDown}
        disabled={isDisabled}
        multiline
        maxRows={4}
      />

      <IconButton
        type="submit"
        disabled={!question.trim() || isDisabled}
        sx={{
          p: '10px',
          backgroundColor: '#10b981',
          color: '#ffffff',
          boxShadow: '0 4px 14px rgba(16, 185, 129, 0.4)',
          transition: 'all 0.2s cubic-bezier(0.34, 1.56, 0.64, 1)',
          '&:hover': {
            backgroundColor: '#059669',
            transform: 'scale(1.1) rotate(-6deg)',
            boxShadow: '0 6px 18px rgba(16, 185, 129, 0.55)',
          },
          '&:active': {
            transform: 'scale(0.95) rotate(0deg)',
          },
          '&.Mui-disabled': {
            backgroundColor: 'rgba(255, 255, 255, 0.1)',
            color: '#71717a',
          },
        }}
      >
        {isDisabled ? <CircularProgress size={20} color="inherit" /> : <SendIcon sx={{ fontSize: 20 }} />}
      </IconButton>
    </Paper>
  );
}
