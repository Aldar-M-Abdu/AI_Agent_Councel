import React, { useState } from 'react';
import { Dialog, DialogTitle, DialogContent, DialogActions, Button, TextField, Tabs, Tab, Typography, Box } from '@mui/material';
import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:8000';

export default function AuthModal({ open, onClose, onAuthSuccess }) {
  const [tab, setTab] = useState(0);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleTabChange = (_, newValue) => {
    setTab(newValue);
    setError(null);
  };

  const handleAuth = async (endpoint) => {
    setLoading(true);
    setError(null);
    try {
      const res = await axios.post(`${API_BASE_URL}/api/${endpoint}`, { username, password });
      onAuthSuccess(res.data.access_token);
      setUsername('');
      setPassword('');
      onClose();
    } catch (err) {
      setError(err.response?.data?.detail || 'Authentication failed');
    }
    setLoading(false);
  };

  return (
    <Dialog open={open} onClose={onClose}>
      <DialogTitle>Account</DialogTitle>
      <DialogContent>
        <Tabs value={tab} onChange={handleTabChange} centered>
          <Tab label="Log in" />
          <Tab label="Register" />
        </Tabs>
        <Box mt={2}>
          <TextField
            label="Username"
            value={username}
            onChange={e => setUsername(e.target.value)}
            fullWidth
            margin="normal"
            autoFocus
          />
          <TextField
            label="Password"
            type="password"
            value={password}
            onChange={e => setPassword(e.target.value)}
            fullWidth
            margin="normal"
          />
          {error && <Typography color="error" variant="body2">{error}</Typography>}
        </Box>
      </DialogContent>
      <DialogActions>
        <Button onClick={() => handleAuth(tab === 0 ? 'login' : 'register')} color="primary" variant="contained" disabled={loading}>
          {tab === 0 ? 'Log in' : 'Register'}
        </Button>
        <Button onClick={onClose}>Cancel</Button>
      </DialogActions>
    </Dialog>
  );
}
