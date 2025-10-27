# Frontend API Configuration

This document explains how to configure the frontend to connect to your backend API, whether it's running locally or on an EC2 instance.

## Overview

The frontend has been updated to use environment variables for API endpoints instead of hardcoded URLs. This allows you to easily switch between local development and production environments.

## Environment Files

The frontend uses three environment files:

- `.env` - Default configuration (used when no specific environment is detected)
- `.env.development` - Local development configuration
- `.env.production` - Production configuration

## Configuration Options

### For Local Development
The `.env.development` file is already configured for local development:
```
VITE_API_URL=http://localhost:8000
```

### For EC2 Deployment
Update the `.env` and `.env.production` files with your EC2 public IP address:
```
VITE_API_URL=http://YOUR_EC2_PUBLIC_IP:8000
```

## Quick Setup

### Option 1: Manual Update
1. Open `frontend/.env` and `frontend/.env.production`
2. Replace `YOUR_EC2_PUBLIC_IP` with your actual EC2 public IP address
3. Example: `VITE_API_URL=http://54.123.45.67:8000`

### Option 2: Using the Update Script

#### On Linux/Mac:
```bash
cd frontend
./update-api-url.sh 54.123.45.67
```

#### On Windows:
```cmd
cd frontend
update-api-url.bat 54.123.45.67
```

## How It Works

The frontend now uses a centralized API configuration in `src/config/api.js`:

```javascript
const getApiBaseUrl = () => {
  const apiUrl = import.meta.env.VITE_API_URL;
  
  if (apiUrl && apiUrl !== 'http://YOUR_EC2_PUBLIC_IP:8000') {
    return apiUrl;
  }
  
  // Fallback to localhost for development
  return 'http://localhost:8000';
};

export const API_BASE_URL = getApiBaseUrl();
export const createApiUrl = (endpoint) => {
  const cleanEndpoint = endpoint.startsWith('/') ? endpoint.slice(1) : endpoint;
  return `${API_BASE_URL}/${cleanEndpoint}`;
};
```

All API calls throughout the application now use the `createApiUrl()` function to construct the full URL.

## Verification

After updating the configuration, you can verify it's working by:

1. Opening the browser developer console
2. Looking for the log message: `🔗 API Base URL: http://YOUR_IP:8000`
3. Checking that API calls in the Network tab use the correct URL

## Troubleshooting

### Common Issues

1. **API calls still going to localhost**: Make sure you've updated the environment files and restarted your development server.

2. **CORS errors**: Ensure your backend is configured to accept requests from your frontend domain.

3. **Environment variables not loading**: Make sure your environment files are in the `frontend/` directory and start with `VITE_`.

### Environment Priority

Vite loads environment files in this order:
1. `.env.production` (in production mode)
2. `.env.development` (in development mode)  
3. `.env` (always loaded)

Variables in files loaded later will override those loaded earlier.

## Security Notes

- Never commit sensitive information to environment files
- Use different configurations for development, staging, and production
- Consider using environment-specific secrets management for production deployments

## Next Steps

After configuring the API URL:

1. **Development**: Run `npm run dev` to start the development server
2. **Production**: Run `npm run build` to create a production build
3. **Deploy**: Upload the built files to your web server

The frontend will automatically use the correct API endpoint based on your configuration.