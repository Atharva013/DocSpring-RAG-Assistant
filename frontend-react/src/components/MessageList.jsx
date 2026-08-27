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
  // Ensure standalone bold section titles have space
  formatted = formatted.replace(/([^\n])\n(\*\*[^*]+\*\*)\n/g, '$1\n\n$2\n');
  formatted = formatted.replace(/\n{3,}/g, '\n\n');
  return formatted;
};

/**
 * Glorified MessageList component displaying user questions and AI responses.
 * Features custom logo avatar, dynamic Gemini/GPT style rendering,
 * deduplicated source citation chips, and smooth entrance micro-animations.
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
          mb: 4,
          borderRadius: 5,
          background: 'linear-gradient(135deg, rgba(15, 23, 42, 0.95) 0%, rgba(30, 41, 59, 0.9) 100%)',
          backdropFilter: 'blur(20px)',
          border: '1px solid rgba(255, 255, 255, 0.1)',
          boxSizing: 'border-box',
          maxWidth: '100%',
          color: '#ffffff',
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
            p: '3px',
            background: 'linear-gradient(135deg, #22c55e 0%, #06b6d4 50%, #f97316 100%)',
            boxShadow: '0 0 24px rgba(34, 197, 94, 0.45)',
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

        <Typography variant="h5" sx={{ color: '#ffffff', fontWeight: 900, mb: 1, letterSpacing: '-0.01em' }}>
          Ask Any Question About Your Uploaded PDFs
        </Typography>

        <Typography variant="body2" sx={{ color: '#94a3b8', maxWidth: 520, mx: 'auto', mb: 3.5, fontSize: '0.92rem' }}>
          Upload your PDF documents above, then type a question or select one of these quick prompt suggestions:
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
                border: '1px solid rgba(255, 255, 255, 0.12)',
                color: '#f8fafc',
                fontWeight: 600,
                fontSize: '0.86rem',
                cursor: 'pointer',
                transition: 'all 0.22s ease',
                '&:hover': {
                  borderColor: '#22c55e',
                  backgroundColor: 'rgba(34, 197, 94, 0.18)',
                  color: '#4ade80',
                  transform: 'translateY(-3px)',
                  boxShadow: '0 6px 20px rgba(34, 197, 94, 0.25)',
                },
              }}
            />
          ))}
        </Box>
      </Paper>
    );
  }

  return (
    <Stack spacing={2.8} sx={{ mb: 4 }}>
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
                  width: 42,
                  height: 42,
                  backgroundColor: '#16a34a',
                  boxShadow: '0 4px 16px rgba(22, 163, 74, 0.4)',
                }}
              >
                <PersonIcon fontSize="small" />
              </Avatar>
            ) : (
              <Box
                sx={{
                  width: 42,
                  height: 42,
                  borderRadius: '50%',
                  p: '2px',
                  background: 'linear-gradient(135deg, #22c55e 0%, #06b6d4 100%)',
                  boxShadow: '0 0 16px rgba(34, 197, 94, 0.4)',
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
                p: 2.8,
                maxWidth: '85%',
                position: 'relative',
                borderRadius: isUser ? '24px 24px 4px 24px' : '24px 24px 24px 4px',
                backgroundColor: isUser ? '#16a34a' : '#ffffff',
                color: isUser ? '#ffffff' : '#0f172a',
                border: isUser ? 'none' : '1px solid #e2e8f0',
                boxShadow: isUser ? '0 6px 20px rgba(22, 163, 74, 0.3)' : '0 4px 20px rgba(0, 0, 0, 0.05)',
                transition: 'box-shadow 0.2s ease, transform 0.2s ease',
                '&:hover': {
                  boxShadow: isUser ? '0 8px 24px rgba(22, 163, 74, 0.4)' : '0 8px 25px rgba(0, 0, 0, 0.08)',
                },
              }}
            >
              {isUser ? (
                <Typography variant="body1" sx={{ whiteSpace: 'pre-wrap', lineHeight: 1.6, fontSize: '0.98rem', fontWeight: 500 }}>
                  {msg.message}
                </Typography>
              ) : (
                <>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                    <Box
                      sx={{
                        fontSize: '0.96rem',
                        lineHeight: 1.75,
                        color: '#0f172a',
                        flex: 1,
                        '& p': { m: 0, mb: 1.4 },
                        '& p:last-child': { mb: 0 },
                        '& h1, & h2, & h3, & h4, & h5, & h6': { fontWeight: 800, mt: 2, mb: 1, color: '#0f172a' },
                        '& ul, & ol': { pl: 2.5, m: 0, mb: 1.4 },
                        '& li': { mb: 0.6 },
                        '& strong, & b': { fontWeight: 800, color: '#16a34a', display: 'inline-block' },
                        '& code': { backgroundColor: '#f1f5f9', p: '2px 6px', borderRadius: 1, fontFamily: 'monospace', fontSize: '0.88em' },
                      }}
                    >
                      <ReactMarkdown
                        components={{
                          h1: ({ children }) => <Typography variant="h6" sx={{ fontWeight: 800, color: '#0f172a', mt: 2, mb: 1 }}>{children}</Typography>,
                          h2: ({ children }) => <Typography variant="subtitle1" sx={{ fontWeight: 800, color: '#0f172a', mt: 2, mb: 1 }}>{children}</Typography>,
                          h3: ({ children }) => <Typography variant="subtitle2" sx={{ fontWeight: 800, color: '#0f172a', mt: 1.5, mb: 0.5 }}>{children}</Typography>,
                          strong: ({ children }) => (
                            <Typography
                              component="span"
                              sx={{
                                fontWeight: 800,
                                color: '#0f172a',
                                fontSize: '1rem',
                                display: 'block',
                                mt: 1.5,
                                mb: 0.5,
                                background: 'linear-gradient(135deg, #0f172a 0%, #16a34a 100%)',
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
                          ml: 1,
                          color: '#64748b',
                          transition: 'all 0.2s ease',
                          '&:hover': { color: '#16a34a', backgroundColor: '#f0fdf4', transform: 'scale(1.1)' },
                        }}
                      >
                        {isCopied ? <CheckIcon fontSize="small" color="success" /> : <ContentCopyIcon fontSize="small" />}
                      </IconButton>
                    </Tooltip>
                  </Box>

                  {/* Deduplicated Source Citation Chips */}
                  {uniqueSources.length > 0 && (
                    <Box sx={{ mt: 2.5, pt: 1.8, borderTop: '1px solid #f1f5f9' }}>
                      <Typography variant="caption" sx={{ color: '#64748b', fontWeight: 800, display: 'block', mb: 1, letterSpacing: '0.04em' }}>
                        CITED SOURCES
                      </Typography>
                      <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                        {uniqueSources.map((src, i) => (
                          <Chip
                            key={i}
                            size="small"
                            icon={<BookmarkBorderIcon style={{ fontSize: 13, color: '#16a34a' }} />}
                            label={`${src.file}${src.page ? ` · p.${src.page}` : ''}`}
                            sx={{
                              backgroundColor: '#f0fdf4',
                              border: '1px solid #d1fae5',
                              color: '#15803d',
                              fontWeight: 700,
                              fontSize: '0.74rem',
                              transition: 'all 0.2s ease',
                              '&:hover': {
                                backgroundColor: '#dcfce7',
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
              width: 42,
              height: 42,
              borderRadius: '50%',
              p: '2px',
              background: 'linear-gradient(135deg, #22c55e 0%, #06b6d4 100%)',
              boxShadow: '0 0 18px rgba(34, 197, 94, 0.5)',
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
              borderRadius: '24px 24px 24px 4px',
              backgroundColor: '#ffffff',
              border: '1px solid #bbf7d0',
              boxShadow: '0 4px 16px rgba(22, 163, 74, 0.15)',
              display: 'flex',
              alignItems: 'center',
              gap: 1.5,
              animation: 'pulseGlow 2.5s infinite ease-in-out',
            }}
          >
            <Typography variant="body2" sx={{ color: '#16a34a', fontWeight: 700 }}>
              🧠 RAG Pipeline active — searching vectors & generating response…
            </Typography>
          </Paper>
        </Box>
      )}
    </Stack>
  );
}
