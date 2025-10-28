// Configuration Manager for Dynamic IP Updates
// This file helps manage API endpoints dynamically

import configData from '../../config.json';

/**
 * Get the current environment (development, production, staging)
 */
export const getCurrentEnvironment = () => {
  // Check if we're in development mode
  if (import.meta.env.DEV) {
    return 'development';
  }
  
  // Check for explicit environment variable
  const env = import.meta.env.VITE_ENVIRONMENT;
  if (env && configData[env]) {
    return env;
  }
  
  // Default to production
  return 'production';
};

/**
 * Get API URL for the current environment
 */
export const getApiUrl = () => {
  const env = getCurrentEnvironment();
  
  // First check environment variables
  const envApiUrl = import.meta.env.VITE_API_URL;
  if (envApiUrl) {
    return envApiUrl;
  }
  
  // Fallback to config file
  return configData[env]?.apiUrl || configData.production.apiUrl;
};

/**
 * Update configuration (for future use with admin panel)
 */
export const updateConfig = (environment, newApiUrl) => {
  console.log(`Configuration update requested: ${environment} -> ${newApiUrl}`);
  // This would require a backend endpoint to update the config file
  // For now, just log the request
};

/**
 * Get all available environments
 */
export const getAvailableEnvironments = () => {
  return Object.keys(configData).filter(key => key !== 'notes');
};

/**
 * Get configuration info for debugging
 */
export const getConfigInfo = () => {
  return {
    currentEnvironment: getCurrentEnvironment(),
    currentApiUrl: getApiUrl(),
    availableEnvironments: getAvailableEnvironments(),
    configData: configData
  };
};

// Log configuration on import for debugging
console.log('🔧 Configuration Manager Loaded:', getConfigInfo());