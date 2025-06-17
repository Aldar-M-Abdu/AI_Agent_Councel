// Configuration for the frontend application
const config = {
  // API Base URL - automatically detects environment
  API_BASE_URL: process.env.REACT_APP_API_URL || 
    (process.env.NODE_ENV === 'production' 
      ? window.location.origin  // Use same origin in production
      : 'http://127.0.0.1:8000' // Development backend URL - Fixed port to 8000
    ),
  
  // Legacy property name for backward compatibility
  get apiUrl() {
    return this.API_BASE_URL;
  },
  
  // Other configuration options
  DEFAULT_TIMEOUT: 30000, // 30 seconds
  RETRY_ATTEMPTS: 3,
};

export default config; 