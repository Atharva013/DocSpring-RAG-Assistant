import React, { useState, useRef } from 'react';
import {
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Box,
  Typography,
  LinearProgress,
  Alert,
  Chip,
} from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import PictureAsPdfIcon from '@mui/icons-material/PictureAsPdf';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';

/**
 * UploadPanel component for PDF drag-and-drop file upload.
 * Uses useRef for 100% reliable file selection clicks and HTML5 Drag & Drop.
 */
export default function UploadPanel({ onUpload, isUploading, uploadStatus }) {
  const [selectedFile, setSelectedFile] = useState(null);
  const [isDragging, setIsDragging] = useState(false);
  const fileInputRef = useRef(null);

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0];
      setSelectedFile(file);
      onUpload(file);
    }
  };

  const handleBoxClick = () => {
    if (fileInputRef.current) {
      fileInputRef.current.value = null;
      fileInputRef.current.click();
    }
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const file = e.dataTransfer.files[0];
      if (file.type === 'application/pdf' || file.name.endsWith('.pdf')) {
        setSelectedFile(file);
        onUpload(file);
      } else {
        alert('Please drop a valid PDF file.');
      }
    }
  };

  return (
    <Accordion
      defaultExpanded
      sx={{
        mb: 2.5,
        borderRadius: '20px !important',
        border: '1px solid rgba(34, 197, 94, 0.2)',
        boxShadow: '0 4px 20px rgba(0, 0, 0, 0.03)',
        overflow: 'hidden',
        background: '#ffffff',
        '&::before': { display: 'none' },
      }}
    >
      <AccordionSummary expandIcon={<ExpandMoreIcon sx={{ color: '#16a34a' }} />} sx={{ backgroundColor: '#ffffff', px: 2.5, py: 0.5 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1.5 }}>
          <Box
            sx={{
              width: 32,
              height: 32,
              borderRadius: '10px',
              background: 'linear-gradient(135deg, #22c55e 0%, #16a34a 100%)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              color: '#ffffff',
              boxShadow: '0 3px 10px rgba(22, 163, 74, 0.3)',
            }}
          >
            <CloudUploadIcon sx={{ fontSize: 18 }} />
          </Box>
          <Typography variant="h6" sx={{ fontSize: '1.02rem', color: '#0f172a', fontWeight: 800 }}>
            Upload PDF Documents
          </Typography>
        </Box>
      </AccordionSummary>

      <AccordionDetails sx={{ p: 2.5, pt: 0 }}>
        {/* Hidden File Input */}
        <input
          ref={fileInputRef}
          type="file"
          accept=".pdf"
          style={{ display: 'none' }}
          onChange={handleFileChange}
        />

        {/* Dropzone Box */}
        <Box
          onClick={handleBoxClick}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
          sx={{
            p: 3.5,
            borderRadius: 4,
            border: isDragging ? '2px dashed #22c55e' : '2px dashed #86efac',
            backgroundColor: isDragging ? 'rgba(220, 252, 231, 0.8)' : '#f0fdf4',
            background: isDragging
              ? 'rgba(220, 252, 231, 0.8)'
              : 'linear-gradient(135deg, rgba(240, 253, 244, 0.8) 0%, rgba(255, 255, 255, 0.95) 100%)',
            textAlign: 'center',
            cursor: 'pointer',
            transition: 'all 0.22s cubic-bezier(0.4, 0, 0.2, 1)',
            boxShadow: isDragging ? '0 0 0 5px rgba(34, 197, 94, 0.2)' : '0 2px 10px rgba(22, 163, 74, 0.05)',
            '&:hover': {
              borderColor: '#16a34a',
              transform: 'translateY(-2px)',
              boxShadow: '0 6px 20px rgba(22, 163, 74, 0.12)',
            },
          }}
        >
          <PictureAsPdfIcon sx={{ fontSize: 44, color: '#16a34a', mb: 1 }} />

          <Typography variant="body1" sx={{ fontWeight: 800, color: '#14532d', fontSize: '1.05rem' }}>
            {selectedFile ? selectedFile.name : 'Click to Upload or Drag & Drop PDF here'}
          </Typography>

          <Typography variant="caption" sx={{ color: '#166534', display: 'block', mt: 0.5, fontWeight: 600 }}>
            Supports PDF files up to 20MB
          </Typography>

          <Chip
            label=" Azure AI Search RAG Vector Indexing"
            size="small"
            sx={{
              mt: 1.5,
              backgroundColor: '#dcfce7',
              color: '#15803d',
              fontWeight: 700,
              fontSize: '0.72rem',
              border: '1px solid #bbf7d0',
            }}
          />
        </Box>

        {/* Progress bar */}
        {isUploading && (
          <Box sx={{ mt: 2 }}>
            <LinearProgress color="primary" sx={{ height: 6, borderRadius: 3 }} />
            <Typography variant="caption" sx={{ color: '#16a34a', mt: 0.8, display: 'block', textAlign: 'center', fontWeight: 700 }}>
              Parsing PDF text & generating 1536-dim vectors...
            </Typography>
          </Box>
        )}

        {/* Upload status message */}
        {uploadStatus && (
          <Alert
            severity={uploadStatus.type}
            icon={<CheckCircleIcon fontSize="inherit" />}
            sx={{ mt: 2, borderRadius: 3, fontWeight: 600 }}
          >
            {uploadStatus.message}
          </Alert>
        )}
      </AccordionDetails>
    </Accordion>
  );
}
