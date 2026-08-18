import React, { useState } from 'react';
import { Paper, InputBase, IconButton, CircularProgress } from '@mui/material';
import SendIcon from '@mui/icons-material/Send';

/**
 * ChatInput component for user question entry.
 * MUI Components Used:
 * - Paper: https://mui.com/material-ui/react-paper/
 * - InputBase: https://mui.com/material-ui/react-input/
 * - IconButton: https://mui.com/material-ui/react-button/#icon-button
 */
export default function ChatInput({ onSend, isDisabled }) {
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
      elevation={4}
      sx={{
        position: 'fixed',
        bottom: 24,
        left: { xs: 16, sm: 300 },
        right: 24,
        maxWidth: 900,
        margin: '0 auto',
        p: '4px 8px 4px 20px',
        display: 'flex',
        alignItems: 'center',
        borderRadius: 60,
        backgroundColor: '#ffffff',
        border: '2px solid #16a34a',
        boxShadow: '0 8px 30px rgba(22, 163, 74, 0.15)',
        zIndex: 1100,
        animation: 'slideUpFade 0.45s ease-out forwards',
        transition: 'all 0.25s cubic-bezier(0.4, 0, 0.2, 1)',
        '&:focus-within': {
          borderColor: '#15803d',
          boxShadow: '0 12px 40px rgba(22, 163, 74, 0.3)',
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
          color: '#0f172a',
          '& input::placeholder': {
            color: '#64748b',
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
          backgroundColor: '#16a34a',
          color: '#ffffff',
          boxShadow: '0 4px 14px rgba(22, 163, 74, 0.4)',
          transition: 'all 0.2s cubic-bezier(0.34, 1.56, 0.64, 1)',
          '&:hover': {
            backgroundColor: '#15803d',
            transform: 'scale(1.12) rotate(-8deg)',
            boxShadow: '0 6px 18px rgba(22, 163, 74, 0.5)',
          },
          '&:active': {
            transform: 'scale(0.95) rotate(0deg)',
          },
          '&.Mui-disabled': {
            backgroundColor: '#86efac',
            color: '#ffffff',
          },
        }}
      >
        {isDisabled ? <CircularProgress size={20} color="inherit" /> : <SendIcon sx={{ fontSize: 20 }} />}
      </IconButton>
    </Paper>
  );
}
