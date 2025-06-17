import React, { useEffect, useState } from 'react';
import { Drawer, Typography, List, ListItem, ListItemText, CircularProgress, Button, Alert, Divider } from '@mui/material';
import HistoryIcon from '@mui/icons-material/History';
import InfoIcon from '@mui/icons-material/Info';
import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:8000';

export default function HistoryPanel({ open, onClose, token }) {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [info, setInfo] = useState(null);

  useEffect(() => {
    if (open) {
      console.log('HistoryPanel opened, fetching history...', { token: !!token });
      fetchHistory();
    }
    // eslint-disable-next-line
  }, [open, token]);

  const fetchHistory = async () => {
    setLoading(true);
    setError(null);
    setInfo(null);
    
    try {
      console.log('Fetching history from:', `${API_BASE_URL}/api/history`);
      const headers = token ? { Authorization: `Bearer ${token}` } : {};
      const res = await axios.get(`${API_BASE_URL}/api/history`, { headers });
      
      console.log('History response:', res.data);
      setHistory(res.data.history || []);
      
      // Show appropriate message
      if (res.data.demo && !token) {
        setInfo('Visar demo-data. Logga in för att se din personliga historik.');
      } else if (res.data.message && token) {
        setInfo(res.data.message);
      } else if (!token) {
        setInfo('Ingen inloggning krävs. Historiken visas automatiskt.');
      }
    } catch (err) {
      console.error('History fetch error:', err);
      setError(`Misslyckades att ladda historik: ${err.message}`);
      
      // Add fallback demo data for testing
      setHistory([
        {
          request_id: "fallback-1",
          user_query: "Should I invest in renewable energy stocks?",
          executive_summary: "Fallback demo: Consider diversified green energy portfolio",
          decision_quality_score: 0.85,
          confidence_level: "high",
          saved_at: "2025-06-16T20:00:00",
          final_recommendation: "Proceed with renewable energy investment strategy"
        }
      ]);
      setInfo('Visar lokal demo-data på grund av anslutningsfel.');
    }
    setLoading(false);
  };

  return (
    <Drawer 
      anchor="left" 
      open={open} 
      onClose={onClose}
      className="history-drawer"
      ModalProps={{
        keepMounted: true, // Better open performance on mobile.
      }}
    >
      <div style={{ width: 450, padding: 24, maxHeight: '100vh', overflow: 'auto' }}>
        <div style={{ display: 'flex', alignItems: 'center', marginBottom: 16 }}>
          <HistoryIcon style={{ marginRight: 8 }} />
          <Typography variant="h6">Beslutshistorik</Typography>
        </div>
        
        {info && (
          <Alert severity="info" style={{ marginBottom: 16 }} icon={<InfoIcon />}>
            {info}
          </Alert>
        )}
        
        {error && (
          <Alert severity="error" style={{ marginBottom: 16 }}>
            {error}
          </Alert>
        )}

        {loading ? (
          <div style={{ textAlign: 'center', padding: 20 }}>
            <CircularProgress />
            <Typography variant="body2" style={{ marginTop: 10 }}>
              Laddar historik...
            </Typography>
          </div>
        ) : history.length === 0 ? (
          <div style={{ textAlign: 'center', padding: 20 }}>
            <HistoryIcon style={{ fontSize: 48, color: '#ccc', marginBottom: 16 }} />
            <Typography variant="body1" color="textSecondary">
              Ingen historik hittades.
            </Typography>
            <Typography variant="body2" color="textSecondary" style={{ marginTop: 8 }}>
              Dina beslut kommer att visas här när du använder systemet.
            </Typography>
          </div>
        ) : (
          <>
            <Typography variant="body2" color="textSecondary" style={{ marginBottom: 16 }}>
              {history.length} beslut i historiken
            </Typography>
            <List>
              {history.map((item, idx) => (
                <React.Fragment key={idx}>
                  <ListItem alignItems="flex-start" style={{ paddingLeft: 0, paddingRight: 0 }}>
                    <ListItemText
                      primary={
                        <Typography variant="subtitle1" style={{ fontWeight: 600, marginBottom: 4 }}>
                          {item.user_query || item.question || 'Ingen fråga'}
                        </Typography>
                      }
                      secondary={
                        <div>
                          <Typography variant="body2" style={{ marginBottom: 8 }}>
                            {item.final_recommendation || item.executive_summary || 'Ingen rekommendation'}
                          </Typography>
                          {item.decision_quality_score && (
                            <div style={{ 
                              fontSize: '0.8em', 
                              color: '#666', 
                              backgroundColor: '#f5f5f5', 
                              padding: '4px 8px', 
                              borderRadius: '4px',
                              display: 'inline-block'
                            }}>
                              <strong>Kvalitet:</strong> {Math.round(item.decision_quality_score * 100)}% • 
                              <strong> Förtroende:</strong> {item.confidence_level || 'medium'} • 
                              <strong> Datum:</strong> {item.saved_at ? new Date(item.saved_at).toLocaleDateString('sv-SE') : 'Okänt'}
                            </div>
                          )}
                        </div>
                      }
                    />
                  </ListItem>
                  {idx < history.length - 1 && <Divider />}
                </React.Fragment>
              ))}
            </List>
          </>
        )}
        
        <div style={{ marginTop: 24, display: 'flex', gap: 12 }}>
          <Button onClick={onClose} variant="contained" color="primary" fullWidth>
            Stäng
          </Button>
          <Button 
            onClick={fetchHistory} 
            variant="outlined" 
            style={{ minWidth: 100 }}
            disabled={loading}
          >
            Uppdatera
          </Button>
        </div>
      </div>
    </Drawer>
  );
} 