import React from 'react';
import { Paper, Box, Typography, Chip, Stack } from '@mui/material';
import FolderIcon from '@mui/icons-material/Folder';
import PictureAsPdfIcon from '@mui/icons-material/PictureAsPdf';

/**
 * DocumentsPanel component displaying the list of indexed PDFs for the active session.
 */
export default function DocumentsPanel({ documents = [] }) {
  if (documents.length === 0) return null;

  return (
    <Paper
      elevation={0}
      sx={{
        p: 2,
        px: 2.5,
        mb: 2,
        borderRadius: 3,
        backgroundColor: '#ffffff',
        border: '1px solid #e2e8f0',
      }}
    >
      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 1.5 }}>
        <FolderIcon sx={{ color: '#ea580c', fontSize: 20 }} />
        <Typography variant="subtitle2" sx={{ fontWeight: 700, color: '#0f172a' }}>
          INDEXED DOCUMENTS ({documents.length})
        </Typography>
      </Box>

      <Stack direction="row" spacing={1} flexWrap="wrap" useFlexGap>
        {documents.map((doc) => (
          <Chip
            key={doc.document_id || doc.filename}
            icon={<PictureAsPdfIcon style={{ fontSize: 16, color: '#dc2626' }} />}
            label={`${doc.filename} · ${doc.chunks_indexed || 0} chunks`}
            variant="outlined"
            sx={{
              backgroundColor: '#fef2f2',
              borderColor: '#fecaca',
              color: '#991b1b',
              fontWeight: 600,
              fontSize: '0.8rem',
              py: 0.5,
            }}
          />
        ))}
      </Stack>
    </Paper>
  );
}
