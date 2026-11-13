import React, { useState } from 'react';
import { 
  Dialog, 
  DialogTitle, 
  DialogContent, 
  DialogActions, 
  Button, 
  FormControl, 
  FormLabel, 
  RadioGroup, 
  FormControlLabel, 
  Radio, 
  Alert,
  CircularProgress,
  Box,
  Typography,
  Chip
} from '@mui/material';
import axios from 'axios';
import FileDownloadIcon from '@mui/icons-material/FileDownload';
import BusinessIcon from '@mui/icons-material/Business';
import PictureAsPdfIcon from '@mui/icons-material/PictureAsPdf';
import DescriptionIcon from '@mui/icons-material/Description';

const API_BASE_URL = 'http://127.0.0.1:8000';

export default function ExportModal({ open, onClose, requestId, isProfessional = false }) {
  const [exportFormat, setExportFormat] = useState('html');
  const [isExporting, setIsExporting] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);

  const handleExport = async () => {
    if (!requestId && isProfessional) {
      setError('No request ID available for export');
      return;
    }

    setIsExporting(true);
    setError(null);
    setSuccess(false);

    try {
      if (isProfessional) {
        // Use professional export endpoint with query parameters
        const response = await axios.post(`${API_BASE_URL}/api/export-professional-report/${requestId}?format=${exportFormat}`);
        
        // Check if export was successful
        if (response.data.success) {
          if (exportFormat === 'json') {
            // For JSON format, create and download blob directly
            const jsonData = JSON.stringify(response.data.data, null, 2);
            const blob = new Blob([jsonData], { type: 'application/json' });
            const url = window.URL.createObjectURL(blob);
            const link = document.createElement('a');
            link.href = url;
            link.download = `decision-analysis-${requestId}.json`;
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            window.URL.revokeObjectURL(url);
          } else if (response.data.download_url) {
            // For other formats, use the download URL
            const downloadUrl = `${API_BASE_URL}${response.data.download_url}`;
            window.open(downloadUrl, '_blank');
          } else {
            setError('Download link not available. Please try again.');
            setIsExporting(false);
            return;
          }
          
          setSuccess(true);
          setTimeout(() => {
            setSuccess(false);
            onClose();
          }, 2000);
          
        } else {
          setError(response.data.message || 'Export failed');
        }
      } else {
        // Fallback to basic export (to be implemented)
        setError('Standard export is not implemented yet. Use Professional Analysis mode.');
        setIsExporting(false);
        return;
      }

    } catch (err) {
      console.error('Export error:', err);
      setError(
        err.response?.data?.detail || 
        err.message || 
        'Failed to export report. Please try again.'
      );
    }

    setIsExporting(false);
  };

  const handleClose = () => {
    if (!isExporting) {
      setError(null);
      setSuccess(false);
      onClose();
    }
  };

  const getFormatIcon = (format) => {
    switch (format) {
      case 'html':
        return <DescriptionIcon />;
      case 'pdf':
        return <PictureAsPdfIcon />;
      case 'json':
        return <BusinessIcon />;
      default:
        return <FileDownloadIcon />;
    }
  };

  const getFormatDescription = (format) => {
    switch (format) {
      case 'html':
        return 'Beautiful HTML report with interactive elements and styling';
      case 'pdf':
        return 'PDF format (coming soon — use HTML for now)';
      case 'json':
        return 'Raw JSON data for integration and further analysis';
      default:
        return 'Export format';
    }
  };

  return (
    <Dialog open={open} onClose={handleClose} maxWidth="sm" fullWidth>
      <DialogTitle sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
        <FileDownloadIcon />
        {isProfessional ? 'Export Professional Report' : 'Export Decision Analysis'}
        {isProfessional && (
          <Chip 
            label="Professional" 
            color="primary" 
            size="small" 
            sx={{ ml: 1 }}
          />
        )}
      </DialogTitle>
      
      <DialogContent>
        {error && (
          <Alert severity="error" sx={{ mb: 2 }}>
            {error}
          </Alert>
        )}
        
        {success && (
          <Alert severity="success" sx={{ mb: 2 }}>
            Report exported successfully!
          </Alert>
        )}

        {isProfessional ? (
          <>
            <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
              Export your professional decision analysis in formats suitable for
              executive presentations, documentation, and further analysis.
            </Typography>

            <FormControl component="fieldset" fullWidth>
              <FormLabel component="legend" sx={{ mb: 2, fontWeight: 600 }}>
                Choose Export Format
              </FormLabel>
              <RadioGroup
                value={exportFormat}
                onChange={(e) => setExportFormat(e.target.value)}
              >
                <FormControlLabel
                  value="html"
                  control={<Radio />}
                  label={
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                      {getFormatIcon('html')}
                      <Box>
                        <Typography variant="body1" fontWeight={500}>
                          HTML Report
                        </Typography>
                        <Typography variant="body2" color="text.secondary">
                          {getFormatDescription('html')}
                        </Typography>
                      </Box>
                    </Box>
                  }
                  sx={{ mb: 2, alignItems: 'flex-start' }}
                />
                
                <FormControlLabel
                  value="pdf"
                  control={<Radio />}
                  label={
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                      {getFormatIcon('pdf')}
                      <Box>
                        <Typography variant="body1" fontWeight={500}>
                          PDF Report
                        </Typography>
                        <Typography variant="body2" color="text.secondary">
                          {getFormatDescription('pdf')}
                        </Typography>
                      </Box>
                    </Box>
                  }
                  sx={{ mb: 2, alignItems: 'flex-start' }}
                />
                
                <FormControlLabel
                  value="json"
                  control={<Radio />}
                  label={
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                      {getFormatIcon('json')}
                      <Box>
                        <Typography variant="body1" fontWeight={500}>
                          JSON Data
                        </Typography>
                        <Typography variant="body2" color="text.secondary">
                          {getFormatDescription('json')}
                        </Typography>
                      </Box>
                    </Box>
                  }
                  sx={{ alignItems: 'flex-start' }}
                />
              </RadioGroup>
            </FormControl>
          </>
        ) : (
          <Typography variant="body2" color="text.secondary">
            Export functionality is only available in Professional Analysis mode.
            Switch to professional mode to access export options.
          </Typography>
        )}
      </DialogContent>
      
      <DialogActions>
        <Button onClick={handleClose} disabled={isExporting}>
          Cancel
        </Button>
        <Button 
          onClick={handleExport} 
          variant="contained" 
          disabled={isExporting || !isProfessional}
          startIcon={isExporting ? <CircularProgress size={20} /> : <FileDownloadIcon />}
        >
          {isExporting ? 'Exporting...' : 'Export'}
        </Button>
      </DialogActions>
    </Dialog>
  );
}
