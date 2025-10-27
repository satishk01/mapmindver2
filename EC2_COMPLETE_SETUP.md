# Complete EC2 Setup Guide

## The Problem
The frontend React app is hardcoded to connect to `localhost:8000`, which won't work when the backend is on EC2.

## Solutions (Choose One)

### Solution 1: Environment-Based Configuration (Recommended)

1. **Update the production environment file:**
   ```bash
   cd frontend
   nano .env.production
   ```
   
   Replace `YOUR_EC2_PUBLIC_IP` with your actual EC2 public IP:
   ```env
   VITE_API_URL=http://54.123.45.67:8000
   ```

2. **Update one frontend file to use the API config:**
   
   Edit `frontend/src/modals/FlowModal.jsx` (as an example):
   ```javascript
   // Add this import at the top
   import { API_BASE_URL } from '../config/api';
   
   // Replace this line:
   // .post(`http://localhost:8000/create-flow`, data, {
   
   // With this:
   .post(`${API_BASE_URL}/create-flow`, data, {
   ```

3. **Build for production:**
   ```bash
   npm run build
   ```

### Solution 2: Quick Fix Script (Fastest)

1. **Run the fix script:**
   ```bash
   chmod +x fix_frontend_api.sh
   ./fix_frontend_api.sh YOUR_EC2_PUBLIC_IP
   ```
   
   Example:
   ```bash
   ./fix_frontend_api.sh 54.123.45.67
   ```

2. **Build the frontend:**
   ```bash
   cd frontend
   npm run build
   ```

### Solution 3: Nginx Proxy (Production Ready)

1. **Keep localhost in frontend code**
2. **Configure Nginx to proxy API calls:**
   
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;
       
       # Serve frontend
       location / {
           root /path/to/frontend/dist;
           try_files $uri $uri/ /index.html;
       }
       
       # Proxy API calls to backend
       location /api/ {
           proxy_pass http://localhost:8000/;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

3. **Update frontend to use `/api/` prefix:**
   ```javascript
   // Instead of: http://localhost:8000/create-flow
   // Use: /api/create-flow
   ```

## Complete Deployment Steps

### Step 1: Backend Setup
```bash
# On your EC2 instance
cd backend
cp .env.bedrock .env
# Edit .env to set your S3 bucket name

# Install dependencies
pip install fastapi uvicorn pymongo boto3 python-dotenv pandas langchain chromadb

# Test
python test_import.py
python test_bedrock.py

# Start backend
uvicorn app:app --host 0.0.0.0 --port 8000
```

### Step 2: Frontend Setup

**Option A: Build and serve on EC2**
```bash
# On your EC2 instance
cd frontend

# Update API URL
echo "VITE_API_URL=http://$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4):8000" > .env.production

# Install dependencies and build
npm install
npm run build

# Serve the built files
npx serve -s dist -l 3000
```

**Option B: Build locally and upload**
```bash
# On your local machine
cd frontend

# Update API URL with your EC2 IP
echo "VITE_API_URL=http://YOUR_EC2_PUBLIC_IP:8000" > .env.production

# Build
npm install
npm run build

# Upload dist folder to EC2
scp -r dist/ ec2-user@YOUR_EC2_IP:/home/ec2-user/frontend-dist/
```

### Step 3: Configure Security Groups

Make sure your EC2 security group allows:
- Port 22 (SSH)
- Port 8000 (Backend API)
- Port 3000 (Frontend, if serving from EC2)
- Port 80/443 (HTTP/HTTPS, if using Nginx)

### Step 4: Access Your Application

- **Backend API docs**: `http://YOUR_EC2_IP:8000/docs`
- **Frontend**: `http://YOUR_EC2_IP:3000` (if serving from EC2)

## Testing the Connection

1. **Test backend directly:**
   ```bash
   curl http://YOUR_EC2_IP:8000/flows
   ```

2. **Test from browser:**
   - Open browser developer tools (F12)
   - Go to Network tab
   - Try creating a flow in the frontend
   - Check if API calls are going to the correct IP

## Troubleshooting

### Frontend can't connect to backend:
1. Check EC2 security groups
2. Verify backend is running on 0.0.0.0:8000 (not 127.0.0.1)
3. Check if API URL is correct in frontend

### CORS errors:
The backend already has CORS enabled for all origins, so this shouldn't be an issue.

### Connection refused:
1. Make sure backend is running
2. Check if port 8000 is open in security groups
3. Verify the EC2 public IP is correct

## Production Recommendations

1. **Use a domain name** instead of IP address
2. **Set up SSL/HTTPS** with Let's Encrypt
3. **Use Nginx** as reverse proxy
4. **Set up PM2** for process management
5. **Configure proper logging** and monitoring

This setup will allow your React frontend to properly communicate with the FastAPI backend running on EC2!