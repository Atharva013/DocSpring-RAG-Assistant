import React from 'react';
import {
  Drawer,
  Box,
  Typography,
  Button,
  List,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  IconButton,
  Divider,
} from '@mui/material';
import AddIcon from '@mui/icons-material/Add';
import ChatBubbleIcon from '@mui/icons-material/ChatBubble';
import DeleteIcon from '@mui/icons-material/Delete';
import AutoAwesomeIcon from '@mui/icons-material/AutoAwesome';

const DRAWER_WIDTH = 280;

/**
 * Sidebar component for session management.
 * MUI Components Used:
 * - Drawer: https://mui.com/material-ui/react-drawer/
 * - List, ListItemButton, ListItemIcon, ListItemText: https://mui.com/material-ui/react-list/
 * - Button: https://mui.com/material-ui/react-button/
 */
export default function Sidebar({
  sessions = [],
  activeSessionId,
  onSelectSession,
  onNewChat,
  onDeleteSession,
}) {
  return (
    <Drawer
      variant="permanent"
      sx={{
        width: DRAWER_WIDTH,
        flexShrink: 0,
        '& .MuiDrawer-paper': {
          width: DRAWER_WIDTH,
          boxSizing: 'border-box',
          backgroundColor: '#0f172a',
          color: '#f8fafc',
          borderRight: '1px solid #1e293b',
        },
      }}
    >
      {/* App Branding Header */}
      <Box sx={{ p: 2.5, display: 'flex', alignItems: 'center', gap: 1.5 }}>
        <Box
          sx={{
            width: 38,
            height: 38,
            borderRadius: 2.5,
            background: 'linear-gradient(135deg, #22c55e 0%, #16a34a 100%)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            color: '#fff',
            boxShadow: '0 4px 14px rgba(22, 163, 74, 0.4)',
            animation: 'pulseGlow 3.5s infinite ease-in-out',
          }}
        >
          <AutoAwesomeIcon fontSize="small" />
        </Box>
        <Box>
          <Typography variant="h6" sx={{ color: '#ffffff', fontSize: '1.05rem', fontWeight: 800, letterSpacing: '-0.01em' }}>
            DocSpring AI
          </Typography>
          <Typography variant="caption" sx={{ color: '#94a3b8', fontSize: '0.72rem', fontWeight: 600 }}>
            Multi-PDF RAG Assistant
          </Typography>
        </Box>
      </Box>

      {/* New Chat Button */}
      <Box sx={{ px: 2, mb: 2 }}>
        <Button
          fullWidth
          variant="contained"
          color="primary"
          startIcon={<AddIcon />}
          onClick={onNewChat}
          sx={{
            py: 1.3,
            fontWeight: 700,
            borderRadius: 3,
            backgroundColor: '#16a34a',
            boxShadow: '0 4px 14px rgba(22, 163, 74, 0.35)',
            transition: 'all 0.22s cubic-bezier(0.4, 0, 0.2, 1)',
            '&:hover': {
              backgroundColor: '#15803d',
              transform: 'translateY(-2px) scale(1.01)',
              boxShadow: '0 6px 20px rgba(22, 163, 74, 0.5)',
            },
            '&:active': {
              transform: 'translateY(0) scale(0.99)',
            },
          }}
        >
          New Chat
        </Button>
      </Box>

      <Divider sx={{ borderColor: '#1e293b', mb: 1 }} />

      {/* Sessions List */}
      <Box sx={{ overflowY: 'auto', flex: 1, px: 1.5 }}>
        <Typography
          variant="caption"
          sx={{ px: 1.5, py: 1, display: 'block', color: '#64748b', fontWeight: 700, letterSpacing: '0.06em' }}
        >
          RECENT CHATS
        </Typography>

        <List disablePadding>
          {sessions.map((session, index) => {
            const isSelected = session.session_id === activeSessionId;
            return (
              <ListItemButton
                key={session.session_id}
                selected={isSelected}
                onClick={() => onSelectSession(session.session_id)}
                sx={{
                  borderRadius: 2.5,
                  mb: 0.8,
                  py: 1,
                  px: 1.5,
                  color: isSelected ? '#ffffff' : '#cbd5e1',
                  backgroundColor: isSelected ? 'rgba(22, 163, 74, 0.22)' : 'transparent',
                  border: isSelected ? '1px solid rgba(34, 197, 94, 0.4)' : '1px solid transparent',
                  boxShadow: isSelected ? '0 4px 12px rgba(22, 163, 74, 0.15)' : 'none',
                  animation: `slideInLeft 0.35s ease-out forwards`,
                  animationDelay: `${Math.min(index * 0.04, 0.4)}s`,
                  transition: 'all 0.2s cubic-bezier(0.4, 0, 0.2, 1)',
                  '&:hover': {
                    backgroundColor: isSelected ? 'rgba(22, 163, 74, 0.3)' : '#1e293b',
                    transform: 'translateX(4px)',
                    borderColor: isSelected ? 'rgba(34, 197, 94, 0.5)' : '#334155',
                  },
                }}
              >
                <ListItemIcon sx={{ minWidth: 30, color: isSelected ? '#4ade80' : '#64748b', transition: 'color 0.2s ease' }}>
                  <ChatBubbleIcon fontSize="small" />
                </ListItemIcon>

                <ListItemText
                  primary={session.title || 'New chat'}
                  primaryTypographyProps={{
                    fontSize: '0.85rem',
                    fontWeight: isSelected ? 700 : 500,
                    noWrap: true,
                  }}
                />

                <IconButton
                  size="small"
                  onClick={(e) => {
                    e.stopPropagation();
                    onDeleteSession(session);
                  }}
                  sx={{
                    color: '#64748b',
                    opacity: 0.6,
                    transition: 'all 0.2s ease',
                    '&:hover': {
                      color: '#ef4444',
                      opacity: 1,
                      backgroundColor: 'rgba(239, 68, 68, 0.15)',
                      transform: 'rotate(12deg) scale(1.15)',
                    },
                  }}
                >
                  <DeleteIcon fontSize="small" />
                </IconButton>
              </ListItemButton>
            );
          })}
        </List>
      </Box>
    </Drawer>
  );
}
