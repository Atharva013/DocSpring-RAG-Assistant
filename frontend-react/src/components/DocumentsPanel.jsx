import React from 'react';
import { Paper, Box, Typography, Chip, Stack } from '@mui/material';
import FolderIcon from '@mui/icons-material/Folder';
import PictureAsPdfIcon from '@mui/icons-material/PictureAsPdf';

/**
 * DocumentsPanel component displaying the list of indexed PDFs in warm dark glass card style.
 */
export default function DocumentsPanel({ documents = [] }) {
  if (documents.length === 0) return null;

  return (
    <Paper
      elevation={0}
      sx={{
        p: 2,
        px: 2.8,
        mb: 2.5,
        borderRadius: '18px',
        backgroundColor: 'rgba(24, 24, 27, 0.75)',
        backdropFilter: 'blur(20px)',
        border: '1px solid rgba(255, 255, 255, 0.08)',
        boxShadow: '0 4px 20px rgba(0, 0, 0, 0.2)',
      }}
    >
      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 1.5 }}>
        <FolderIcon sx={{ color: '#fb923c', fontSize: 20 }} />
        <Typography variant="subtitle2" sx={{ fontWeight: 800, color: '#f4f4f5', letterSpacing: '0.04em', fontSize: '0.78rem' }}>
          INDEXED DOCUMENTS ({documents.length})
        </Typography>
      </Box>

      <Stack direction="row" spacing={1.2} flexWrap="wrap" useFlexGap>
        {documents.map((doc) => (
          <Chip
            key={doc.document_id || doc.filename}
            icon={<PictureAsPdfIcon style={{ fontSize: 16, color: '#f87171' }} />}
            label={`${doc.filename} · ${doc.chunks_indexed || 0} chunks`}
            variant="outlined"
            sx={{
              backgroundColor: 'rgba(239, 68, 68, 0.1)',
              borderColor: 'rgba(239, 68, 68, 0.25)',
              color: '#fca5a5',
              fontWeight: 600,
              fontSize: '0.8rem',
              py: 0.5,
              borderRadius: '12px',
              transition: 'all 0.2s ease',
              '&:hover': {
                backgroundColor: 'rgba(239, 68, 68, 0.18)',
                borderColor: 'rgba(239, 68, 68, 0.4)',
              },
            }}
          />
        ))}
      </Stack>
    </Paper>
  );
}
