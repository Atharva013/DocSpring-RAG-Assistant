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
  Chip,
  Tooltip,
} from '@mui/material';
import AddIcon from '@mui/icons-material/Add';
import ChatBubbleIcon from '@mui/icons-material/ChatBubble';
import DeleteIcon from '@mui/icons-material/Delete';
import ChevronLeftIcon from '@mui/icons-material/ChevronLeft';
import DescriptionIcon from '@mui/icons-material/Description';
import AutoAwesomeIcon from '@mui/icons-material/AutoAwesome';
import logoImg from '../assets/logo.avif';

const DRAWER_WIDTH = 300;

/**
 * Claude-Inspired Minimalist Sidebar component.
 * Features full smooth 0px collapse, warm charcoal aesthetic, logo integration,
 * document count chips, and clean session history items. Footer removed as requested.
 */
export default function Sidebar({
  isOpen = true,
  onToggleSidebar,
  sessions = [],
  activeSessionId,
  onSelectSession,
  onNewChat,
  onDeleteSession,
}) {
  return (
    <Drawer
      variant="persistent"
      anchor="left"
      open={isOpen}
      sx={{
        width: isOpen ? DRAWER_WIDTH : 0,
        flexShrink: 0,
        transition: 'width 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
        '& .MuiDrawer-paper': {
          width: DRAWER_WIDTH,
          boxSizing: 'border-box',
          backgroundColor: '#161618',
          backdropFilter: 'blur(20px)',
          color: '#e4e4e7',
          borderRight: '1px solid rgba(255, 255, 255, 0.07)',
          boxShadow: '6px 0 30px rgba(0, 0, 0, 0.35)',
          transition: 'transform 0.3s cubic-bezier(0.4, 0, 0.2, 1), width 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
          overflowX: 'hidden',
          display: 'flex',
          flexDirection: 'column',
        },
      }}
    >
      {/* App Branding Header & Collapse Trigger */}
      <Box
        sx={{
          p: 2.2,
          px: 2.5,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
        }}
      >
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1.6 }}>
          {/* Logo Frame */}
          <Box
            sx={{
              width: 38,
              height: 38,
              borderRadius: '50%',
              overflow: 'hidden',
              p: '2px',
              background: 'linear-gradient(135deg, #10b981 0%, #06b6d4 100%)',
              boxShadow: '0 0 14px rgba(16, 185, 129, 0.35)',
              flexShrink: 0,
            }}
          >
            <Box
              component="img"
              src={logoImg}
              alt="DocSpring Logo"
              sx={{
                width: '100%',
                height: '100%',
                borderRadius: '50%',
                objectFit: 'cover',
                backgroundColor: '#161618',
              }}
            />
          </Box>

          <Box>
            <Typography
              variant="h6"
              sx={{
                color: '#f4f4f5',
                fontSize: '1.05rem',
                fontWeight: 800,
                letterSpacing: '-0.02em',
                fontFamily: 'Inter, sans-serif',
              }}
            >
              DocSpring AI
            </Typography>
            <Typography
              variant="caption"
              sx={{
                color: '#34d399',
                fontSize: '0.72rem',
                fontWeight: 600,
                display: 'flex',
                alignItems: 'center',
                gap: 0.5,
              }}
            >
              <AutoAwesomeIcon sx={{ fontSize: 11 }} /> Multi-PDF RAG Engine
            </Typography>
          </Box>
        </Box>

        {/* Sidebar Close Button */}
        <Tooltip title="Close Sidebar">
          <IconButton
            onClick={onToggleSidebar}
            sx={{
              color: '#a1a1aa',
              p: 0.8,
              borderRadius: '10px',
              '&:hover': { color: '#ffffff', backgroundColor: 'rgba(255, 255, 255, 0.08)' },
            }}
          >
            <ChevronLeftIcon fontSize="small" />
          </IconButton>
        </Tooltip>
      </Box>

      {/* New Chat Button */}
      <Box sx={{ px: 2, mb: 2, mt: 0.5 }}>
        <Button
          fullWidth
          variant="contained"
          startIcon={<AddIcon />}
          onClick={onNewChat}
          sx={{
            py: 1.2,
            fontWeight: 700,
            fontSize: '0.88rem',
            borderRadius: '14px',
            backgroundColor: '#27272a',
            color: '#f4f4f5',
            border: '1px solid rgba(255, 255, 255, 0.1)',
            boxShadow: '0 2px 10px rgba(0, 0, 0, 0.2)',
            textTransform: 'none',
            transition: 'all 0.2s ease',
            '&:hover': {
              backgroundColor: '#3f3f46',
              borderColor: '#10b981',
              color: '#ffffff',
              transform: 'translateY(-1px)',
              boxShadow: '0 4px 16px rgba(16, 185, 129, 0.2)',
            },
          }}
        >
          New Chat
        </Button>
      </Box>

      <Divider sx={{ borderColor: 'rgba(255, 255, 255, 0.06)', mb: 1.5 }} />

      {/* Sessions List */}
      <Box sx={{ overflowY: 'auto', flex: 1, px: 1.5, pb: 2 }}>
        <Typography
          variant="caption"
          sx={{
            px: 1.5,
            py: 0.8,
            display: 'block',
            color: '#71717a',
            fontWeight: 700,
            letterSpacing: '0.06em',
            fontSize: '0.68rem',
          }}
        >
          RECENT CHATS ({sessions.length})
        </Typography>

        <List disablePadding>
          {sessions.map((session) => {
            const isSelected = session.session_id === activeSessionId;
            const docCount = session.document_count || 0;

            return (
              <ListItemButton
                key={session.session_id}
                selected={isSelected}
                onClick={() => onSelectSession(session.session_id)}
                sx={{
                  borderRadius: '12px',
                  mb: 0.8,
                  py: 1,
                  px: 1.5,
                  color: isSelected ? '#ffffff' : '#a1a1aa',
                  backgroundColor: isSelected ? 'rgba(255, 255, 255, 0.08)' : 'transparent',
                  border: isSelected ? '1px solid rgba(255, 255, 255, 0.12)' : '1px solid transparent',
                  transition: 'all 0.2s ease',
                  '&:hover': {
                    backgroundColor: isSelected ? 'rgba(255, 255, 255, 0.12)' : 'rgba(255, 255, 255, 0.04)',
                    color: '#ffffff',
                    transform: 'translateX(3px)',
                  },
                }}
              >
                <ListItemIcon sx={{ minWidth: 28, color: isSelected ? '#34d399' : '#71717a' }}>
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

                {docCount > 0 && (
                  <Chip
                    icon={<DescriptionIcon style={{ fontSize: 10, color: isSelected ? '#34d399' : '#a1a1aa' }} />}
                    label={docCount}
                    size="small"
                    sx={{
                      height: 18,
                      fontSize: '0.65rem',
                      fontWeight: 700,
                      backgroundColor: isSelected ? 'rgba(52, 211, 153, 0.2)' : 'rgba(255, 255, 255, 0.06)',
                      color: isSelected ? '#34d399' : '#a1a1aa',
                      mr: 0.5,
                    }}
                  />
                )}

                <IconButton
                  size="small"
                  onClick={(e) => {
                    e.stopPropagation();
                    onDeleteSession(session);
                  }}
                  sx={{
                    color: '#71717a',
                    opacity: 0.4,
                    p: 0.5,
                    transition: 'all 0.2s ease',
                    '&:hover': {
                      color: '#f87171',
                      opacity: 1,
                      backgroundColor: 'rgba(248, 113, 113, 0.15)',
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
