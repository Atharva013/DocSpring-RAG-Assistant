import React, { useState } from 'react';
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
  useMediaQuery,
  useTheme,
} from '@mui/material';
import AddIcon from '@mui/icons-material/Add';
import ChatBubbleIcon from '@mui/icons-material/ChatBubble';
import DeleteIcon from '@mui/icons-material/Delete';
import MenuOpenIcon from '@mui/icons-material/MenuOpen';
import MenuIcon from '@mui/icons-material/Menu';
import DescriptionIcon from '@mui/icons-material/Description';
import AutoAwesomeIcon from '@mui/icons-material/AutoAwesome';
import logoImg from '../assets/logo.avif';

const DRAWER_WIDTH = 300;
const COLLAPSED_WIDTH = 78;

/**
 * Glorified Sidebar component for advanced session management.
 * Incorporates the custom DocSpring logo asset, glassmorphism aesthetics,
 * collapsible state toggle, document badges, and micro-animations.
 */
export default function Sidebar({
  sessions = [],
  activeSessionId,
  onSelectSession,
  onNewChat,
  onDeleteSession,
}) {
  const [collapsed, setCollapsed] = useState(false);
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));

  const activeWidth = collapsed ? COLLAPSED_WIDTH : DRAWER_WIDTH;

  return (
    <Drawer
      variant="permanent"
      sx={{
        width: activeWidth,
        flexShrink: 0,
        transition: 'width 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
        '& .MuiDrawer-paper': {
          width: activeWidth,
          boxSizing: 'border-box',
          backgroundColor: 'rgba(15, 23, 42, 0.96)',
          backdropFilter: 'blur(16px)',
          color: '#f8fafc',
          borderRight: '1px solid rgba(255, 255, 255, 0.08)',
          boxShadow: '4px 0 25px rgba(0, 0, 0, 0.3)',
          transition: 'width 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
          overflowX: 'hidden',
        },
      }}
    >
      {/* App Branding Header */}
      <Box
        sx={{
          p: 2.5,
          display: 'flex',
          alignItems: 'center',
          justifyContent: collapsed ? 'center' : 'space-between',
          gap: 1.5,
        }}
      >
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1.8 }}>
          {/* Logo Frame featuring user's um-person logo asset */}
          <Box
            sx={{
              width: 44,
              height: 44,
              borderRadius: '50%',
              overflow: 'hidden',
              position: 'relative',
              p: '2px',
              background: 'linear-gradient(135deg, #22c55e 0%, #06b6d4 50%, #f97316 100%)',
              boxShadow: '0 0 16px rgba(34, 197, 94, 0.45)',
              animation: 'pulseGlow 4s infinite ease-in-out',
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
                backgroundColor: '#090d16',
              }}
            />
          </Box>

          {!collapsed && (
            <Box>
              <Typography
                variant="h6"
                sx={{
                  color: '#ffffff',
                  fontSize: '1.12rem',
                  fontWeight: 900,
                  letterSpacing: '-0.02em',
                  background: 'linear-gradient(135deg, #ffffff 0%, #cbd5e1 100%)',
                  WebkitBackgroundClip: 'text',
                  WebkitTextFillColor: 'transparent',
                }}
              >
                DocSpring AI
              </Typography>
              <Typography
                variant="caption"
                sx={{
                  color: '#4ade80',
                  fontSize: '0.73rem',
                  fontWeight: 700,
                  display: 'flex',
                  alignItems: 'center',
                  gap: 0.5,
                }}
              >
                <AutoAwesomeIcon sx={{ fontSize: 11 }} /> Multi-PDF RAG
              </Typography>
            </Box>
          )}
        </Box>

        {/* Sidebar Collapse Toggle Button */}
        {!isMobile && (
          <Tooltip title={collapsed ? 'Expand Sidebar' : 'Collapse Sidebar'} placement="right">
            <IconButton
              onClick={() => setCollapsed(!collapsed)}
              sx={{
                color: '#94a3b8',
                '&:hover': { color: '#ffffff', backgroundColor: 'rgba(255, 255, 255, 0.08)' },
              }}
            >
              {collapsed ? <MenuIcon fontSize="small" /> : <MenuOpenIcon fontSize="small" />}
            </IconButton>
          </Tooltip>
        )}
      </Box>

      {/* New Chat Button */}
      <Box sx={{ px: collapsed ? 1.5 : 2, mb: 2 }}>
        {collapsed ? (
          <Tooltip title="New Chat" placement="right">
            <IconButton
              onClick={onNewChat}
              sx={{
                width: '100%',
                py: 1.5,
                borderRadius: 3,
                backgroundColor: '#16a34a',
                color: '#fff',
                boxShadow: '0 4px 14px rgba(22, 163, 74, 0.4)',
                '&:hover': { backgroundColor: '#15803d', transform: 'scale(1.05)' },
              }}
            >
              <AddIcon />
            </IconButton>
          </Tooltip>
        ) : (
          <Button
            fullWidth
            variant="contained"
            color="primary"
            startIcon={<AddIcon />}
            onClick={onNewChat}
            sx={{
              py: 1.3,
              fontWeight: 800,
              fontSize: '0.9rem',
              borderRadius: 3,
              background: 'linear-gradient(135deg, #22c55e 0%, #16a34a 100%)',
              boxShadow: '0 4px 16px rgba(22, 163, 74, 0.4)',
              transition: 'all 0.22s cubic-bezier(0.4, 0, 0.2, 1)',
              '&:hover': {
                background: 'linear-gradient(135deg, #16a34a 0%, #15803d 100%)',
                transform: 'translateY(-2px)',
                boxShadow: '0 6px 22px rgba(22, 163, 74, 0.55)',
              },
            }}
          >
            New Chat
          </Button>
        )}
      </Box>

      <Divider sx={{ borderColor: 'rgba(255, 255, 255, 0.08)', mb: 1.5 }} />

      {/* Sessions List */}
      <Box sx={{ overflowY: 'auto', flex: 1, px: collapsed ? 1 : 1.5 }}>
        {!collapsed && (
          <Typography
            variant="caption"
            sx={{
              px: 1.5,
              py: 1,
              display: 'block',
              color: '#64748b',
              fontWeight: 800,
              letterSpacing: '0.08em',
              fontSize: '0.68rem',
            }}
          >
            ACTIVE SESSIONS ({sessions.length})
          </Typography>
        )}

        <List disablePadding>
          {sessions.map((session, index) => {
            const isSelected = session.session_id === activeSessionId;
            const docCount = session.document_count || 0;

            if (collapsed) {
              return (
                <Tooltip key={session.session_id} title={session.title || 'New chat'} placement="right">
                  <ListItemButton
                    selected={isSelected}
                    onClick={() => onSelectSession(session.session_id)}
                    sx={{
                      borderRadius: 2.5,
                      mb: 1,
                      justifyContent: 'center',
                      p: 1.5,
                      backgroundColor: isSelected ? 'rgba(34, 197, 94, 0.25)' : 'transparent',
                      border: isSelected ? '1px solid rgba(34, 197, 94, 0.5)' : '1px solid transparent',
                    }}
                  >
                    <ChatBubbleIcon fontSize="small" sx={{ color: isSelected ? '#4ade80' : '#64748b' }} />
                  </ListItemButton>
                </Tooltip>
              );
            }

            return (
              <ListItemButton
                key={session.session_id}
                selected={isSelected}
                onClick={() => onSelectSession(session.session_id)}
                sx={{
                  borderRadius: 2.5,
                  mb: 1,
                  py: 1.1,
                  px: 1.8,
                  color: isSelected ? '#ffffff' : '#cbd5e1',
                  backgroundColor: isSelected ? 'rgba(34, 197, 94, 0.16)' : 'rgba(255, 255, 255, 0.02)',
                  border: isSelected ? '1px solid rgba(34, 197, 94, 0.45)' : '1px solid rgba(255, 255, 255, 0.04)',
                  boxShadow: isSelected ? '0 4px 16px rgba(34, 197, 94, 0.18)' : 'none',
                  animation: `slideInLeft 0.3s ease-out forwards`,
                  animationDelay: `${Math.min(index * 0.03, 0.3)}s`,
                  transition: 'all 0.22s cubic-bezier(0.4, 0, 0.2, 1)',
                  '&:hover': {
                    backgroundColor: isSelected ? 'rgba(34, 197, 94, 0.25)' : 'rgba(255, 255, 255, 0.06)',
                    transform: 'translateX(4px)',
                    borderColor: isSelected ? 'rgba(34, 197, 94, 0.6)' : 'rgba(255, 255, 255, 0.12)',
                  },
                }}
              >
                <ListItemIcon sx={{ minWidth: 32, color: isSelected ? '#4ade80' : '#64748b' }}>
                  <ChatBubbleIcon fontSize="small" />
                </ListItemIcon>

                <ListItemText
                  primary={session.title || 'New chat'}
                  primaryTypographyProps={{
                    fontSize: '0.86rem',
                    fontWeight: isSelected ? 800 : 500,
                    noWrap: true,
                  }}
                />

                {docCount > 0 && (
                  <Chip
                    icon={<DescriptionIcon style={{ fontSize: 10, color: isSelected ? '#4ade80' : '#94a3b8' }} />}
                    label={docCount}
                    size="small"
                    sx={{
                      height: 18,
                      fontSize: '0.65rem',
                      fontWeight: 700,
                      backgroundColor: isSelected ? 'rgba(34, 197, 94, 0.3)' : 'rgba(255, 255, 255, 0.08)',
                      color: isSelected ? '#4ade80' : '#94a3b8',
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
                    color: '#64748b',
                    opacity: 0.5,
                    p: 0.5,
                    transition: 'all 0.2s ease',
                    '&:hover': {
                      color: '#ef4444',
                      opacity: 1,
                      backgroundColor: 'rgba(239, 68, 68, 0.2)',
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

      {/* Sidebar Footer User Info */}
      <Divider sx={{ borderColor: 'rgba(255, 255, 255, 0.08)' }} />
      <Box sx={{ p: 2, display: 'flex', alignItems: 'center', gap: 1.5 }}>
        <Box
          component="img"
          src={logoImg}
          alt="User Profile"
          sx={{
            width: 34,
            height: 34,
            borderRadius: '50%',
            objectFit: 'cover',
            border: '1.5px solid #22c55e',
          }}
        />
        {!collapsed && (
          <Box sx={{ minWidth: 0, flex: 1 }}>
            <Typography variant="body2" sx={{ color: '#fff', fontWeight: 700, fontSize: '0.82rem' }} noWrap>
              Enterprise User
            </Typography>
            <Typography variant="caption" sx={{ color: '#94a3b8', fontSize: '0.7rem' }} noWrap>
              Azure AI S0 Powered
            </Typography>
          </Box>
        )}
      </Box>
    </Drawer>
  );
}
