import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';
import SettingsPanel from './components/SettingsPanel';
import ExportModal from './components/ExportModal';
import { IconButton, Button, Tab, Tabs, Box, Typography, Card, CardContent, Grid, Chip, LinearProgress, Alert } from '@mui/material';
import SettingsIcon from '@mui/icons-material/Settings';
import ShareIcon from '@mui/icons-material/Share';
import AuthModal from './components/AuthModal';
import HistoryPanel from './components/HistoryPanel';
import AccountCircleIcon from '@mui/icons-material/AccountCircle';
import HistoryIcon from '@mui/icons-material/History';
import BusinessIcon from '@mui/icons-material/Business';
import PersonIcon from '@mui/icons-material/Person';
import AnalyticsIcon from '@mui/icons-material/Analytics';
import TrendingUpIcon from '@mui/icons-material/TrendingUp';

// Base URL for the backend API
const API_BASE_URL = 'http://127.0.0.1:8000';

function TabPanel(props) {
  const { children, value, index, ...other } = props;
  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`simple-tabpanel-${index}`}
      aria-labelledby={`simple-tab-${index}`}
      {...other}
    >
      {value === index && (
        <Box sx={{ p: 3 }}>
          {children}
        </Box>
      )}
    </div>
  );
}

function App() {
  const [userText, setUserText] = useState('');
  const [decisionResponse, setDecisionResponse] = useState(null);
  const [professionalResponse, setProfessionalResponse] = useState(null);
  const [dashboardData, setDashboardData] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [showResults, setShowResults] = useState(false);
  // eslint-disable-next-line no-unused-vars
  const [agents, setAgents] = useState([]);
  const [settingsOpen, setSettingsOpen] = useState(false);
  const [exportOpen, setExportOpen] = useState(false);
  const [selectedAgents, setSelectedAgents] = useState(['NeutralAgent', 'PositiveAgent', 'SkepticAgent', 'RiskExpertAgent']);
  const [discussionDepth, setDiscussionDepth] = useState(2);
  const [authOpen, setAuthOpen] = useState(false);
  const [historyOpen, setHistoryOpen] = useState(false);
  const [token, setToken] = useState(() => localStorage.getItem('jwt') || '');
  const [activeTab, setActiveTab] = useState(0);
  const [decisionMode, setDecisionMode] = useState('professional'); // 'professional' or 'standard'
  
  // Professional decision fields
  const [urgencyLevel, setUrgencyLevel] = useState('medium');
  const [stakeholderContext, setStakeholderContext] = useState('');
  const [budgetConstraints, setBudgetConstraints] = useState('');
  const [timelineRequirements, setTimelineRequirements] = useState('');
  const [decisionFramework, setDecisionFramework] = useState('auto');

  // Fetch agent information on component mount
  useEffect(() => {
    fetchAgents();
  }, []);

  const fetchAgents = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/agents`);
      setAgents(response.data.agents);
    } catch (err) {
      console.error("Error fetching agents:", err);
    }
  };

  const handleAuthSuccess = (jwt) => {
    setToken(jwt);
    localStorage.setItem('jwt', jwt);
  };
  
  const handleLogout = () => {
    setToken('');
    localStorage.removeItem('jwt');
  };

  const handleTabChange = (event, newValue) => {
    setActiveTab(newValue);
  };

  const handleSubmitProfessionalDecision = async (e) => {
    e.preventDefault();
    if (!userText.trim()) {
      setError('Please enter a decision question.');
      return;
    }
    
    setIsLoading(true);
    setError(null);
    setProfessionalResponse(null);
    setDashboardData(null);
    setShowResults(false);
    
    try {
      const requestData = {
        user_text: userText,
        urgency_level: urgencyLevel,
        stakeholder_context: stakeholderContext || undefined,
        budget_constraints: budgetConstraints || undefined,
        timeline_requirements: timelineRequirements || undefined,
        enable_executive_reporting: true,
        decision_framework: decisionFramework
      };

      const response = await axios.post(`${API_BASE_URL}/api/professional-decision`, requestData);
      setProfessionalResponse(response.data);
      setShowResults(true);

      // Fetch dashboard data
      try {
        const dashboardResponse = await axios.get(`${API_BASE_URL}/api/executive-dashboard/${response.data.request_id}`);
        setDashboardData(dashboardResponse.data);
      } catch (dashboardErr) {
        console.warn("Dashboard data not available:", dashboardErr);
      }

      // Save to user history if logged in
      if (token) {
        await axios.post(`${API_BASE_URL}/api/history/save`, response.data, {
          headers: { Authorization: `Bearer ${token}` }
        });
      }
    } catch (err) {
      console.error("Error submitting professional decision:", err);
      setError(`Failed to get professional analysis: ${err.response?.data?.detail || err.message || 'Unknown error'}`);
    }
    setIsLoading(false);
  };

  const handleSubmitStandardDecision = async (e) => {
    e.preventDefault();
    if (!userText.trim()) {
      setError('Please enter a decision question.');
      return;
    }
    
    setIsLoading(true);
    setError(null);
    setDecisionResponse(null);
    setShowResults(false);
    
    try {
      let response;
      try {
        response = await axios.post(`${API_BASE_URL}/api/orchestrated-debate`, { user_text: userText });
      } catch (enhancedErr) {
        try {
          response = await axios.post(`${API_BASE_URL}/api/decision-with-discussion`, { user_text: userText });
        } catch (basicErr) {
          response = await axios.post(`${API_BASE_URL}/api/debate`, { user_text: userText });
        }
      }
      setDecisionResponse(response.data);
      setShowResults(true);
      
      if (token) {
        await axios.post(`${API_BASE_URL}/api/history/save`, response.data, {
          headers: { Authorization: `Bearer ${token}` }
        });
      }
    } catch (err) {
      console.error("Error submitting decision:", err);
      setError(`Failed to get decision: ${err.response?.data?.detail || err.message || 'Unknown error'}`);
    }
    setIsLoading(false);
  };

  const handleSubmitDecision = decisionMode === 'professional' ? handleSubmitProfessionalDecision : handleSubmitStandardDecision;

  const handleNewDecision = () => {
    setUserText('');
    setDecisionResponse(null);
    setProfessionalResponse(null);
    setDashboardData(null);
    setShowResults(false);
    setError(null);
    setStakeholderContext('');
    setBudgetConstraints('');
    setTimelineRequirements('');
  };

  const getAgentIcon = (agentName) => {
    const icons = {
      'Neutral Agent': '⚖️',
      'Positive Agent': '🌟', 
      'Skeptic Agent': '🔍',
      'Risk Expert Agent': '🛡️'
    };
    return icons[agentName] || '🤖';
  };

  const getAgentColor = (agentName) => {
    const colors = {
      'Neutral Agent': '#6c757d',
      'Positive Agent': '#28a745',
      'Skeptic Agent': '#ffc107',
      'Risk Expert Agent': '#dc3545'
    };
    return colors[agentName] || '#007bff';
  };

  const getConfidenceColor = (confidence) => {
    const confidenceNum = typeof confidence === 'string' ? 0.5 : confidence;
    if (confidenceNum >= 0.8) return '#28a745';
    if (confidenceNum >= 0.6) return '#ffc107';
    return '#dc3545';
  };

  const formatConfidence = (confidence) => {
    if (typeof confidence === 'string') {
      return confidence.charAt(0).toUpperCase() + confidence.slice(1);
    }
    return `${(confidence * 100).toFixed(0)}%`;
  };

  const handleAgentChange = (agentName) => {
    setSelectedAgents((prev) =>
      prev.includes(agentName)
        ? prev.filter((a) => a !== agentName)
        : [...prev, agentName]
    );
  };
  
  const handleDepthChange = (val) => setDiscussionDepth(val);

  const renderProfessionalResults = () => {
    if (!professionalResponse) return null;

    return (
      <div className="results-container">
        <Box sx={{ width: '100%' }}>
          <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
            <Tabs value={activeTab} onChange={handleTabChange} aria-label="professional results tabs">
              <Tab icon={<AnalyticsIcon />} label="Executive Summary" />
              <Tab icon={<TrendingUpIcon />} label="Dashboard" />
              <Tab icon={<BusinessIcon />} label="Detailed Analysis" />
            </Tabs>
          </Box>
          
          <TabPanel value={activeTab} index={0}>
            {/* Executive Summary */}
            <Grid container spacing={3}>
              {/* Main Executive Summary Card */}
              <Grid item xs={12}>
                <Card className="executive-summary-card" sx={{ mb: 3 }}>
                  <CardContent sx={{ p: 4 }}>
                    <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 3 }}>
                      <Typography variant="h4" component="div" sx={{ display: 'flex', alignItems: 'center', fontWeight: 600 }}>
                        <BusinessIcon sx={{ mr: 2, fontSize: 32 }} />
                      Executive Summary
                    </Typography>
                      <Box>
                      <Chip
                          label={`${formatConfidence(professionalResponse.confidence_level)} Confidence`}
                        color="primary"
                          sx={{ 
                            mr: 1, 
                            backgroundColor: getConfidenceColor(professionalResponse.decision_quality_score),
                            fontWeight: 600,
                            fontSize: '0.9rem'
                          }}
                      />
                      <Chip
                          label={`${(professionalResponse.decision_quality_score * 100).toFixed(0)}% Quality`}
                        color="secondary"
                          sx={{ fontWeight: 600, fontSize: '0.9rem' }}
                      />
                    </Box>
                    </Box>
                    
                    {/* Strategic Recommendation */}
                    <Box sx={{ 
                      backgroundColor: 'rgba(255,255,255,0.1)', 
                      p: 3, 
                      borderRadius: 2, 
                      mb: 3,
                      border: '2px solid rgba(255,255,255,0.2)'
                    }}>
                      <Typography variant="h5" sx={{ 
                        mb: 2, 
                        fontWeight: 700,
                        color: 'white',
                        textAlign: 'center'
                      }}>
                        🎯 Strategic Recommendation
                      </Typography>
                      <Typography variant="h6" sx={{ 
                        textAlign: 'center',
                        fontWeight: 600,
                        fontSize: '1.3rem',
                        color: 'rgba(255,255,255,0.95)'
                      }}>
                        {professionalResponse.professional_decision?.recommended_alternative || 'Proceed with Analysis-Based Approach'}
                      </Typography>
                    </Box>

                    {/* Executive Summary Text */}
                    <Typography variant="body1" sx={{ 
                      fontSize: '1.1rem',
                      lineHeight: 1.7,
                      color: 'rgba(255,255,255,0.9)',
                      textAlign: 'justify'
                    }}>
                      {professionalResponse.executive_summary}
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
              
              {/* Key Stats Row */}
              <Grid item xs={12} md={4}>
                <Card sx={{ 
                  height: '100%', 
                  background: 'linear-gradient(135deg, #1976d2 0%, #42a5f5 100%)',
                  color: 'white'
                }}>
                  <CardContent sx={{ textAlign: 'center', p: 3 }}>
                    <AnalyticsIcon sx={{ fontSize: 48, mb: 2, color: 'white' }} />
                    <Typography variant="h4" sx={{ fontWeight: 700, mb: 1 }}>
                      {(professionalResponse.decision_quality_score * 100).toFixed(0)}%
                    </Typography>
                    <Typography variant="h6" sx={{ fontWeight: 600 }}>
                      Decision Quality
                    </Typography>
                    <Typography variant="body2" sx={{ mt: 1, color: 'rgba(255,255,255,0.95)' }}>
                      Based on comprehensive analysis frameworks
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>

              <Grid item xs={12} md={4}>
                <Card sx={{ 
                  height: '100%', 
                  background: 'linear-gradient(135deg, #388e3c 0%, #66bb6a 100%)',
                  color: 'white'
                }}>
                  <CardContent sx={{ textAlign: 'center', p: 3 }}>
                    <TrendingUpIcon sx={{ fontSize: 48, mb: 2, color: 'white' }} />
                    <Typography variant="h4" sx={{ fontWeight: 700, mb: 1 }}>
                      {formatConfidence(professionalResponse.confidence_level)}
                    </Typography>
                    <Typography variant="h6" sx={{ fontWeight: 600 }}>
                      Confidence Level
                    </Typography>
                    <Typography variant="body2" sx={{ mt: 1, color: 'rgba(255,255,255,0.95)' }}>
                      Professional consensus assessment
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>

              <Grid item xs={12} md={4}>
                <Card sx={{ 
                  height: '100%', 
                  background: 'linear-gradient(135deg, #f57c00 0%, #ffb74d 100%)',
                  color: 'white'
                }}>
                  <CardContent sx={{ textAlign: 'center', p: 3 }}>
                    <BusinessIcon sx={{ fontSize: 48, mb: 2, color: 'white' }} />
                    <Typography variant="h4" sx={{ fontWeight: 700, mb: 1 }}>
                      {professionalResponse.next_actions?.length || 5}
                    </Typography>
                    <Typography variant="h6" sx={{ fontWeight: 600 }}>
                      Action Items
                    </Typography>
                    <Typography variant="body2" sx={{ mt: 1, color: 'rgba(255,255,255,0.95)' }}>
                      Strategic implementation steps
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>

              {/* Implementation Plan */}
              <Grid item xs={12} md={6}>
                <Card sx={{ height: '100%' }}>
                  <CardContent sx={{ p: 3 }}>
                    <Typography variant="h6" sx={{ 
                      mb: 3, 
                      display: 'flex', 
                      alignItems: 'center',
                      fontWeight: 600,
                      color: '#1976d2'
                    }}>
                      📋 Strategic Action Plan
                    </Typography>
                    {professionalResponse.next_actions?.map((action, index) => (
                      <Box key={index} sx={{ 
                        display: 'flex', 
                        alignItems: 'flex-start', 
                        mb: 2,
                        p: 2,
                        backgroundColor: '#f8f9fa',
                        borderRadius: 1,
                        borderLeft: '4px solid #1976d2'
                      }}>
                        <Typography variant="h6" sx={{ 
                          minWidth: 32, 
                          height: 32,
                          backgroundColor: '#1976d2',
                          color: 'white',
                          borderRadius: '50%',
                          display: 'flex',
                          alignItems: 'center',
                          justifyContent: 'center',
                          mr: 2,
                          fontSize: '0.9rem',
                          fontWeight: 600
                        }}>
                          {index + 1}
                      </Typography>
                        <Typography variant="body1" sx={{ fontWeight: 500, lineHeight: 1.5 }}>
                          {action}
                        </Typography>
                      </Box>
                    ))}
                  </CardContent>
                </Card>
              </Grid>
              
              {/* Implementation Details */}
              <Grid item xs={12} md={6}>
                <Card sx={{ height: '100%' }}>
                  <CardContent sx={{ p: 3 }}>
                    <Typography variant="h6" sx={{ 
                      mb: 3, 
                      display: 'flex', 
                      alignItems: 'center',
                      fontWeight: 600,
                      color: '#d32f2f'
                    }}>
                      ⚙️ Implementation Framework
                    </Typography>
                    
                    <Box sx={{ mb: 3 }}>
                      <Typography variant="subtitle1" sx={{ fontWeight: 600, mb: 1, color: '#1976d2' }}>
                        📅 Timeline
                    </Typography>
                      <Typography variant="body1" sx={{ 
                        p: 2, 
                        backgroundColor: '#e3f2fd', 
                        borderRadius: 1,
                        borderLeft: '4px solid #2196f3'
                      }}>
                        {professionalResponse.implementation_timeline}
                    </Typography>
                    </Box>

                    <Box sx={{ mb: 3 }}>
                      <Typography variant="subtitle1" sx={{ fontWeight: 600, mb: 1, color: '#d32f2f' }}>
                        ⚠️ Risk Assessment
                      </Typography>
                      <Typography variant="body1" sx={{ 
                        p: 2, 
                        backgroundColor: '#ffebee', 
                        borderRadius: 1,
                        borderLeft: '4px solid #f44336'
                      }}>
                        {professionalResponse.risk_assessment}
                      </Typography>
                    </Box>

                    <Box>
                      <Typography variant="subtitle1" sx={{ fontWeight: 600, mb: 1, color: '#388e3c' }}>
                        🤝 Stakeholder Engagement
                      </Typography>
                      <Typography variant="body1" sx={{ 
                        p: 2, 
                        backgroundColor: '#e8f5e8', 
                        borderRadius: 1,
                        borderLeft: '4px solid #4caf50'
                      }}>
                        {professionalResponse.stakeholder_communication}
                      </Typography>
                    </Box>
                  </CardContent>
                </Card>
              </Grid>
            </Grid>
          </TabPanel>
          
          <TabPanel value={activeTab} index={1}>
            {/* Executive Dashboard */}
            {dashboardData ? (
              <Grid container spacing={3}>
                {/* Dashboard Header */}
                <Grid item xs={12}>
                  <Card sx={{ 
                    background: 'linear-gradient(135deg, #2c3e50 0%, #34495e 100%)',
                    color: 'white',
                    mb: 2
                  }}>
                    <CardContent sx={{ p: 4 }}>
                      <Typography variant="h4" sx={{ 
                        mb: 2, 
                        fontWeight: 600,
                        display: 'flex',
                        alignItems: 'center'
                      }}>
                        <TrendingUpIcon sx={{ mr: 2, fontSize: 36 }} />
                        Executive Dashboard
                      </Typography>
                                          <Typography variant="subtitle1" sx={{ color: 'rgba(255,255,255,0.95)' }}>
                      Strategic Decision Analysis Overview • Generated {new Date().toLocaleDateString('en-US')}
                    </Typography>
                    </CardContent>
                  </Card>
                </Grid>

                {/* Key Performance Indicators */}
                <Grid item xs={12} md={3}>
                  <Card className="dashboard-card" sx={{ 
                    height: '100%',
                    background: 'linear-gradient(135deg, #43a047 0%, #66bb6a 100%)',
                    color: 'white',
                    textAlign: 'center'
                  }}>
                    <CardContent sx={{ p: 3 }}>
                      <Typography variant="h6" sx={{ mb: 2, fontWeight: 600, color: 'rgba(255,255,255,0.95)' }}>
                        Strategic Direction
                      </Typography>
                      <Typography variant="h4" sx={{ fontWeight: 700, mb: 2 }}>
                        ✓
                      </Typography>
                      <Typography variant="body1" sx={{ fontWeight: 600 }}>
                        {dashboardData.recommendation}
                      </Typography>
                    </CardContent>
                  </Card>
                </Grid>

                <Grid item xs={12} md={3}>
                  <Card className="dashboard-card" sx={{ 
                    height: '100%',
                    background: 'linear-gradient(135deg, #1976d2 0%, #42a5f5 100%)',
                    color: 'white',
                    textAlign: 'center'
                  }}>
                    <CardContent sx={{ p: 3 }}>
                      <Typography variant="h6" sx={{ mb: 2, fontWeight: 600, color: 'rgba(255,255,255,0.95)' }}>
                        Confidence Level
                      </Typography>
                      <Typography variant="h4" sx={{ fontWeight: 700, mb: 2 }}>
                        {Math.round(dashboardData.quality_score * 100)}%
                      </Typography>
                      <Typography variant="body1" sx={{ fontWeight: 600 }}>
                        {dashboardData.confidence}
                      </Typography>
                    </CardContent>
                  </Card>
                </Grid>

                <Grid item xs={12} md={3}>
                  <Card className="dashboard-card" sx={{ 
                    height: '100%',
                    background: 'linear-gradient(135deg, #f57c00 0%, #ffb74d 100%)',
                    color: 'white',
                    textAlign: 'center'
                  }}>
                    <CardContent sx={{ p: 3 }}>
                      <Typography variant="h6" sx={{ mb: 2, fontWeight: 600, color: 'rgba(255,255,255,0.95)' }}>
                        Risk Profile
                      </Typography>
                      <Typography variant="h4" sx={{ fontWeight: 700, mb: 2 }}>
                        {(dashboardData.risk_level === 'High') ? '⚠️' : 
                         (dashboardData.risk_level === 'Medium') ? '⚡' : '✅'}
                      </Typography>
                      <Typography variant="body1" sx={{ fontWeight: 600 }}>
                        {dashboardData.risk_level} Risk
                      </Typography>
                    </CardContent>
                  </Card>
                </Grid>
                
                <Grid item xs={12} md={3}>
                  <Card className="dashboard-card" sx={{ 
                    height: '100%',
                    background: 'linear-gradient(135deg, #7b1fa2 0%, #ab47bc 100%)',
                    color: 'white',
                    textAlign: 'center'
                  }}>
                    <CardContent sx={{ p: 3 }}>
                      <Typography variant="h6" sx={{ mb: 2, fontWeight: 600, color: 'rgba(255,255,255,0.95)' }}>
                        Implementation
                      </Typography>
                      <Typography variant="h4" sx={{ fontWeight: 700, mb: 2 }}>
                        {dashboardData.key_actions}
                      </Typography>
                      <Typography variant="body1" sx={{ fontWeight: 600 }}>
                        Key Actions
                      </Typography>
                    </CardContent>
                  </Card>
                </Grid>
                
                {/* Quality Metrics */}
                <Grid item xs={12} md={8}>
                  <Card sx={{ height: '100%' }}>
                    <CardContent sx={{ p: 3 }}>
                      <Typography variant="h6" sx={{ 
                        mb: 3, 
                        fontWeight: 600,
                        color: '#1976d2',
                        display: 'flex',
                        alignItems: 'center'
                      }}>
                        📊 Quality & Consensus Metrics
                      </Typography>
                      
                      <Box sx={{ mb: 4 }}>
                        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 1 }}>
                          <Typography variant="body1" sx={{ fontWeight: 600 }}>
                            Decision Quality Score
                          </Typography>
                          <Typography variant="h6" sx={{ fontWeight: 700, color: '#1976d2' }}>
                            {Math.round(dashboardData.quality_score * 100)}%
                          </Typography>
                      </Box>
                        <LinearProgress 
                          variant="determinate" 
                          value={dashboardData.quality_score * 100} 
                          sx={{ 
                            height: 8, 
                            borderRadius: 4,
                            backgroundColor: '#e3f2fd',
                            '& .MuiLinearProgress-bar': {
                              borderRadius: 4,
                              backgroundColor: '#1976d2'
                            }
                          }} 
                        />
                        <Typography variant="body2" sx={{ mt: 1, color: '#333', fontWeight: 500 }}>
                          Based on comprehensive analysis frameworks and evidence quality
                        </Typography>
                      </Box>

                      <Box sx={{ mb: 4 }}>
                        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 1 }}>
                          <Typography variant="body1" sx={{ fontWeight: 600 }}>
                            Consensus Strength
                          </Typography>
                          <Typography variant="h6" sx={{ fontWeight: 700, color: '#388e3c' }}>
                            {Math.round(dashboardData.consensus_strength * 100)}%
                          </Typography>
                        </Box>
                        <LinearProgress 
                          variant="determinate" 
                          value={dashboardData.consensus_strength * 100} 
                          sx={{ 
                            height: 8, 
                            borderRadius: 4,
                            backgroundColor: '#e8f5e8',
                            '& .MuiLinearProgress-bar': {
                              borderRadius: 4,
                              backgroundColor: '#388e3c'
                            }
                          }} 
                        />
                        <Typography variant="body2" sx={{ mt: 1, color: '#333', fontWeight: 500 }}>
                          Agreement level across professional analysis dimensions
                        </Typography>
                      </Box>

                      <Box sx={{ 
                        display: 'flex', 
                        justifyContent: 'space-around',
                        backgroundColor: '#f8f9fa',
                        p: 2,
                        borderRadius: 2
                      }}>
                        <Box sx={{ textAlign: 'center' }}>
                          <Typography variant="h4" sx={{ fontWeight: 700, color: '#1976d2' }}>
                            {dashboardData.key_actions}
                          </Typography>
                          <Typography variant="body2" sx={{ fontWeight: 600 }}>
                            Action Items
                          </Typography>
                        </Box>
                        <Box sx={{ textAlign: 'center' }}>
                          <Typography variant="h4" sx={{ fontWeight: 700, color: '#d32f2f' }}>
                            {dashboardData.high_risks}
                          </Typography>
                          <Typography variant="body2" sx={{ fontWeight: 600 }}>
                            High Risks
                          </Typography>
                        </Box>
                        <Box sx={{ textAlign: 'center' }}>
                          <Typography variant="h4" sx={{ fontWeight: 700, color: '#f57c00' }}>
                            {dashboardData.timeline?.split(' ')[0] || '3-6'}
                          </Typography>
                          <Typography variant="body2" sx={{ fontWeight: 600 }}>
                            Timeline (Months)
                          </Typography>
                        </Box>
                      </Box>
                    </CardContent>
                  </Card>
                </Grid>
                
                {/* Strategic Summary */}
                <Grid item xs={12} md={4}>
                  <Card sx={{ height: '100%' }}>
                    <CardContent sx={{ p: 3 }}>
                      <Typography variant="h6" sx={{ 
                        mb: 3, 
                        fontWeight: 600,
                        color: '#7b1fa2',
                        display: 'flex',
                        alignItems: 'center'
                      }}>
                        🎯 Strategic Overview
                      </Typography>
                      
                      <Box sx={{ mb: 3 }}>
                        <Typography variant="subtitle1" sx={{ fontWeight: 600, mb: 1, color: '#1976d2' }}>
                          📅 Implementation Framework
                      </Typography>
                        <Typography variant="body1" sx={{ 
                          p: 2, 
                          backgroundColor: '#e3f2fd', 
                          borderRadius: 1,
                          fontWeight: 500
                        }}>
                          {dashboardData.timeline}
                      </Typography>
                      </Box>

                      <Box sx={{ mb: 3 }}>
                        <Typography variant="subtitle1" sx={{ fontWeight: 600, mb: 1, color: '#d32f2f' }}>
                          ⚠️ Risk Assessment
                        </Typography>
                        <Typography variant="body1" sx={{ 
                          p: 2, 
                          backgroundColor: (dashboardData.risk_level === 'High') ? '#ffebee' : 
                                         (dashboardData.risk_level === 'Medium') ? '#fff3e0' : '#e8f5e8',
                          borderRadius: 1,
                          fontWeight: 500,
                          color: (dashboardData.risk_level === 'High') ? '#d32f2f' : 
                                 (dashboardData.risk_level === 'Medium') ? '#f57c00' : '#388e3c'
                        }}>
                          {dashboardData.risk_level} Risk Profile
                        </Typography>
                      </Box>

                      <Box>
                        <Typography variant="subtitle1" sx={{ fontWeight: 600, mb: 1, color: '#388e3c' }}>
                          📈 Success Probability
                        </Typography>
                        <Typography variant="body1" sx={{ 
                          p: 2, 
                          backgroundColor: '#e8f5e8', 
                          borderRadius: 1,
                          fontWeight: 500,
                          textAlign: 'center'
                        }}>
                          {Math.round(dashboardData.quality_score * dashboardData.consensus_strength * 100)}%
                        </Typography>
                        <Typography variant="body2" sx={{ mt: 1, color: '#333', textAlign: 'center', fontWeight: 500 }}>
                          Based on quality score × consensus strength
                        </Typography>
                      </Box>
                    </CardContent>
                  </Card>
                </Grid>
              </Grid>
            ) : (
              <Alert severity="info" sx={{ m: 2 }}>
                <Typography variant="h6" sx={{ fontWeight: 600, mb: 1 }}>
                  📊 Dashboard Preparation
                </Typography>
                Executive dashboard data is being prepared. This includes quality metrics, risk assessment, and strategic overview components.
              </Alert>
            )}
          </TabPanel>
          
          <TabPanel value={activeTab} index={2}>
            {/* Detailed Analysis */}
            <Grid container spacing={3}>
              {/* Analysis Header */}
              <Grid item xs={12}>
                <Card sx={{ 
                  background: 'linear-gradient(135deg, #1565c0 0%, #1976d2 100%)',
                  color: 'white',
                  mb: 2
                }}>
                  <CardContent sx={{ p: 4 }}>
                    <Typography variant="h4" sx={{ 
                      mb: 2, 
                      fontWeight: 600,
                      display: 'flex',
                      alignItems: 'center'
                    }}>
                      <AnalyticsIcon sx={{ mr: 2, fontSize: 36 }} />
                      Detailed Professional Analysis
                    </Typography>
                    <Typography variant="subtitle1" sx={{ color: 'rgba(255,255,255,0.95)' }}>
                      Comprehensive strategic analysis with supporting evidence and methodology
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>

              {/* Strategic Framework */}
              <Grid item xs={12}>
                <Card>
                  <CardContent sx={{ p: 4 }}>
                    <Typography variant="h5" sx={{ 
                      mb: 3, 
                      fontWeight: 600,
                      color: '#1976d2',
                      display: 'flex',
                      alignItems: 'center'
                    }}>
                      🎯 Strategic Decision Framework
                    </Typography>
                    
                    <Grid container spacing={3}>
                      <Grid item xs={12} md={6}>
                        <Box sx={{ p: 3, backgroundColor: '#f8f9fa', borderRadius: 2, height: '100%' }}>
                          <Typography variant="h6" sx={{ fontWeight: 600, mb: 2, color: '#1976d2' }}>
                            📊 Analysis Methodology
                          </Typography>
                          <Typography variant="body1" sx={{ mb: 2 }}>
                            <strong>Framework:</strong> {professionalResponse.professional_decision?.strategic_framework || 'Comprehensive Business Analysis'}
                          </Typography>
                          <Typography variant="body1" sx={{ mb: 2 }}>
                            <strong>Model Used:</strong> {professionalResponse.professional_decision?.model_used || 'Mixtral-8x7B-Instruct'}
                          </Typography>
                          <Typography variant="body1" sx={{ mb: 2 }}>
                            <strong>Analysis Type:</strong> {professionalResponse.professional_decision?.analysis_type || 'Professional Strategic Analysis'}
                          </Typography>
                          <Typography variant="body1">
                            <strong>Confidence Score:</strong> {Math.round((professionalResponse.professional_decision?.confidence_score || 0.85) * 100)}%
                          </Typography>
                        </Box>
                      </Grid>
                      
                      <Grid item xs={12} md={6}>
                        <Box sx={{ p: 3, backgroundColor: '#e8f5e8', borderRadius: 2, height: '100%' }}>
                          <Typography variant="h6" sx={{ fontWeight: 600, mb: 2, color: '#388e3c' }}>
                            🔍 Quality Assessment
                          </Typography>
                          <Typography variant="body1" sx={{ mb: 2 }}>
                            <strong>Decision Quality:</strong> {Math.round(professionalResponse.decision_quality_score * 100)}%
                          </Typography>
                          <Typography variant="body1" sx={{ mb: 2 }}>
                            <strong>Confidence Level:</strong> {formatConfidence(professionalResponse.confidence_level)}
                          </Typography>
                          <Typography variant="body1" sx={{ mb: 2 }}>
                            <strong>Consensus Method:</strong> {professionalResponse.consensus_result?.methodology || 'Professional AI Analysis'}
                          </Typography>
                          <Typography variant="body1">
                            <strong>Analysis Quality:</strong> {professionalResponse.consensus_result?.analysis_quality || 'Professional Grade'}
                          </Typography>
                        </Box>
                      </Grid>
                    </Grid>
                  </CardContent>
                </Card>
              </Grid>
              
              {/* Comprehensive Analysis */}
              <Grid item xs={12}>
                <Card>
                  <CardContent sx={{ p: 4 }}>
                    <Typography variant="h5" sx={{ 
                      mb: 3, 
                      fontWeight: 600,
                      color: '#d32f2f',
                      display: 'flex',
                      alignItems: 'center'
                    }}>
                      📋 Full Strategic Analysis
                    </Typography>
                    
                    {professionalResponse.professional_decision?.full_analysis ? (
                      <Box sx={{ 
                        p: 3, 
                        backgroundColor: '#fafafa', 
                        borderRadius: 2,
                        border: '1px solid #e0e0e0'
                      }}>
                        <Typography variant="body1" sx={{ 
                          whiteSpace: 'pre-wrap',
                          lineHeight: 1.8,
                          fontSize: '1rem',
                          fontFamily: 'Georgia, serif'
                        }}>
                          {professionalResponse.professional_decision.full_analysis}
                        </Typography>
                      </Box>
                    ) : (
                      <Box sx={{ 
                        p: 3, 
                        backgroundColor: '#fff3e0', 
                        borderRadius: 2,
                        border: '1px solid #ffcc02'
                      }}>
                        <Typography variant="body1" sx={{ color: '#f57c00', fontWeight: 500 }}>
                          Detailed analysis is being processed. The executive summary above provides the key strategic insights.
                        </Typography>
                      </Box>
                    )}
                  </CardContent>
                </Card>
              </Grid>

              {/* Executive Report Details */}
              <Grid item xs={12} md={6}>
                <Card sx={{ height: '100%' }}>
                  <CardContent sx={{ p: 3 }}>
                    <Typography variant="h6" sx={{ 
                      mb: 3, 
                      fontWeight: 600,
                      color: '#7b1fa2',
                      display: 'flex',
                      alignItems: 'center'
                    }}>
                      📊 Executive Report Summary
                    </Typography>
                    
                    <Box sx={{ mb: 3 }}>
                      <Typography variant="subtitle1" sx={{ fontWeight: 600, mb: 1, color: '#1976d2' }}>
                        Analysis Provider
                      </Typography>
                      <Typography variant="body1" sx={{ 
                        p: 2, 
                        backgroundColor: '#e3f2fd', 
                        borderRadius: 1
                      }}>
                        {professionalResponse.executive_report?.analysis_provider || 'Professional AI Analysis System'}
                      </Typography>
                    </Box>

                    <Box sx={{ mb: 3 }}>
                      <Typography variant="subtitle1" sx={{ fontWeight: 600, mb: 1, color: '#388e3c' }}>
                        Key Insights
                      </Typography>
                      <Typography variant="body1" sx={{ 
                        p: 2, 
                        backgroundColor: '#e8f5e8', 
                        borderRadius: 1,
                        minHeight: '80px'
                      }}>
                        {professionalResponse.executive_report?.key_insights || 'Strategic insights extracted from comprehensive analysis frameworks'}
                      </Typography>
                    </Box>

                    <Box>
                      <Typography variant="subtitle1" sx={{ fontWeight: 600, mb: 1, color: '#d32f2f' }}>
                        Risk Assessment
                      </Typography>
                      <Typography variant="body1" sx={{ 
                        p: 2, 
                        backgroundColor: '#ffebee', 
                        borderRadius: 1
                      }}>
                        {professionalResponse.executive_report?.risk_summary || professionalResponse.risk_assessment}
                      </Typography>
                    </Box>
                  </CardContent>
                </Card>
              </Grid>
              
              {/* Methodology Details */}
              <Grid item xs={12} md={6}>
                <Card sx={{ height: '100%' }}>
                  <CardContent sx={{ p: 3 }}>
                    <Typography variant="h6" sx={{ 
                      mb: 3, 
                      fontWeight: 600,
                      color: '#f57c00',
                      display: 'flex',
                      alignItems: 'center'
                    }}>
                      🔬 Analysis Methodology
                    </Typography>
                    
                    <Box sx={{ mb: 3 }}>
                      <Typography variant="subtitle1" sx={{ fontWeight: 600, mb: 1, color: '#1976d2' }}>
                        Consensus Building
                      </Typography>
                      <Typography variant="body1" sx={{ 
                        p: 2, 
                        backgroundColor: '#e3f2fd', 
                        borderRadius: 1
                      }}>
                        <strong>Method:</strong> {professionalResponse.consensus_result?.methodology || 'Professional AI Analysis'}<br/>
                        <strong>Confidence:</strong> {professionalResponse.consensus_result?.confidence_level || 'High'}<br/>
                        <strong>Quality:</strong> {professionalResponse.consensus_result?.analysis_quality || 'Professional Grade'}
                      </Typography>
                    </Box>

                    <Box sx={{ mb: 3 }}>
                      <Typography variant="subtitle1" sx={{ fontWeight: 600, mb: 1, color: '#388e3c' }}>
                        Analysis Framework
                      </Typography>
                      <Typography variant="body1" sx={{ 
                        p: 2, 
                        backgroundColor: '#e8f5e8', 
                        borderRadius: 1
                      }}>
                        Multidimensional strategic analysis including market environment, stakeholder impact, risk assessment, and implementability
                      </Typography>
                    </Box>

                    <Box>
                      <Typography variant="subtitle1" sx={{ fontWeight: 600, mb: 1, color: '#d32f2f' }}>
                        Quality Metrics
                      </Typography>
                      <Box sx={{ 
                        p: 2, 
                        backgroundColor: '#ffebee', 
                        borderRadius: 1
                      }}>
                        <Typography variant="body2" sx={{ mb: 1 }}>
                          <strong>Overall Quality:</strong> {Math.round(professionalResponse.decision_quality_score * 100)}%
                        </Typography>
                        <Typography variant="body2" sx={{ mb: 1 }}>
                          <strong>Confidence Level:</strong> {formatConfidence(professionalResponse.confidence_level)}
                        </Typography>
                        <Typography variant="body2">
                          <strong>Consensus Strength:</strong> Professional Grade
                        </Typography>
                      </Box>
                    </Box>
                  </CardContent>
                </Card>
              </Grid>

              {/* Raw Data Section (Expandable) */}
              <Grid item xs={12}>
                <Card>
                  <CardContent sx={{ p: 3 }}>
                    <Typography variant="h6" sx={{ 
                      mb: 2, 
                      fontWeight: 600,
                      color: '#616161',
                      display: 'flex',
                      alignItems: 'center'
                    }}>
                      🔧 Technical Analysis Data
                    </Typography>
                    <Alert severity="info" sx={{ mb: 2 }}>
                      <Typography variant="body2">
                        This section contains raw analysis data for technical review and verification purposes.
                      </Typography>
                    </Alert>
                    
                    <Box sx={{ 
                      backgroundColor: '#f5f5f5', 
                      p: 2, 
                      borderRadius: 1,
                      border: '1px solid #e0e0e0',
                      maxHeight: '400px',
                      overflow: 'auto'
                    }}>
                      <Typography variant="body2" sx={{ fontFamily: 'monospace', fontSize: '0.85rem' }}>
                        <strong>Professional Decision Data:</strong><br/>
                        {JSON.stringify(professionalResponse.professional_decision, null, 2)}
                      </Typography>
                    </Box>
                    
                    <Box sx={{ 
                      backgroundColor: '#f5f5f5', 
                      p: 2, 
                      borderRadius: 1,
                      border: '1px solid #e0e0e0',
                      maxHeight: '400px',
                      overflow: 'auto',
                      mt: 2
                    }}>
                      <Typography variant="body2" sx={{ fontFamily: 'monospace', fontSize: '0.85rem' }}>
                        <strong>Consensus Analysis Data:</strong><br/>
                      {JSON.stringify(professionalResponse.consensus_result, null, 2)}
                      </Typography>
                    </Box>
                  </CardContent>
                </Card>
              </Grid>
            </Grid>
          </TabPanel>
        </Box>
      </div>
    );
  };

  const renderStandardResults = () => {
    if (!decisionResponse) return null;

    return (
      <div className="results-container">
        <Grid container spacing={3}>
          <Grid item xs={12}>
            <Card>
              <CardContent>
                <Typography variant="h5" component="div" sx={{ mb: 2 }}>
                  Decision Council Results
                </Typography>
                <Typography variant="body1" sx={{ mb: 2 }}>
                                      {decisionResponse.final_recommendation || 'Analysis completed'}
                </Typography>
              </CardContent>
            </Card>
          </Grid>
          
          {decisionResponse.initial_responses?.map((response, index) => (
            <Grid item xs={12} md={6} key={index}>
              <Card className="agent-card">
                <CardContent>
                  <Typography variant="h6" sx={{ mb: 1, display: 'flex', alignItems: 'center' }}>
                    <span style={{ marginRight: '8px' }}>{getAgentIcon(response.agent_name)}</span>
                    {response.agent_name}
                  </Typography>
                  <Chip
                    label={response.agent_type}
                    size="small"
                    sx={{ mb: 2, backgroundColor: getAgentColor(response.agent_name), color: 'white' }}
                  />
                  <Typography variant="body2">
                    {response.text_response}
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      </div>
    );
  };

  return (
    <div className="app">
      <div className="container">
        {/* Header */}
        <header className="header">
          <div className="header-content">
            <h1 className="title">
              <span className="title-icon">🧠</span>
              AI Decision Council
              <IconButton 
                onClick={() => setSettingsOpen(true)} 
                style={{ marginLeft: 8, color: 'white' }}
                title="Settings"
              >
                <SettingsIcon />
              </IconButton>
              <IconButton 
                className="history-button"
                onClick={() => {
                  console.log('History button clicked! Opening history panel...');
                  setHistoryOpen(true);
                }} 
                style={{ 
                  marginLeft: 8, 
                  color: 'white',
                  backgroundColor: 'rgba(255,255,255,0.2)',
                  border: '2px solid rgba(255,255,255,0.5)',
                  borderRadius: '8px'
                }}
                title="View decision history (click here!)"
              >
                <HistoryIcon />
              </IconButton>
              {token ? (
                <IconButton onClick={handleLogout} style={{ marginLeft: 8 }} title="Log out">
                  <AccountCircleIcon color="primary" />
                </IconButton>
              ) : (
                <IconButton onClick={() => setAuthOpen(true)} style={{ marginLeft: 8 }} title="Log in/Register">
                  <AccountCircleIcon />
                </IconButton>
              )}
            </h1>
            <p className="subtitle">
              Enterprise-grade decision support with structured methods and professional reporting
            </p>
          </div>
        </header>
        
        <AuthModal open={authOpen} onClose={() => setAuthOpen(false)} onAuthSuccess={handleAuthSuccess} />
        <HistoryPanel open={historyOpen} onClose={() => setHistoryOpen(false)} token={token} />
        <SettingsPanel
          open={settingsOpen}
          onClose={() => setSettingsOpen(false)}
          selectedAgents={selectedAgents}
          onAgentChange={handleAgentChange}
          discussionDepth={discussionDepth}
          onDepthChange={handleDepthChange}
        />

        {/* Main Content */}
        <main className="main-content">
          {!showResults ? (
            <>
              {/* Decision Mode Selection */}
              <div className="mode-selection">
                <Button
                  variant={decisionMode === 'professional' ? 'contained' : 'outlined'}
                  onClick={() => setDecisionMode('professional')}
                  startIcon={<BusinessIcon />}
                  sx={{ mr: 2 }}
                >
                  Professional Analysis
                </Button>
                <Button
                  variant={decisionMode === 'standard' ? 'contained' : 'outlined'}
                  onClick={() => setDecisionMode('standard')}
                  startIcon={<PersonIcon />}
                >
                  Standard Discussion
                </Button>
              </div>

              {/* Input Section */}
              <form onSubmit={handleSubmitDecision} className="decision-form">
                <div className="form-group">
                  <label htmlFor="user-text" className="form-label">
                    {decisionMode === 'professional' ? 'Strategic Decision Question' : 'Decision Question'}
                  </label>
                  <textarea
                    id="user-text"
                    className="form-textarea"
                    rows={4}
                    value={userText}
                    onChange={(e) => setUserText(e.target.value)}
                    placeholder={decisionMode === 'professional' 
                      ? "Example: We are considering a $5M investment in AI transformation over the next 18 months. Should we proceed and how should we structure the implementation?"
                      : "What decision do you need help with? Our AI agents will discuss and provide recommendations."
                    }
                    disabled={isLoading}
                  />
                </div>

                {decisionMode === 'professional' && (
                  <>
                    <Grid container spacing={2} sx={{ mt: 2 }}>
                      <Grid item xs={12} md={6}>
                        <div className="form-group">
                          <label className="form-label">Urgency Level</label>
                          <select
                            className="form-select"
                            value={urgencyLevel}
                            onChange={(e) => setUrgencyLevel(e.target.value)}
                          >
                            <option value="low">Low</option>
                            <option value="medium">Medium</option>
                            <option value="high">High</option>
                            <option value="critical">Critical</option>
                          </select>
                        </div>
                      </Grid>
                      <Grid item xs={12} md={6}>
                        <div className="form-group">
                          <label className="form-label">Decision Framework</label>
                          <select
                            className="form-select"
                            value={decisionFramework}
                            onChange={(e) => setDecisionFramework(e.target.value)}
                          >
                            <option value="auto">Automatic identification</option>
                            <option value="swot">SWOT analysis</option>
                            <option value="cost_benefit">Cost-benefit analysis</option>
                            <option value="risk_reward">Risk-reward analysis</option>
                            <option value="stakeholder">Stakeholder analysis</option>
                            <option value="mece">MECE framework</option>
                          </select>
                        </div>
                      </Grid>
                      <Grid item xs={12}>
                        <div className="form-group">
                          <label className="form-label">Stakeholder Context (Optional)</label>
                          <input
                            type="text"
                            className="form-input"
                            value={stakeholderContext}
                            onChange={(e) => setStakeholderContext(e.target.value)}
                            placeholder="e.g. Board, C-suite, employees, customers"
                          />
                        </div>
                      </Grid>
                      <Grid item xs={12} md={6}>
                        <div className="form-group">
                          <label className="form-label">Budget Constraints (Optional)</label>
                          <input
                            type="text"
                            className="form-input"
                            value={budgetConstraints}
                            onChange={(e) => setBudgetConstraints(e.target.value)}
                            placeholder="e.g. Maximum $5M with quarterly reviews"
                          />
                        </div>
                      </Grid>
                      <Grid item xs={12} md={6}>
                        <div className="form-group">
                          <label className="form-label">Timeline Requirements (Optional)</label>
                          <input
                            type="text"
                            className="form-input"
                            value={timelineRequirements}
                            onChange={(e) => setTimelineRequirements(e.target.value)}
                            placeholder="e.g. Decision needed within 4 weeks"
                          />
                        </div>
                      </Grid>
                    </Grid>
                  </>
                )}

                {error && (
                  <Alert severity="error" sx={{ mt: 2 }}>
                    {error}
                  </Alert>
                )}

                <Button
                  type="submit"
                  variant="contained"
                  size="large"
                  disabled={isLoading || !userText.trim()}
                  sx={{ mt: 3, minWidth: 200 }}
                  startIcon={decisionMode === 'professional' ? <BusinessIcon /> : <PersonIcon />}
                >
                  {isLoading ? 'Analyzing...' : (decisionMode === 'professional' ? 'Get Professional Analysis' : 'Get Council Decision')}
                </Button>
              </form>
            </>
          ) : (
            <>
              {/* Results Section */}
              <div className="results-header">
                <Button
                  onClick={handleNewDecision}
                  variant="outlined"
                  sx={{ mb: 2 }}
                >
                  New Decision
                </Button>
                {professionalResponse && (
                  <Button
                    onClick={() => setExportOpen(true)}
                    variant="outlined"
                    startIcon={<ShareIcon />}
                    sx={{ mb: 2, ml: 2 }}
                  >
                    Export Report
                  </Button>
                )}
              </div>
              
              {decisionMode === 'professional' ? renderProfessionalResults() : renderStandardResults()}
            </>
          )}
        </main>
        
        <ExportModal 
          open={exportOpen} 
          onClose={() => setExportOpen(false)} 
          requestId={professionalResponse?.request_id}
          isProfessional={decisionMode === 'professional'}
        />
      </div>
    </div>
  );
}

export default App;
