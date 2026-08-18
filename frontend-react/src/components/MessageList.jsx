import React, { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import { Box, Paper, Avatar, Typography, Stack, Chip, IconButton, Tooltip } from '@mui/material';
import AutoAwesomeIcon from '@mui/icons-material/AutoAwesome';
import PersonIcon from '@mui/icons-material/Person';
import BookmarkBorderIcon from '@mui/icons-material/BookmarkBorder';
import ContentCopyIcon from '@mui/icons-material/ContentCopy';
import CheckIcon from '@mui/icons-material/Check';

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

// Normalizes markdown text so section headers like "Summary:", "Key points:", "Sources:"
// are converted to bold section titles (**Summary**, **Key points**, **Sources**) on their own line.
const formatMessageMarkdown = (text) => {
  if (!text) return '';
  let formatted = text;

  // Convert "Summary:", "Summary :", "### Summary", "# Summary" to "**Summary**\n"
  formatted = formatted.replace(/^(?:#+\s*)?Summary\s*:\s*/gmi, '**Summary**\n');
  formatted = formatted.replace(/^(?:#+\s*)Summary\b/gmi, '**Summary**');

  // Convert "Key points:", "Key Points:", "### Key points" to "\n\n**Key points**\n"
  formatted = formatted.replace(/^(?:#+\s*)?Key\s+[pP]oints\s*:\s*/gmi, '\n\n**Key points**\n');
  formatted = formatted.replace(/^(?:#+\s*)Key\s+[pP]oints\b/gmi, '\n\n**Key points**');

  // Convert "Sources:", "Cited Sources:", "### Sources" to "\n\n**Sources**\n"
  formatted = formatted.replace(/^(?:#+\s*)?(?:Cited\s+)?Sources\s*:\s*/gmi, '\n\n**Sources**\n');
  formatted = formatted.replace(/^(?:#+\s*)(?:Cited\s+)?Sources\b/gmi, '\n\n**Sources**');

  // Clean up excessive empty lines
  formatted = formatted.replace(/\n{3,}/g, '\n\n');
  return formatted.trim();
};

/**
 * MessageList component displaying user questions and AI responses with:
 * - Consistent bold markdown headers
 * - Wrapped suggestion chips inside card bounds
 * - Deduplicated citation chips
 */
export default function MessageList({ messages = [], isThinking, onSelectSuggestion }) {
  const [copiedIndex, setCopiedIndex] = useState(null);

  const handleCopy = (text, index) => {
    navigator.clipboard.writeText(text);
    setCopiedIndex(index);
    setTimeout(() => setCopiedIndex(null), 2000);
  };

  const suggestions = [
    '⚡ Summarize this document in 3 key bullet points',
    '📊 What are the main products and services offered?',
    '🔍 What are the key details and security solutions?',
  ];

  if (messages.length === 0 && !isThinking) {
    return (
      <Paper
        elevation={0}
        sx={{
          textAlign: 'center',
          py: 5,
          px: { xs: 2, sm: 4 },
          mb: 4,
          borderRadius: 5,
          background: 'linear-gradient(135deg, rgba(240, 253, 244, 0.4) 0%, rgba(255, 255, 255, 0.9) 100%)',
          border: '1px solid #e2e8f0',
          boxSizing: 'border-box',
          maxWidth: '100%',
          overflow: 'hidden',
          animation: 'fadeInScale 0.4s ease-out forwards',
        }}
      >
        <Box
          sx={{
            width: 56,
            height: 56,
            borderRadius: '16px',
            background: 'linear-gradient(135deg, #22c55e 0%, #16a34a 100%)',
            display: 'inline-flex',
            alignItems: 'center',
            justifyContent: 'center',
            color: '#ffffff',
            mb: 2,
            boxShadow: '0 6px 20px rgba(22, 163, 74, 0.3)',
            animation: 'pulseGlow 3s infinite ease-in-out',
          }}
        >
          <AutoAwesomeIcon sx={{ fontSize: 30 }} />
        </Box>

        <Typography variant="h6" sx={{ color: '#0f172a', fontWeight: 800, mb: 1 }}>
          Ask Any Question About Your Uploaded PDFs
        </Typography>

        <Typography variant="body2" sx={{ color: '#64748b', maxWidth: 500, mx: 'auto', mb: 3 }}>
          Upload PDF files above, then type a question or pick one of these quick suggestions:
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
                py: 1.2,
                px: 1.5,
                borderRadius: '14px',
                backgroundColor: '#ffffff',
                border: '1px solid #cbd5e1',
                color: '#1e293b',
                fontWeight: 600,
                fontSize: '0.85rem',
                cursor: 'pointer',
                boxShadow: '0 2px 8px rgba(0,0,0,0.04)',
                maxWidth: '100%',
                '& .MuiChip-label': {
                  whiteSpace: 'normal',
                  wordBreak: 'break-word',
                  display: 'block',
                  py: 0.2,
                },
                '&:hover': {
                  borderColor: '#16a34a',
                  backgroundColor: '#f0fdf4',
                  color: '#15803d',
                  transform: 'translateY(-3px)',
                  boxShadow: '0 6px 16px rgba(22, 163, 74, 0.15)',
                },
                transition: 'all 0.22s ease',
              }}
            />
          ))}
        </Box>
      </Paper>
    );
  }

  return (
    <Stack spacing={2.5} sx={{ mb: 4 }}>
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
            <Avatar
              sx={{
                width: 38,
                height: 38,
                backgroundColor: isUser ? '#16a34a' : '#0f172a',
                boxShadow: isUser ? '0 4px 14px rgba(22, 163, 74, 0.35)' : '0 4px 14px rgba(15, 23, 42, 0.25)',
                transition: 'transform 0.2s ease',
                '&:hover': {
                  transform: 'scale(1.08)',
                },
              }}
            >
              {isUser ? <PersonIcon fontSize="small" /> : <AutoAwesomeIcon fontSize="small" sx={{ color: '#4ade80' }} />}
            </Avatar>

            {/* Bubble */}
            <Paper
              elevation={0}
              sx={{
                p: 2.5,
                maxWidth: '85%',
                position: 'relative',
                borderRadius: isUser ? '22px 22px 4px 22px' : '22px 22px 22px 4px',
                backgroundColor: isUser ? '#16a34a' : '#ffffff',
                color: isUser ? '#ffffff' : '#0f172a',
                border: isUser ? 'none' : '1px solid #e2e8f0',
                boxShadow: isUser ? '0 6px 18px rgba(22, 163, 74, 0.25)' : '0 3px 12px rgba(0, 0, 0, 0.04)',
                transition: 'box-shadow 0.2s ease, transform 0.2s ease',
                '&:hover': {
                  boxShadow: isUser ? '0 8px 22px rgba(22, 163, 74, 0.35)' : '0 6px 20px rgba(0, 0, 0, 0.07)',
                },
              }}
            >
              {isUser ? (
                <Typography variant="body1" sx={{ whiteSpace: 'pre-wrap', lineHeight: 1.6, fontSize: '0.96rem', fontWeight: 500 }}>
                  {msg.message}
                </Typography>
              ) : (
                <>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                    <Box
                      sx={{
                        fontSize: '0.96rem',
                        lineHeight: 1.7,
                        color: '#0f172a',
                        flex: 1,
                        '& p': { m: 0, mb: 1.2 },
                        '& p:last-child': { mb: 0 },
                        '& h1, & h2, & h3, & h4, & h5, & h6': { fontWeight: 800, mt: 1.8, mb: 0.8, color: '#0f172a' },
                        '& ul, & ol': { pl: 2.5, m: 0, mb: 1.2 },
                        '& li': { mb: 0.5 },
                        '& strong, & b': { fontWeight: 800, color: '#0f172a' },
                        '& code': { backgroundColor: '#f1f5f9', p: '2px 6px', borderRadius: 1, fontFamily: 'monospace', fontSize: '0.88em' },
                      }}
                    >
                      <ReactMarkdown
                        components={{
                          h1: ({ children }) => <Typography variant="h6" sx={{ fontWeight: 800, color: '#0f172a', mt: 2, mb: 1 }}>{children}</Typography>,
                          h2: ({ children }) => <Typography variant="subtitle1" sx={{ fontWeight: 800, color: '#0f172a', mt: 2, mb: 1 }}>{children}</Typography>,
                          h3: ({ children }) => <Typography variant="subtitle2" sx={{ fontWeight: 800, color: '#0f172a', mt: 1.5, mb: 0.5 }}>{children}</Typography>,
                          strong: ({ children }) => <strong style={{ fontWeight: 800, color: '#0f172a' }}>{children}</strong>,
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
                    <Box sx={{ mt: 2, pt: 1.5, borderTop: '1px solid #f1f5f9' }}>
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
          <Avatar sx={{ width: 38, height: 38, backgroundColor: '#0f172a', animation: 'pulseGlow 2s infinite ease-in-out' }}>
            <AutoAwesomeIcon fontSize="small" sx={{ color: '#4ade80' }} />
          </Avatar>
          <Paper
            elevation={0}
            sx={{
              p: 2.2,
              borderRadius: '22px 22px 22px 4px',
              backgroundColor: '#ffffff',
              border: '1px solid #bbf7d0',
              boxShadow: '0 4px 16px rgba(22, 163, 74, 0.12)',
              display: 'flex',
              alignItems: 'center',
              gap: 1.5,
              animation: 'pulseGlow 2.5s infinite ease-in-out',
            }}
          >
            <Typography variant="body2" sx={{ color: '#16a34a', fontWeight: 700 }}>
              🧠 RAG Pipeline active — searching vectors & generating answer…
            </Typography>
          </Paper>
        </Box>
      )}
    </Stack>
  );
}

