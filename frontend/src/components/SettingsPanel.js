import React, { useState, useEffect } from 'react';
import {
  Drawer,
  FormGroup,
  FormControlLabel,
  Checkbox,
  Slider,
  Typography,
  Button,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Switch,
  Box,
  Divider,
  Alert,
  CircularProgress,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  TextField
} from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import SaveIcon from '@mui/icons-material/Save';
import RestoreIcon from '@mui/icons-material/Restore';
import config from '../config';

const agentOptions = [
  { name: 'Neutral Agent', label: 'Neutral (Strategic Business Analyst)' },
  { name: 'Positive Agent', label: 'Positive (Chief Innovation Officer)' },
  { name: 'Skeptic Agent', label: 'Skeptic (Chief Risk Officer)' },
  { name: 'Risk Expert Agent', label: 'Risk Expert (Quantitative Risk Manager)' },
];

export default function SettingsPanel({ 
  open, 
  onClose, 
  selectedAgents, 
  onAgentChange, 
  discussionDepth, 
  onDepthChange 
}) {
  const [settings, setSettings] = useState(null);
  const [availableModels, setAvailableModels] = useState(null);
  const [loading, setLoading] = useState(false);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);

  // Load settings when the panel opens
  useEffect(() => {
    if (open) {
      loadSettings();
      loadAvailableModels();
    }
  }, [open]);

  const loadSettings = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch(`${config.apiUrl}/api/settings`);
      if (!response.ok) {
        throw new Error(`Failed to load settings: ${response.statusText}`);
      }
      const data = await response.json();
      setSettings(data);
    } catch (err) {
      setError(`Error loading settings: ${err.message}`);
      console.error('Settings load error:', err);
    } finally {
      setLoading(false);
    }
  };

  const loadAvailableModels = async () => {
    try {
      const response = await fetch(`${config.apiUrl}/api/settings/models`);
      if (!response.ok) {
        throw new Error(`Failed to load models: ${response.statusText}`);
      }
      const data = await response.json();
      setAvailableModels(data);
    } catch (err) {
      console.error('Model load error:', err);
    }
  };

  const saveSettings = async () => {
    if (!settings) return;
    
    setSaving(true);
    setError(null);
    setSuccess(null);
    
    try {
      const response = await fetch(`${config.apiUrl}/api/settings`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(settings),
      });
      
      if (!response.ok) {
        throw new Error(`Failed to save settings: ${response.statusText}`);
      }
      
      const data = await response.json();
      setSettings(data.updated_settings);
      setSuccess(data.message);
      
      // Clear success message after 3 seconds
      setTimeout(() => setSuccess(null), 3000);
    } catch (err) {
      setError(`Error saving settings: ${err.message}`);
      console.error('Settings save error:', err);
    } finally {
      setSaving(false);
    }
  };

  const resetSettings = async () => {
    setSaving(true);
    setError(null);
    setSuccess(null);
    
    try {
      const response = await fetch(`${config.apiUrl}/api/settings/reset`, {
        method: 'POST',
      });
      
      if (!response.ok) {
        throw new Error(`Failed to reset settings: ${response.statusText}`);
      }
      
      const data = await response.json();
      setSettings(data.updated_settings);
      setSuccess(data.message);
      
      // Clear success message after 3 seconds
      setTimeout(() => setSuccess(null), 3000);
    } catch (err) {
      setError(`Error resetting settings: ${err.message}`);
      console.error('Settings reset error:', err);
    } finally {
      setSaving(false);
    }
  };

  const handleSettingChange = (key, value) => {
    setSettings(prev => ({
      ...prev,
      [key]: value
    }));
  };

  if (loading) {
    return (
      <Drawer anchor="right" open={open} onClose={onClose}>
        <Box sx={{ width: 400, p: 3, display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>
          <CircularProgress />
        </Box>
      </Drawer>
    );
  }

  return (
    <Drawer anchor="right" open={open} onClose={onClose}>
      <Box sx={{ width: 400, p: 3 }}>
        <Typography variant="h5" gutterBottom>
          System Settings
        </Typography>

        {error && (
          <Alert severity="error" sx={{ mb: 2 }}>
            {error}
          </Alert>
        )}

        {success && (
          <Alert severity="success" sx={{ mb: 2 }}>
            {success}
          </Alert>
        )}

        {settings && (
          <>
            {/* Agent selection */}
            <Accordion defaultExpanded>
              <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                <Typography variant="h6">Agent Selection</Typography>
              </AccordionSummary>
              <AccordionDetails>
                <FormGroup>
                  {agentOptions.map((agent) => (
                    <FormControlLabel
                      key={agent.name}
                      control={
                        <Checkbox
                          checked={selectedAgents.includes(agent.name)}
                          onChange={() => onAgentChange(agent.name)}
                        />
                      }
                      label={agent.label}
                    />
                  ))}
                </FormGroup>
                
                <Typography variant="subtitle2" sx={{ mt: 2, mb: 1 }}>
                  Discussion Depth: {discussionDepth}
                </Typography>
                <Slider
                  value={discussionDepth}
                  onChange={(_, v) => onDepthChange(v)}
                  min={1}
                  max={5}
                  step={1}
                  marks
                  valueLabelDisplay="auto"
                />
              </AccordionDetails>
            </Accordion>

            {/* Model configuration */}
            <Accordion>
              <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                <Typography variant="h6">Model Configuration</Typography>
              </AccordionSummary>
              <AccordionDetails>
                <FormControl fullWidth sx={{ mb: 2 }}>
                  <InputLabel>Model Type</InputLabel>
                  <Select
                    value={settings.model_type}
                    onChange={(e) => handleSettingChange('model_type', e.target.value)}
                    label="Model Type"
                  >
                    {availableModels?.model_types?.map((model) => (
                      <MenuItem key={model.value} value={model.value}>
                        {model.label} - {model.description}
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>

                {settings.model_type === 'direct_hf' && (
                  <FormControl fullWidth sx={{ mb: 2 }}>
                    <InputLabel>OpenRouter Model</InputLabel>
                    <Select
                      value={settings.openrouter_model}
                      onChange={(e) => handleSettingChange('openrouter_model', e.target.value)}
                      label="OpenRouter Model"
                    >
                      {availableModels?.openrouter_models?.map((model) => (
                        <MenuItem key={model.value} value={model.value}>
                          {model.label} - {model.description}
                        </MenuItem>
                      ))}
                    </Select>
                  </FormControl>
                )}

                <TextField
                  fullWidth
                  type="number"
                  label="Max Response Time (seconds)"
                  value={settings.max_response_time}
                  onChange={(e) => handleSettingChange('max_response_time', parseInt(e.target.value))}
                  inputProps={{ min: 5, max: 60 }}
                  sx={{ mb: 2 }}
                />
              </AccordionDetails>
            </Accordion>

            {/* Performance Settings */}
            <Accordion>
              <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                <Typography variant="h6">Performance Settings</Typography>
              </AccordionSummary>
              <AccordionDetails>
                <FormControlLabel
                  control={
                    <Switch
                      checked={settings.fast_mode}
                      onChange={(e) => handleSettingChange('fast_mode', e.target.checked)}
                    />
                  }
                  label="Fast Mode"
                />
                
                <FormControlLabel
                  control={
                    <Switch
                      checked={settings.use_direct_hf}
                      onChange={(e) => handleSettingChange('use_direct_hf', e.target.checked)}
                    />
                  }
                  label="Use Direct HF API"
                />

                <FormControlLabel
                  control={
                    <Switch
                      checked={settings.deepseek_use_reasoning}
                      onChange={(e) => handleSettingChange('deepseek_use_reasoning', e.target.checked)}
                    />
                  }
                  label="DeepSeek Reasoning Mode"
                />
              </AccordionDetails>
            </Accordion>

            {/* Advanced Settings */}
            <Accordion>
              <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                <Typography variant="h6">Advanced Settings</Typography>
              </AccordionSummary>
              <AccordionDetails>
                <FormControlLabel
                  control={
                    <Switch
                      checked={settings.enable_professional_mode}
                      onChange={(e) => handleSettingChange('enable_professional_mode', e.target.checked)}
                    />
                  }
                  label="Professional Mode"
                />

                <FormControlLabel
                  control={
                    <Switch
                      checked={settings.enable_discussion_mode}
                      onChange={(e) => handleSettingChange('enable_discussion_mode', e.target.checked)}
                    />
                  }
                  label="Discussion Mode"
                />

                <FormControlLabel
                  control={
                    <Switch
                      checked={settings.enable_reasoning_mode}
                      onChange={(e) => handleSettingChange('enable_reasoning_mode', e.target.checked)}
                    />
                  }
                  label="Reasoning Mode"
                />

                <Typography variant="subtitle2" sx={{ mt: 2, mb: 1 }}>
                  Quality Threshold: {settings.quality_threshold}
                </Typography>
                <Slider
                  value={settings.quality_threshold}
                  onChange={(_, v) => handleSettingChange('quality_threshold', v)}
                  min={0.1}
                  max={1.0}
                  step={0.1}
                  marks
                  valueLabelDisplay="auto"
                />

                <Typography variant="subtitle2" sx={{ mt: 2, mb: 1 }}>
                  Consensus Threshold: {settings.consensus_threshold}
                </Typography>
                <Slider
                  value={settings.consensus_threshold}
                  onChange={(_, v) => handleSettingChange('consensus_threshold', v)}
                  min={0.1}
                  max={1.0}
                  step={0.1}
                  marks
                  valueLabelDisplay="auto"
                />

                <Typography variant="subtitle2" sx={{ mt: 2, mb: 1 }}>
                  Max Discussion Rounds: {settings.max_discussion_rounds}
                </Typography>
                <Slider
                  value={settings.max_discussion_rounds}
                  onChange={(_, v) => handleSettingChange('max_discussion_rounds', v)}
                  min={1}
                  max={10}
                  step={1}
                  marks
                  valueLabelDisplay="auto"
                />
              </AccordionDetails>
            </Accordion>

            <Divider sx={{ my: 3 }} />

            {/* Action buttons */}
            <Box sx={{ display: 'flex', gap: 2, mb: 2 }}>
              <Button
                variant="contained"
                color="primary"
                onClick={saveSettings}
                disabled={saving}
                startIcon={saving ? <CircularProgress size={20} /> : <SaveIcon />}
                fullWidth
              >
                {saving ? 'Saving...' : 'Save Settings'}
              </Button>
              
              <Button
                variant="outlined"
                color="secondary"
                onClick={resetSettings}
                disabled={saving}
                startIcon={<RestoreIcon />}
                fullWidth
              >
                Reset to Defaults
              </Button>
            </Box>

            <Button
              variant="text"
              onClick={onClose}
              fullWidth
              sx={{ mt: 1 }}
            >
              Close
            </Button>
          </>
        )}
      </Box>
    </Drawer>
  );
}
