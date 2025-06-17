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
      setError('Inget förfrågnings-ID tillgängligt för export');
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
            link.download = `beslutsanalys-${requestId}.json`;
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            window.URL.revokeObjectURL(url);
          } else if (response.data.download_url) {
            // For other formats, use the download URL
            const downloadUrl = `${API_BASE_URL}${response.data.download_url}`;
            window.open(downloadUrl, '_blank');
          } else {
            setError('Nedladdningslänk inte tillgänglig. Försök igen.');
            setIsExporting(false);
            return;
          }
          
          setSuccess(true);
          setTimeout(() => {
            setSuccess(false);
            onClose();
          }, 2000);
          
        } else {
          setError(response.data.message || 'Export misslyckades');
        }
      } else {
        // Fallback to basic export (to be implemented)
        setError('Standardexport inte implementerat ännu. Använd Professionell Analys-läge.');
        setIsExporting(false);
        return;
      }

    } catch (err) {
      console.error('Export error:', err);
      setError(
        err.response?.data?.detail || 
        err.message || 
        'Misslyckades att exportera rapport. Försök igen.'
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
        return 'Vacker HTML-rapport med interaktiva element och styling';
      case 'pdf':
        return 'PDF-format (kommer snart - använd HTML för tillfället)';
      case 'json':
        return 'Rå JSON-data för integration och vidare analys';
      default:
        return 'Exportformat';
    }
  };

  return (
    <Dialog open={open} onClose={handleClose} maxWidth="sm" fullWidth>
      <DialogTitle sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
        <FileDownloadIcon />
        {isProfessional ? 'Exportera Professionell Rapport' : 'Exportera Beslutsanalys'}
        {isProfessional && (
          <Chip 
            label="Professionell" 
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
            Rapport exporterad framgångsrikt!
          </Alert>
        )}

        {isProfessional ? (
          <>
            <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
              Exportera din professionella beslutsanalys i olika format lämpliga för 
              ledningspresentationer, dokumentation och vidare analys.
            </Typography>

            <FormControl component="fieldset" fullWidth>
              <FormLabel component="legend" sx={{ mb: 2, fontWeight: 600 }}>
                Välj Exportformat
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
                          HTML-rapport
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
                          PDF-rapport
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
                          JSON-data
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
            Exportfunktionalitet är endast tillgänglig i Professionell Analys-läge.
            Växla till professionellt läge för att få tillgång till exportalternativ.
          </Typography>
        )}
      </DialogContent>
      
      <DialogActions>
        <Button onClick={handleClose} disabled={isExporting}>
          Avbryt
        </Button>
        <Button 
          onClick={handleExport} 
          variant="contained" 
          disabled={isExporting || !isProfessional}
          startIcon={isExporting ? <CircularProgress size={20} /> : <FileDownloadIcon />}
        >
          {isExporting ? 'Exporterar...' : 'Exportera'}
        </Button>
      </DialogActions>
    </Dialog>
  );
} 