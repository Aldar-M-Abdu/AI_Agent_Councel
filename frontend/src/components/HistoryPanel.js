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
        setInfo('Showing demo data. Log in to see your personal history.');
      } else if (res.data.message && token) {
        setInfo(res.data.message);
      } else if (!token) {
        setInfo('No login required. History is shown automatically.');
      }
    } catch (err) {
      console.error('History fetch error:', err);
      setError(`Failed to load history: ${err.message}`);
      
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
      setInfo('Showing local demo data due to a connection error.');
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
          <Typography variant="h6">Decision History</Typography>
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
              Loading history...
            </Typography>
          </div>
        ) : history.length === 0 ? (
          <div style={{ textAlign: 'center', padding: 20 }}>
            <HistoryIcon style={{ fontSize: 48, color: '#ccc', marginBottom: 16 }} />
            <Typography variant="body1" color="textSecondary">
              No history found.
            </Typography>
            <Typography variant="body2" color="textSecondary" style={{ marginTop: 8 }}>
              Your decisions will appear here when you use the system.
            </Typography>
          </div>
        ) : (
          <>
            <Typography variant="body2" color="textSecondary" style={{ marginBottom: 16 }}>
              {history.length} decisions in history
            </Typography>
            <List>
              {history.map((item, idx) => (
                <React.Fragment key={idx}>
                  <ListItem alignItems="flex-start" style={{ paddingLeft: 0, paddingRight: 0 }}>
                    <ListItemText
                      primary={
                        <Typography variant="subtitle1" style={{ fontWeight: 600, marginBottom: 4 }}>
                          {item.user_query || item.question || 'No question'}
                        </Typography>
                      }
                      secondary={
                        <div>
                          <Typography variant="body2" style={{ marginBottom: 8 }}>
                            {item.final_recommendation || item.executive_summary || 'No recommendation'}
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
                              <strong>Quality:</strong> {Math.round(item.decision_quality_score * 100)}% • 
                              <strong> Confidence:</strong> {item.confidence_level || 'medium'} • 
                              <strong> Date:</strong> {item.saved_at ? new Date(item.saved_at).toLocaleDateString('en-US') : 'Unknown'}
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
            Close
          </Button>
          <Button 
            onClick={fetchHistory} 
            variant="outlined" 
            style={{ minWidth: 100 }}
            disabled={loading}
          >
            Refresh
          </Button>
        </div>
      </div>
    </Drawer>
  );
}
