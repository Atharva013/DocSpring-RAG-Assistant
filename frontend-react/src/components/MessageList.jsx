import React, { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import { Box, Paper, Avatar, Typography, Stack, Chip, IconButton, Tooltip } from '@mui/material';
import AutoAwesomeIcon from '@mui/icons-material/AutoAwesome';
import PersonIcon from '@mui/icons-material/Person';
import BookmarkBorderIcon from '@mui/icons-material/BookmarkBorder';
import ContentCopyIcon from '@mui/icons-material/ContentCopy';
import CheckIcon from '@mui/icons-material/Check';
import logoImg from '../assets/logo.avif';

// Helper to deduplicate sources by file and page number
const getUniqueSources = (sourcesDetail) => {
  if (!sourcesDetail || !Array.isArray(sourcesDetail)) return [];
  const seen = new Set();
  const unique = [];

  for (const src of sourcesDetail) {
    const file = src.source_file || 'Document';
    const page = src.page_number || 0;
    const key = `${file}-${page}`;
    if (!seen.has(key)) {
      seen.add(key);
      unique.push({ file, page });
    }
  }

  return unique;
};

// Clean up markdown text for dynamic presentation
const formatMessageMarkdown = (text) => {
  if (!text) return '';
  let formatted = text.trim();
  formatted = formatted.replace(/([^\n])\n(\*\*[^*]+\*\*)\n/g, '$1\n\n$2\n');
  formatted = formatted.replace(/\n{3,}/g, '\n\n');
  return formatted;
};

/**
 * MessageList component displaying user questions and AI responses.
 * Features glassy light brown AI response cards with elegant curved ends,
 * clear spacing gap above the floating input, and proprietary branding.
 */
export default function MessageList({ messages = [], isThinking, onSelectSuggestion }) {
  const [copiedIndex, setCopiedIndex] = useState(null);

  const handleCopy = (text, index) => {
    navigator.clipboard.writeText(text);
    setCopiedIndex(index);
    setTimeout(() => setCopiedIndex(null), 2000);
  };

  const suggestions = [
    '⚡ Summarize this document in key bullet points',
    '📊 What are the main findings and analysis?',
    '🔍 Explain the security & architecture details',
  ];

  if (messages.length === 0 && !isThinking) {
    return (
      <Paper
        elevation={0}
        sx={{
          textAlign: 'center',
          py: 6,
          px: { xs: 2.5, sm: 5 },
          mb: 6,
          borderRadius: '24px',
          background: 'rgba(24, 24, 27, 0.75)',
          backdropFilter: 'blur(20px)',
          border: '1px solid rgba(255, 255, 255, 0.08)',
          boxSizing: 'border-box',
          maxWidth: '100%',
          color: '#f4f4f5',
          animation: 'fadeInScale 0.4s ease-out forwards',
        }}
      >
        <Box
          sx={{
            width: 72,
            height: 72,
            borderRadius: '50%',
            overflow: 'hidden',
            mx: 'auto',
            mb: 2.5,
            p: '2px',
            background: 'linear-gradient(135deg, #10b981 0%, #06b6d4 100%)',
            boxShadow: '0 0 24px rgba(16, 185, 129, 0.4)',
            animation: 'pulseGlow 3.5s infinite ease-in-out',
          }}
        >
          <Box
            component="img"
            src={logoImg}
            alt="DocSpring Logo"
            sx={{ width: '100%', height: '100%', borderRadius: '50%', objectFit: 'cover' }}
          />
        </Box>

        <Typography variant="h5" sx={{ color: '#ffffff', fontWeight: 800, mb: 1, letterSpacing: '-0.01em' }}>
          Ask Any Question About Your Uploaded PDFs
        </Typography>

        <Typography variant="body2" sx={{ color: '#a1a1aa', maxWidth: 520, mx: 'auto', mb: 3.5, fontSize: '0.92rem' }}>
          Upload PDF documents above, then type a question or select a quick suggestion below:
        </Typography>

        <Box
          sx={{
            display: 'flex',
            flexWrap: 'wrap',
            justifyContent: 'center',
            gap: 1.5,
            maxWidth: '100%',
            mx: 'auto',
          }}
        >
          {suggestions.map((q, idx) => (
            <Chip
              key={idx}
              label={q}
              onClick={() => onSelectSuggestion && onSelectSuggestion(q.replace(/^[^\s]+\s/, ''))}
              sx={{
                height: 'auto',
                py: 1.3,
                px: 1.8,
                borderRadius: '16px',
                backgroundColor: 'rgba(255, 255, 255, 0.05)',
                border: '1px solid rgba(255, 255, 255, 0.1)',
                color: '#f4f4f5',
                fontWeight: 600,
                fontSize: '0.86rem',
                cursor: 'pointer',
                transition: 'all 0.22s ease',
                '&:hover': {
                  borderColor: '#10b981',
                  backgroundColor: 'rgba(16, 185, 129, 0.15)',
                  color: '#34d399',
                  transform: 'translateY(-2px)',
                },
              }}
            />
          ))}
        </Box>
      </Paper>
    );
  }

  return (
    <Stack spacing={3} sx={{ mb: 4, pb: 2 }}>
      {messages.map((msg, index) => {
        const isUser = msg.role === 'user';
        const isCopied = copiedIndex === index;
        const uniqueSources = !isUser ? getUniqueSources(msg.sources_detail) : [];

        return (
          <Box
            key={index}
            sx={{
              display: 'flex',
              gap: 2,
              flexDirection: isUser ? 'row-reverse' : 'row',
              alignItems: 'flex-start',
              animation: 'fadeInScale 0.35s cubic-bezier(0.16, 1, 0.3, 1) forwards',
            }}
          >
            {/* Avatar */}
            {isUser ? (
              <Avatar
                sx={{
                  width: 40,
                  height: 40,
                  backgroundColor: '#10b981',
                  boxShadow: '0 4px 14px rgba(16, 185, 129, 0.4)',
                }}
              >
                <PersonIcon fontSize="small" />
              </Avatar>
            ) : (
              <Box
                sx={{
                  width: 40,
                  height: 40,
                  borderRadius: '50%',
                  p: '2px',
                  background: 'linear-gradient(135deg, #d97706 0%, #f59e0b 100%)',
                  boxShadow: '0 0 16px rgba(217, 119, 6, 0.4)',
                  flexShrink: 0,
                }}
              >
                <Box
                  component="img"
                  src={logoImg}
                  alt="DocSpring AI"
                  sx={{ width: '100%', height: '100%', borderRadius: '50%', objectFit: 'cover' }}
                />
              </Box>
            )}

            {/* Bubble */}
            <Paper
              elevation={0}
              sx={{
                p: 3,
                maxWidth: '85%',
                position: 'relative',
                borderRadius: '24px',
                backgroundColor: isUser ? '#059669' : 'rgba(38, 28, 20, 0.88)',
                backdropFilter: isUser ? 'none' : 'blur(24px)',
                color: isUser ? '#ffffff' : '#fef3c7',
                border: isUser ? 'none' : '1px solid rgba(217, 119, 6, 0.35)',
                boxShadow: isUser
                  ? '0 6px 20px rgba(5, 150, 105, 0.35)'
                  : '0 10px 35px rgba(0, 0, 0, 0.45), 0 0 20px rgba(217, 119, 6, 0.12)',
                transition: 'box-shadow 0.25s ease, transform 0.25s ease',
                '&:hover': {
                  boxShadow: isUser
                    ? '0 8px 24px rgba(5, 150, 105, 0.45)'
                    : '0 14px 45px rgba(0, 0, 0, 0.55), 0 0 25px rgba(217, 119, 6, 0.2)',
                },
              }}
            >
              {isUser ? (
                <Typography variant="body1" sx={{ whiteSpace: 'pre-wrap', lineHeight: 1.65, fontSize: '0.98rem', fontWeight: 500 }}>
                  {msg.message}
                </Typography>
              ) : (
                <>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                    <Box
                      sx={{
                        fontSize: '0.96rem',
                        lineHeight: 1.8,
                        color: '#fef3c7',
                        flex: 1,
                        '& p': { m: 0, mb: 1.4 },
                        '& p:last-child': { mb: 0 },
                        '& h1, & h2, & h3, & h4, & h5, & h6': { fontWeight: 800, mt: 2, mb: 1, color: '#fef08a' },
                        '& ul, & ol': { pl: 2.5, m: 0, mb: 1.4 },
                        '& li': { mb: 0.6 },
                        '& strong, & b': { fontWeight: 800, color: '#fbbf24', display: 'inline-block' },
                        '& code': { backgroundColor: 'rgba(255, 255, 255, 0.08)', p: '2px 6px', borderRadius: 1, fontFamily: 'monospace', fontSize: '0.88em', color: '#fde68a' },
                      }}
                    >
                      <ReactMarkdown
                        components={{
                          h1: ({ children }) => <Typography variant="h6" sx={{ fontWeight: 800, color: '#fef08a', mt: 2, mb: 1 }}>{children}</Typography>,
                          h2: ({ children }) => <Typography variant="subtitle1" sx={{ fontWeight: 800, color: '#fef08a', mt: 2, mb: 1 }}>{children}</Typography>,
                          h3: ({ children }) => <Typography variant="subtitle2" sx={{ fontWeight: 800, color: '#fef08a', mt: 1.5, mb: 0.5 }}>{children}</Typography>,
                          strong: ({ children }) => (
                            <Typography
                              component="span"
                              sx={{
                                fontWeight: 800,
                                color: '#fef08a',
                                fontSize: '0.98rem',
                                display: 'block',
                                mt: 1.5,
                                mb: 0.5,
                                background: 'linear-gradient(135deg, #fef08a 0%, #f59e0b 100%)',
                                WebkitBackgroundClip: 'text',
                                WebkitTextFillColor: 'transparent',
                              }}
                            >
                              {children}
                            </Typography>
                          ),
                        }}
                      >
                        {formatMessageMarkdown(msg.message)}
                      </ReactMarkdown>
                    </Box>

                    {/* Copy Button */}
                    <Tooltip title={isCopied ? 'Copied!' : 'Copy answer'}>
                      <IconButton
                        size="small"
                        onClick={() => handleCopy(msg.message, index)}
                        sx={{
                          ml: 1.5,
                          color: '#d97706',
                          transition: 'all 0.2s ease',
                          '&:hover': { color: '#fbbf24', backgroundColor: 'rgba(217, 119, 6, 0.2)', transform: 'scale(1.1)' },
                        }}
                      >
                        {isCopied ? <CheckIcon fontSize="small" color="success" /> : <ContentCopyIcon fontSize="small" />}
                      </IconButton>
                    </Tooltip>
                  </Box>

                  {/* Deduplicated Source Citation Chips */}
                  {uniqueSources.length > 0 && (
                    <Box sx={{ mt: 2.5, pt: 1.8, borderTop: '1px solid rgba(217, 119, 6, 0.25)' }}>
                      <Typography variant="caption" sx={{ color: '#fbbf24', fontWeight: 800, display: 'block', mb: 1, letterSpacing: '0.04em' }}>
                        CITED SOURCES
                      </Typography>
                      <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                        {uniqueSources.map((src, i) => (
                          <Chip
                            key={i}
                            size="small"
                            icon={<BookmarkBorderIcon style={{ fontSize: 13, color: '#f59e0b' }} />}
                            label={`${src.file}${src.page ? ` · p.${src.page}` : ''}`}
                            sx={{
                              backgroundColor: 'rgba(217, 119, 6, 0.18)',
                              border: '1px solid rgba(217, 119, 6, 0.35)',
                              color: '#fbbf24',
                              fontWeight: 700,
                              fontSize: '0.74rem',
                              transition: 'all 0.2s ease',
                              '&:hover': {
                                backgroundColor: 'rgba(217, 119, 6, 0.3)',
                                transform: 'translateY(-1px)',
                              },
                            }}
                          />
                        ))}
                      </Box>
                    </Box>
                  )}
                </>
              )}
            </Paper>
          </Box>
        );
      })}

      {/* Thinking Indicator */}
      {isThinking && (
        <Box sx={{ display: 'flex', gap: 2, alignItems: 'center', animation: 'fadeInScale 0.3s ease-out forwards' }}>
          <Box
            sx={{
              width: 40,
              height: 40,
              borderRadius: '50%',
              p: '2px',
              background: 'linear-gradient(135deg, #d97706 0%, #f59e0b 100%)',
              boxShadow: '0 0 16px rgba(217, 119, 6, 0.5)',
              animation: 'pulseGlow 2s infinite ease-in-out',
            }}
          >
            <Box
              component="img"
              src={logoImg}
              alt="Thinking"
              sx={{ width: '100%', height: '100%', borderRadius: '50%', objectFit: 'cover' }}
            />
          </Box>
          <Paper
            elevation={0}
            sx={{
              p: 2.2,
              borderRadius: '24px',
              backgroundColor: 'rgba(38, 28, 20, 0.88)',
              backdropFilter: 'blur(20px)',
              border: '1px solid rgba(217, 119, 6, 0.4)',
              boxShadow: '0 4px 20px rgba(217, 119, 6, 0.25)',
              display: 'flex',
              alignItems: 'center',
              gap: 1.5,
              animation: 'pulseGlow 2.5s infinite ease-in-out',
            }}
          >
            <Typography variant="body2" sx={{ color: '#fbbf24', fontWeight: 700 }}>
               RAG Pipeline active — searching vectors & generating response…
            </Typography>
          </Paper>
        </Box>
      )}
    </Stack>
  );
}
