import React from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogContentText,
  DialogActions,
  Button,
  CircularProgress,
} from '@mui/material';

/**
 * DeleteDialog component for session deletion confirmation with loading state.
 */
export default function DeleteDialog({ open, sessionTitle, isDeleting, onClose, onConfirm }) {
  return (
    <Dialog
      open={open}
      onClose={isDeleting ? undefined : onClose}
      PaperProps={{
        sx: {
          borderRadius: 4,
          p: 1,
          maxWidth: 420,
        },
      }}
    >
      <DialogTitle sx={{ fontWeight: 800, color: '#991b1b' }}>
        Delete Chat Session?
      </DialogTitle>
      <DialogContent>
        <DialogContentText sx={{ color: '#475569', fontSize: '0.95rem' }}>
          Are you sure you want to delete <b>"{sessionTitle || 'New chat'}"</b>?
          This will permanently remove all uploaded documents, vectors, and conversation history.
        </DialogContentText>
      </DialogContent>
      <DialogActions sx={{ p: 2, pt: 0 }}>
        <Button onClick={onClose} disabled={isDeleting} variant="outlined" color="inherit" sx={{ borderRadius: 2 }}>
          Cancel
        </Button>
        <Button
          onClick={onConfirm}
          disabled={isDeleting}
          variant="contained"
          color="error"
          startIcon={isDeleting ? <CircularProgress size={16} color="inherit" /> : null}
          sx={{ borderRadius: 2, fontWeight: 700 }}
        >
          {isDeleting ? 'Deleting Session...' : 'Delete Session'}
        </Button>
      </DialogActions>
    </Dialog>
  );
}
