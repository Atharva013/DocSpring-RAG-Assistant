import React from 'react';
import { Paper, Box, Typography, Stack, Button, Tooltip, IconButton } from '@mui/material';
import MenuIcon from '@mui/icons-material/Menu';
import AccessTimeIcon from '@mui/icons-material/AccessTime';
import LayersIcon from '@mui/icons-material/Layers';
import DeleteIcon from '@mui/icons-material/Delete';
import logoImg from '../assets/logo.avif';

const getGreeting = () => {
  const hour = new Date().getHours();
  if (hour < 12) return 'Good morning ☀️';
  if (hour < 17) return 'Good afternoon 🌤️';
  return 'Good evening 🌙';
};

/**
 * Claude/GPT Style HeroHeader bar.
 * Clean, non-intrusive glassmorphism topbar with sidebar toggle button, title,
 * model architecture chips, and timestamp.
 */
export default function HeroHeader({
  title = 'New chat',
  updatedAt,
  chunkCount = 0,
  chatModel = 'DocSpring RAG Engine',
  embedModel = 'text-embedding-3-small',
  isSidebarOpen = true,
  onToggleSidebar,
  onDelete,
}) {
  return (
    <Box sx={{ mb: 3, animation: 'fadeInScale 0.35s ease-out forwards' }}>
      <Paper
        elevation={0}
        sx={{
          p: { xs: 2, md: 2.8 },
          borderRadius: '20px',
          background: 'rgba(24, 24, 27, 0.75)',
          backdropFilter: 'blur(20px)',
          border: '1px solid rgba(255, 255, 255, 0.08)',
          position: 'relative',
          color: '#f4f4f5',
          boxShadow: '0 8px 32px rgba(0, 0, 0, 0.25)',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          flexWrap: 'wrap',
          gap: 2,
        }}
      >
        {/* Left Side: Sidebar Open Toggle & Title */}
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1.8, maxWidth: { xs: '100%', md: '65%' } }}>
          {!isSidebarOpen && (
            <Tooltip title="Open Sidebar">
              <IconButton
                onClick={onToggleSidebar}
                sx={{
                  color: '#f4f4f5',
                  backgroundColor: 'rgba(255, 255, 255, 0.08)',
                  borderRadius: '12px',
                  p: 1,
                  '&:hover': { backgroundColor: 'rgba(255, 255, 255, 0.15)' },
                }}
              >
                <MenuIcon fontSize="small" />
              </IconButton>
            </Tooltip>
          )}

          <Box
            component="img"
            src={logoImg}
            alt="DocSpring Logo"
            sx={{
              width: 42,
              height: 42,
              borderRadius: '50%',
              objectFit: 'cover',
              border: '2px solid #10b981',
              boxShadow: '0 0 14px rgba(16, 185, 129, 0.35)',
              flexShrink: 0,
            }}
          />

          <Box>
            <Typography
              variant="h5"
              sx={{
                fontSize: { xs: '1.25rem', md: '1.5rem' },
                fontWeight: 800,
                letterSpacing: '-0.02em',
                color: '#ffffff',
              }}
            >
              {title}
            </Typography>

            <Typography
              variant="caption"
              sx={{ display: 'flex', alignItems: 'center', gap: 0.8, color: '#a1a1aa', mt: 0.3, fontWeight: 500, fontSize: '0.8rem' }}
            >
              <AccessTimeIcon fontSize="inherit" sx={{ color: '#38bdf8' }} />
              <b>{getGreeting()}</b> &bull; {updatedAt ? new Date(updatedAt).toLocaleString() : 'Just now'}
            </Typography>
          </Box>
        </Box>

        {/* Right Side: Model Badges & Actions */}
        <Stack direction="row" spacing={1.2} alignItems="center" flexWrap="wrap">
          {/* Chat Model Chip */}
          <Tooltip title="Azure AI RAG Model Deployment">
            <Box
              sx={{
                display: 'inline-flex',
                alignItems: 'center',
                gap: 0.8,
                px: 1.6,
                py: 0.6,
                backgroundColor: 'rgba(16, 185, 129, 0.12)',
                border: '1px solid rgba(16, 185, 129, 0.3)',
                borderRadius: '16px',
                fontSize: '0.76rem',
                fontWeight: 700,
                color: '#34d399',
              }}
            >
              <Box sx={{ width: 7, height: 7, borderRadius: '50%', backgroundColor: '#10b981', boxShadow: '0 0 6px #10b981' }} />
              <span>{chatModel || 'DocSpring RAG Engine'}</span>
            </Box>
          </Tooltip>

          {/* Chunks Badge */}
          <Tooltip title="Total Vector Indexed Chunks">
            <Box
              sx={{
                display: 'inline-flex',
                alignItems: 'center',
                gap: 0.6,
                px: 1.6,
                py: 0.6,
                backgroundColor: 'rgba(255, 255, 255, 0.05)',
                border: '1px solid rgba(255, 255, 255, 0.1)',
                borderRadius: '16px',
                fontSize: '0.76rem',
                fontWeight: 600,
                color: '#e4e4e7',
              }}
            >
              <LayersIcon style={{ fontSize: 14, color: '#fb923c' }} />
              <span>{chunkCount} Chunks</span>
            </Box>
          </Tooltip>

          {/* Delete Action */}
          {onDelete && (
            <Tooltip title="Delete Chat Session">
              <IconButton
                size="small"
                onClick={onDelete}
                sx={{
                  color: '#f87171',
                  backgroundColor: 'rgba(248, 113, 113, 0.1)',
                  borderRadius: '12px',
                  p: 0.8,
                  '&:hover': { backgroundColor: 'rgba(248, 113, 113, 0.22)' },
                }}
              >
                <DeleteIcon fontSize="small" />
              </IconButton>
            </Tooltip>
          )}
        </Stack>
      </Paper>
    </Box>
  );
}
