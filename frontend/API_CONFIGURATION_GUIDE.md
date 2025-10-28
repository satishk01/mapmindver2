# API Configuration Guide

This guide explains how to manage the API endpoint configuration for the GenAI Mind Map Flow Builder frontend.

## Current Configuration

The frontend is currently configured to connect to the EC2 backend at:
- **Production URL**: `http://184.73.104.73:8000`
- **Development URL**: `http://localhost:8000` (for local backend development)

## Configuration Files

### 1. Environment Files
- `.env` - Default environment configuration
- `.env.development` - Local development configuration  
- `.env.production` - Production configuration

### 2. Configuration JSON
- `config.json` - Centralized configuration with multiple environments

### 3. Configuration Manager
- `src/config/config-manager.js` - Dynamic configuration management
- `src/config/api.js` - Main API configuration

## Updating the IP Address

### Method 1: Using the Update Script (Recommended)

```bash
# Navigate to the frontend directory
cd frontend

# Run the update script with the new IP address
node update-ip.js 54.123.45.67

# Restart the development server
npm run dev
```

### Method 2: Manual Update

1. **Update Environment Files**:
   ```bash
   # Edit .env
   VITE_API_URL=http://YOUR_NEW_IP:8000
   
   # Edit .env.production
   VITE_API_URL=http://YOUR_NEW_IP:8000
   ```

2. **Update config.json**:
   ```json
   {
     "production": {
       "apiUrl": "http://YOUR_NEW_IP:8000"
     }
   }
   ```

3. **Restart the frontend**:
   ```bash
   npm run dev
   ```

## Verification

After updating the configuration:

1. **Check Browser Console**: Look for configuration logs:
   ```
   🔗 API Base URL: http://YOUR_NEW_IP:8000
   🔧 Configuration Manager Loaded: {...}
   ```

2. **Test Flow Creation**: 
   - Click the drawer icon (hamburger menu)
   - Click "NEW" to create a flow
   - Select "Manual" or "Automatic"
   - Verify the flow is created successfully

3. **Check Network Tab**: Verify API calls are going to the correct endpoint

## Troubleshooting

### Flow Creation Disabled
- **Cause**: Backend not accessible or wrong IP configuration
- **Solution**: 
  1. Verify backend is running on EC2
  2. Check IP address is correct
  3. Ensure port 8000 is accessible
  4. Check browser console for API errors

### CORS Issues
- **Cause**: Backend CORS configuration
- **Solution**: Ensure backend allows requests from frontend domain

### Environment Variables Not Loading
- **Cause**: Vite environment variable naming
- **Solution**: Ensure variables start with `VITE_`

## Development vs Production

- **Development**: Uses `http://localhost:8000` for local backend testing
- **Production**: Uses EC2 IP address for deployed backend

The configuration automatically detects the environment and uses the appropriate endpoint.

## Security Notes

- Never commit sensitive API keys to version control
- Use environment variables for sensitive configuration
- Consider using HTTPS in production environments
- Regularly update IP addresses when EC2 instances change