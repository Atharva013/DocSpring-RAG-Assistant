import React from 'react';
import { Paper, Box, Typography, Chip, Stack, Button, Tooltip } from '@mui/material';
import ChatIcon from '@mui/icons-material/Chat';
import AccessTimeIcon from '@mui/icons-material/AccessTime';
import LayersIcon from '@mui/icons-material/Layers';
import DeleteIcon from '@mui/icons-material/Delete';
import AutoAwesomeIcon from '@mui/icons-material/AutoAwesome';
import ThreeBackgroundCanvas from './ThreeBackgroundCanvas';
import logoImg from '../assets/logo.avif';

const getGreeting = () => {
  const hour = new Date().getHours();
  if (hour < 12) return 'Good morning ☀️';
  if (hour < 17) return 'Good afternoon 🌤️';
  return 'Good evening 🌙';
};

/**
 * Glorified HeroHeader component with embedded Three.js 3D RAG canvas,
 * dynamic model badges, custom logo, and high-tech glassmorphism styling.
 */
export default function HeroHeader({
  title = 'New chat',
  updatedAt,
  chunkCount = 0,
  chatModel = 'gpt-4.1-mini',
  embedModel = 'text-embedding-3-small',
  onDelete,
}) {
  return (
    <Box sx={{ mb: 3, animation: 'fadeInScale 0.4s cubic-bezier(0.4, 0, 0.2, 1) forwards', position: 'relative' }}>
      <Paper
        elevation={0}
        sx={{
          p: { xs: 2.5, md: 3.5 },
          borderRadius: 4,
          background: 'linear-gradient(135deg, rgba(15, 23, 42, 0.94) 0%, rgba(30, 41, 59, 0.92) 100%)',
          backdropFilter: 'blur(20px)',
          border: '1px solid rgba(255, 255, 255, 0.12)',
          position: 'relative',
          overflow: 'hidden',
          boxShadow: '0 12px 40px rgba(0, 0, 0, 0.25)',
          color: '#ffffff',
          transition: 'box-shadow 0.3s ease, border-color 0.3s ease',
          '&:hover': {
            boxShadow: '0 16px 50px rgba(34, 197, 94, 0.2)',
            borderColor: 'rgba(34, 197, 94, 0.4)',
          },
          '&::before': {
            content: '""',
            position: 'absolute',
            top: 0,
            left: 0,
            right: 0,
            height: '3px',
            background: 'linear-gradient(90deg, #16a34a, #4ade80, #06b6d4, #f97316, #16a34a)',
            backgroundSize: '200% 100%',
            animation: 'shimmerFlow 3.5s linear infinite',
            zIndex: 2,
          },
        }}
      >
        {/* Three.js 3D Background Canvas Layer inside Hero Card */}
        <Box
          sx={{
            position: 'absolute',
            top: -40,
            right: -60,
            width: { xs: '100%', sm: 480 },
            height: 280,
            opacity: 0.75,
            pointerEvents: 'none',
            zIndex: 0,
          }}
        >
          <ThreeBackgroundCanvas height="100%" interactive={true} />
        </Box>

        {/* Content Container on Top of 3D Canvas */}
        <Box sx={{ position: 'relative', zIndex: 1, display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: 2 }}>
          {/* Title, Logo Avatar & Timestamp */}
          <Box sx={{ maxWidth: { xs: '100%', md: '65%' } }}>
            <Stack direction="row" spacing={2} alignItems="center" sx={{ mb: 1 }}>
              <Box
                component="img"
                src={logoImg}
                alt="DocSpring Logo"
                sx={{
                  width: 48,
                  height: 48,
                  borderRadius: '50%',
                  objectFit: 'cover',
                  border: '2px solid #22c55e',
                  boxShadow: '0 0 16px rgba(34, 197, 94, 0.5)',
                }}
              />
              <Typography
                variant="h4"
                sx={{
                  fontSize: { xs: '1.4rem', md: '1.75rem' },
                  fontWeight: 900,
                  letterSpacing: '-0.02em',
                  background: 'linear-gradient(135deg, #ffffff 0%, #4ade80 60%, #06b6d4 100%)',
                  WebkitBackgroundClip: 'text',
                  WebkitTextFillColor: 'transparent',
                }}
              >
                {title}
              </Typography>
            </Stack>

            <Typography
              variant="caption"
              sx={{ display: 'flex', alignItems: 'center', gap: 0.8, color: '#94a3b8', mt: 1, fontWeight: 600, fontSize: '0.82rem' }}
            >
              <AccessTimeIcon fontSize="inherit" sx={{ color: '#f97316' }} />
              <b style={{ color: '#38bdf8' }}>{getGreeting()}</b> &bull; {updatedAt ? new Date(updatedAt).toLocaleString() : 'Just now'}
            </Typography>
          </Box>

          {/* Azure AI Model & Chunks Badges */}
          <Stack direction="row" spacing={1.5} alignItems="center" flexWrap="wrap" sx={{ zIndex: 2 }}>
            {/* Chat Model Chip */}
            <Tooltip title="Azure AI Foundry Chat Deployment">
              <Box
                sx={{
                  display: 'inline-flex',
                  alignItems: 'center',
                  gap: 1,
                  px: 1.8,
                  py: 0.8,
                  backgroundColor: 'rgba(34, 197, 94, 0.15)',
                  border: '1px solid rgba(34, 197, 94, 0.4)',
                  borderRadius: '20px',
                  fontSize: '0.78rem',
                  fontWeight: 700,
                  color: '#4ade80',
                  boxShadow: '0 2px 10px rgba(34, 197, 94, 0.2)',
                }}
              >
                <Box sx={{ width: 8, height: 8, borderRadius: '50%', backgroundColor: '#22c55e', boxShadow: '0 0 8px #22c55e' }} />
                <span>{chatModel || 'gpt-4.1-mini'}</span>
              </Box>
            </Tooltip>

            {/* Chunks Badge */}
            <Tooltip title="Total Vector Indexed Chunks in Session">
              <Box
                sx={{
                  display: 'inline-flex',
                  alignItems: 'center',
                  gap: 0.8,
                  px: 1.8,
                  py: 0.8,
                  backgroundColor: 'rgba(249, 115, 22, 0.15)',
                  border: '1px solid rgba(249, 115, 22, 0.4)',
                  borderRadius: '20px',
                  fontSize: '0.78rem',
                  fontWeight: 700,
                  color: '#fb923c',
                }}
              >
                <LayersIcon style={{ fontSize: 15 }} />
                <span>{chunkCount} Chunks</span>
              </Box>
            </Tooltip>

            {/* Delete Session Action */}
            {onDelete && (
              <Tooltip title="Delete Chat Session">
                <Button
                  size="small"
                  onClick={onDelete}
                  startIcon={<DeleteIcon fontSize="small" />}
                  sx={{
                    color: '#f87171',
                    borderColor: 'rgba(248, 113, 113, 0.3)',
                    backgroundColor: 'rgba(239, 68, 68, 0.1)',
                    borderRadius: '20px',
                    px: 1.5,
                    py: 0.7,
                    fontWeight: 700,
                    fontSize: '0.75rem',
                    '&:hover': {
                      backgroundColor: 'rgba(239, 68, 68, 0.25)',
                      borderColor: '#f87171',
                    },
                  }}
                >
                  Delete
                </Button>
              </Tooltip>
            )}
          </Stack>
        </Box>
      </Paper>
    </Box>
  );
}
