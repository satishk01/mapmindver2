// API Configuration for different environments
import { getApiUrl, getConfigInfo } from './config-manager.js';

const getApiBaseUrl = () => {
  const apiUrl = getApiUrl();
  
  console.log('🔧 Using API URL:', apiUrl);
  console.log('🔧 Environment Mode:', import.meta.env.MODE);
  
  return apiUrl;
};

export const API_BASE_URL = getApiBaseUrl();

// Helper function to create full API URLs
export const createApiUrl = (endpoint) => {
  // Remove leading slash if present to avoid double slashes
  const cleanEndpoint = endpoint.startsWith('/') ? endpoint.slice(1) : endpoint;
  const fullUrl = `${API_BASE_URL}/${cleanEndpoint}`;
  console.log('🌐 API Call to:', fullUrl);
  return fullUrl;
};

// Export configuration info for debugging
export const getApiConfig = () => getConfigInfo();

// Log the API URL for debugging
console.log('🔗 API Base URL:', API_BASE_URL);
console.log('🔗 Full Config:', getConfigInfo());

// Test API connection on load
fetch(`${API_BASE_URL}/flows/`)
  .then(response => {
    console.log('✅ API Connection Test Success:', response.status);
    return response.json();
  })
  .then(data => {
    console.log('📊 Current flows:', data);
  })
  .catch(error => {
    console.error('❌ API Connection Test Failed:', error);
  });