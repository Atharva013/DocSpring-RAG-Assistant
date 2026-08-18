import React from 'react';
import { Paper, Box, Typography, Chip, Stack, Button } from '@mui/material';
import ChatIcon from '@mui/icons-material/Chat';
import AccessTimeIcon from '@mui/icons-material/AccessTime';
import LayersIcon from '@mui/icons-material/Layers';
import DeleteIcon from '@mui/icons-material/Delete';

const getGreeting = () => {
  const hour = new Date().getHours();
  if (hour < 12) return 'Good morning ☀️';
  if (hour < 17) return 'Good afternoon 🌤️';
  return 'Good evening 🌙';
};

/**
 * HeroHeader component displaying session title, dynamic time greeting, and model badges.
 */
export default function HeroHeader({
  title = 'New chat',
  updatedAt,
  chunkCount = 0,
  chatModel = '—',
  embedModel = '—',
  onDelete,
}) {
  return (
    <Box sx={{ mb: 2.5, animation: 'fadeInScale 0.4s ease-out forwards' }}>
      <Paper
        elevation={0}
        sx={{
          p: 3,
          borderRadius: 4,
          background: 'linear-gradient(135deg, rgba(22, 163, 74, 0.08) 0%, rgba(255, 255, 255, 0.95) 40%, rgba(249, 115, 22, 0.06) 100%)',
          border: '1px solid #e2e8f0',
          position: 'relative',
          overflow: 'hidden',
          boxShadow: '0 4px 20px rgba(0, 0, 0, 0.03)',
          transition: 'box-shadow 0.3s ease, border-color 0.3s ease',
          '&:hover': {
            boxShadow: '0 8px 30px rgba(22, 163, 74, 0.1)',
            borderColor: '#cbd5e1',
          },
          '&::before': {
            content: '""',
            position: 'absolute',
            top: 0,
            left: 0,
            right: 0,
            height: '3px',
            background: 'linear-gradient(90deg, #16a34a, #4ade80, #f97316, #16a34a)',
            backgroundSize: '200% 100%',
            animation: 'shimmerFlow 3.5s linear infinite',
          },
        }}
      >
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: 2 }}>
          {/* Title, Greeting and Timestamp */}
          <Box>
            <Typography
              variant="h5"
              sx={{
                display: 'flex',
                alignItems: 'center',
                gap: 1.5,
                color: '#0f172a',
                fontWeight: 900,
              }}
            >
              <ChatIcon sx={{ color: '#16a34a', transition: 'transform 0.2s ease', '&:hover': { transform: 'rotate(15deg) scale(1.1)' } }} />
              <span style={{ background: 'linear-gradient(135deg, #16a34a 0%, #059669 50%, #f97316 100%)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>
                {title}
              </span>
            </Typography>

            <Typography
              variant="caption"
              sx={{ display: 'flex', alignItems: 'center', gap: 0.5, color: '#64748b', mt: 1, fontWeight: 600, fontSize: '0.82rem' }}
            >
              <AccessTimeIcon fontSize="inherit" sx={{ color: '#ea580c' }} />
              <b>{getGreeting()}</b> &bull; {updatedAt ? new Date(updatedAt).toLocaleString() : 'Just now'}
            </Typography>
          </Box>

          {/* Model Info & Chunks Badges */}
          <Stack direction="row" spacing={1.5} alignItems="center" flexWrap="wrap">
            {/* Model Info Chip */}
            <Box
              sx={{
                display: 'inline-flex',
                alignItems: 'center',
                gap: 1,
                px: 1.5,
                py: 0.7,
                backgroundColor: '#f0fdf4',
                border: '1px solid #d1fae5',
                borderRadius: '20px',
                fontSize: '0.78rem',
                transition: 'all 0.2s ease',
                '&:hover': {
                  backgroundColor: '#dcfce7',
                  transform: 'scale(1.04)',
                },
              }}
            >
              <Box
                sx={{
                  width: 7,
                  height: 7,
                  borderRadius: '50%',
                  backgroundColor: '#22c55e',
                  boxShadow: '0 0 6px rgba(34, 197, 94, 0.8)',
                  animation: 'pulseGlow 2s infinite ease-in-out',
                }}
              />
              <Typography variant="caption" sx={{ color: '#52796f', fontWeight: 600 }}>
                Chat:
              </Typography>
              <Chip
                label={chatModel}
                size="small"
                sx={{ height: 20, fontSize: '0.72rem', fontWeight: 700, backgroundColor: '#dcfce7', color: '#15803d' }}
              />
              <Typography variant="caption" sx={{ color: '#52796f', fontWeight: 600 }}>
                Embed:
              </Typography>
              <Chip
                label={embedModel}
                size="small"
                sx={{ height: 20, fontSize: '0.72rem', fontWeight: 700, backgroundColor: '#dcfce7', color: '#15803d' }}
              />
            </Box>

            {/* Chunks Indexed Badge */}
            <Chip
              icon={<LayersIcon style={{ fontSize: 14, color: '#16a34a' }} />}
              label={`${chunkCount} chunks indexed`}
              variant="outlined"
              sx={{
                borderColor: '#bbf7d0',
                backgroundColor: '#f0fdf4',
                color: '#15803d',
                fontWeight: 700,
                fontSize: '0.78rem',
                transition: 'all 0.2s ease',
                '&:hover': {
                  backgroundColor: '#dcfce7',
                  transform: 'scale(1.04)',
                  borderColor: '#86efac',
                },
              }}
            />
          </Stack>
        </Box>
      </Paper>

      {/* Delete Button */}
      <Box sx={{ display: 'flex', justifyContent: 'flex-end', mt: 1 }}>
        <Button
          size="small"
          variant="outlined"
          color="error"
          startIcon={<DeleteIcon />}
          onClick={onDelete}
          sx={{
            borderRadius: 2.5,
            fontWeight: 700,
            backgroundColor: '#fee2e2',
            borderColor: '#fca5a5',
            color: '#b91c1c',
            transition: 'all 0.2s ease',
            '&:hover': {
              backgroundColor: '#fecaca',
              borderColor: '#ef4444',
              transform: 'scale(1.03)',
            },
          }}
        >
          Delete Chat
        </Button>
      </Box>
    </Box>
  );
}
