// API Configuration for different environments

const getApiBaseUrl = () => {
  // Use environment variable if set
  const apiUrl = import.meta.env.VITE_API_URL;
  
  if (apiUrl && apiUrl !== 'http://YOUR_EC2_PUBLIC_IP:8000') {
    return apiUrl;
  }
  
  // Fallback to localhost for development
  return 'http://localhost:8000';
};

export const API_BASE_URL = getApiBaseUrl();

// Helper function to create full API URLs
export const createApiUrl = (endpoint) => {
  // Remove leading slash if present to avoid double slashes
  const cleanEndpoint = endpoint.startsWith('/') ? endpoint.slice(1) : endpoint;
  return `${API_BASE_URL}/${cleanEndpoint}`;
};

// Log the API URL for debugging
console.log('🔗 API Base URL:', API_BASE_URL);