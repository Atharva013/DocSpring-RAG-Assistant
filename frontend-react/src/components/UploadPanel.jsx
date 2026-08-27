import React, { useState, useRef, useEffect } from 'react';
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
 * Handles HTML5 Drag & Drop and standard click file selection smoothly.
 */
export default function UploadPanel({ onUpload, isUploading, uploadStatus }) {
  const [selectedFile, setSelectedFile] = useState(null);
  const [isDragging, setIsDragging] = useState(false);
  const fileInputRef = useRef(null);

  // Clear selected file when switching sessions or starting a new chat
  useEffect(() => {
    if (!uploadStatus) {
      setSelectedFile(null);
    }
  }, [uploadStatus]);

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

  const handleDragEnter = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(true);
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    e.stopPropagation();
    e.dataTransfer.dropEffect = 'copy';
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

    const files = e.dataTransfer ? e.dataTransfer.files : null;
    if (files && files.length > 0) {
      const file = files[0];
      const isPdf = file.name.toLowerCase().endsWith('.pdf') || file.type === 'application/pdf';
      if (isPdf) {
        setSelectedFile(file);
        onUpload(file);
      } else {
        alert('Only PDF files are supported. Please drop a valid .pdf document.');
      }
    }
  };

  return (
    <Accordion
      defaultExpanded
      sx={{
        mb: 3,
        borderRadius: '20px !important',
        border: '1px solid rgba(255, 255, 255, 0.08)',
        boxShadow: '0 8px 32px rgba(0, 0, 0, 0.25)',
        overflow: 'hidden',
        background: 'rgba(24, 24, 27, 0.75)',
        backdropFilter: 'blur(20px)',
        color: '#f4f4f5',
        '&::before': { display: 'none' },
      }}
    >
      <AccordionSummary expandIcon={<ExpandMoreIcon sx={{ color: '#10b981' }} />} sx={{ px: 2.5, py: 0.5 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1.5 }}>
          <Box
            sx={{
              width: 32,
              height: 32,
              borderRadius: '10px',
              background: 'linear-gradient(135deg, #10b981 0%, #059669 100%)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              color: '#ffffff',
              boxShadow: '0 3px 10px rgba(16, 185, 129, 0.3)',
            }}
          >
            <CloudUploadIcon sx={{ fontSize: 18 }} />
          </Box>
          <Typography variant="h6" sx={{ fontSize: '1rem', color: '#f4f4f5', fontWeight: 800 }}>
            Upload PDF Documents
          </Typography>
        </Box>
      </AccordionSummary>

      <AccordionDetails sx={{ p: 2.5, pt: 0 }}>
        {/* Hidden File Input */}
        <input
          ref={fileInputRef}
          type="file"
          accept=".pdf,application/pdf"
          style={{ display: 'none' }}
          onChange={handleFileChange}
        />

        {/* Dropzone Box */}
        <Box
          onClick={handleBoxClick}
          onDragEnter={handleDragEnter}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
          sx={{
            p: 3.5,
            borderRadius: '16px',
            border: isDragging ? '2px dashed #10b981' : '2px dashed rgba(16, 185, 129, 0.4)',
            backgroundColor: isDragging ? 'rgba(16, 185, 129, 0.18)' : 'rgba(255, 255, 255, 0.02)',
            textAlign: 'center',
            cursor: 'pointer',
            transition: 'all 0.22s cubic-bezier(0.4, 0, 0.2, 1)',
            boxShadow: isDragging ? '0 0 24px rgba(16, 185, 129, 0.35)' : 'none',
            '&:hover': {
              borderColor: '#10b981',
              backgroundColor: 'rgba(16, 185, 129, 0.08)',
              transform: 'translateY(-2px)',
            },
          }}
        >
          <PictureAsPdfIcon sx={{ fontSize: 44, color: '#10b981', mb: 1 }} />

          <Typography variant="body1" sx={{ fontWeight: 800, color: '#ffffff', fontSize: '1.05rem' }}>
            {selectedFile ? selectedFile.name : 'Click to Upload or Drag & Drop PDF here'}
          </Typography>

          <Typography variant="caption" sx={{ color: '#a1a1aa', display: 'block', mt: 0.5, fontWeight: 500 }}>
            Supports PDF files up to 20MB
          </Typography>

          <Chip
            label="Azure AI Search RAG Vector Indexing"
            size="small"
            sx={{
              mt: 1.5,
              backgroundColor: 'rgba(16, 185, 129, 0.15)',
              color: '#34d399',
              fontWeight: 700,
              fontSize: '0.72rem',
              border: '1px solid rgba(16, 185, 129, 0.3)',
            }}
          />
        </Box>

        {/* Progress bar */}
        {isUploading && (
          <Box sx={{ mt: 2 }}>
            <LinearProgress sx={{ height: 6, borderRadius: 3, backgroundColor: 'rgba(255,255,255,0.1)', '& .MuiLinearProgress-bar': { backgroundColor: '#10b981' } }} />
            <Typography variant="caption" sx={{ color: '#34d399', mt: 0.8, display: 'block', textAlign: 'center', fontWeight: 700 }}>
              Parsing PDF text & generating 1536-dim vectors...
            </Typography>
          </Box>
        )}

        {/* Upload status message */}
        {uploadStatus && (
          <Alert
            severity={uploadStatus.type}
            icon={<CheckCircleIcon fontSize="inherit" />}
            sx={{
              mt: 2,
              borderRadius: '14px',
              fontWeight: 600,
              backgroundColor: uploadStatus.type === 'success' ? 'rgba(16, 185, 129, 0.15)' : 'rgba(239, 68, 68, 0.15)',
              color: uploadStatus.type === 'success' ? '#34d399' : '#f87171',
              border: uploadStatus.type === 'success' ? '1px solid rgba(16, 185, 129, 0.3)' : '1px solid rgba(239, 68, 68, 0.3)',
            }}
          >
            {uploadStatus.message}
          </Alert>
        )}
      </AccordionDetails>
    </Accordion>
  );
}
