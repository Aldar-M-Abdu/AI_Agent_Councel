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
  { name: 'Neutral Agent', label: 'Neutral (Strategisk Affärsanalytiker)' },
  { name: 'Positive Agent', label: 'Positiv (Chefsinnovationsdirektör)' },
  { name: 'Skeptic Agent', label: 'Skeptiker (Chefsriskansvarig)' },
  { name: 'Risk Expert Agent', label: 'Riskexpert (Kvantitativ Riskhanterare)' },
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

  // Ladda inställningar när panelen öppnas
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
        throw new Error(`Misslyckades med att ladda inställningar: ${response.statusText}`);
      }
      const data = await response.json();
      setSettings(data);
    } catch (err) {
      setError(`Fel vid laddning av inställningar: ${err.message}`);
      console.error('Inställningsladdningsfel:', err);
    } finally {
      setLoading(false);
    }
  };

  const loadAvailableModels = async () => {
    try {
      const response = await fetch(`${config.apiUrl}/api/settings/models`);
      if (!response.ok) {
        throw new Error(`Misslyckades med att ladda modeller: ${response.statusText}`);
      }
      const data = await response.json();
      setAvailableModels(data);
    } catch (err) {
      console.error('Modelladdningsfel:', err);
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
        throw new Error(`Misslyckades med att spara inställningar: ${response.statusText}`);
      }
      
      const data = await response.json();
      setSettings(data.updated_settings);
      setSuccess(data.message);
      
      // Rensa framgångsmeddelande efter 3 sekunder
      setTimeout(() => setSuccess(null), 3000);
    } catch (err) {
      setError(`Fel vid sparning av inställningar: ${err.message}`);
      console.error('Inställningssparningsfel:', err);
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
        throw new Error(`Misslyckades med att återställa inställningar: ${response.statusText}`);
      }
      
      const data = await response.json();
      setSettings(data.updated_settings);
      setSuccess(data.message);
      
      // Rensa framgångsmeddelande efter 3 sekunder
      setTimeout(() => setSuccess(null), 3000);
    } catch (err) {
      setError(`Fel vid återställning av inställningar: ${err.message}`);
      console.error('Inställningsåterställningsfel:', err);
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
          Systeminställningar
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
            {/* Agentval */}
            <Accordion defaultExpanded>
              <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                <Typography variant="h6">Agentval</Typography>
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
                  Diskussionsdjup: {discussionDepth}
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

            {/* Modellkonfiguration */}
            <Accordion>
              <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                <Typography variant="h6">Modellkonfiguration</Typography>
              </AccordionSummary>
              <AccordionDetails>
                <FormControl fullWidth sx={{ mb: 2 }}>
                  <InputLabel>Modelltyp</InputLabel>
                  <Select
                    value={settings.model_type}
                    onChange={(e) => handleSettingChange('model_type', e.target.value)}
                    label="Modelltyp"
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
                    <InputLabel>OpenRouter-modell</InputLabel>
                    <Select
                      value={settings.openrouter_model}
                      onChange={(e) => handleSettingChange('openrouter_model', e.target.value)}
                      label="OpenRouter-modell"
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
                  label="Professionellt läge"
                />

                <FormControlLabel
                  control={
                    <Switch
                      checked={settings.enable_discussion_mode}
                      onChange={(e) => handleSettingChange('enable_discussion_mode', e.target.checked)}
                    />
                  }
                  label="Diskussionsläge"
                />

                <FormControlLabel
                  control={
                    <Switch
                      checked={settings.enable_reasoning_mode}
                      onChange={(e) => handleSettingChange('enable_reasoning_mode', e.target.checked)}
                    />
                  }
                  label="Resonemangsläge"
                />

                <Typography variant="subtitle2" sx={{ mt: 2, mb: 1 }}>
                  Kvalitetströskel: {settings.quality_threshold}
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
                  Konsensuströskel: {settings.consensus_threshold}
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
                  Max diskussionsrundor: {settings.max_discussion_rounds}
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

            {/* Åtgärdsknappar */}
            <Box sx={{ display: 'flex', gap: 2, mb: 2 }}>
              <Button
                variant="contained"
                color="primary"
                onClick={saveSettings}
                disabled={saving}
                startIcon={saving ? <CircularProgress size={20} /> : <SaveIcon />}
                fullWidth
              >
                {saving ? 'Sparar...' : 'Spara inställningar'}
              </Button>
              
              <Button
                variant="outlined"
                color="secondary"
                onClick={resetSettings}
                disabled={saving}
                startIcon={<RestoreIcon />}
                fullWidth
              >
                Återställ till standard
              </Button>
            </Box>

            <Button
              variant="text"
              onClick={onClose}
              fullWidth
              sx={{ mt: 1 }}
            >
              Stäng
            </Button>
          </>
        )}
      </Box>
    </Drawer>
  );
} 