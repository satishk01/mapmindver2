# AWS EC2 Deployment Guide

This guide will help you deploy the application on AWS EC2 with role-based access for AWS Bedrock models.

## Prerequisites

- AWS Account with appropriate permissions
- Basic knowledge of AWS EC2, IAM, and S3

## Step 1: Create IAM Role for EC2

### 1.1 Create IAM Policy

Create a custom policy named `BedrockAnalyticsPolicy`:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "bedrock:InvokeModel",
                "bedrock:ListFoundationModels"
            ],
            "Resource": [
                "arn:aws:bedrock:*::foundation-model/anthropic.claude-3-5-sonnet-20241022-v2:0",
                "arn:aws:bedrock:*::foundation-model/us.twelvelabs.pegasus-1-2-v1:0"
            ]
        },
        {
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:PutObject",
                "s3:DeleteObject",
                "s3:ListBucket"
            ],
            "Resource": [
                "arn:aws:s3:::your-bucket-name",
                "arn:aws:s3:::your-bucket-name/*"
            ]
        },
        {
            "Effect": "Allow",
            "Action": [
                "textract:StartDocumentAnalysis",
                "textract:GetDocumentAnalysis",
                "textract:StartDocumentTextDetection",
                "textract:GetDocumentTextDetection"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "sts:GetCallerIdentity"
            ],
            "Resource": "*"
        }
    ]
}
```

### 1.2 Create IAM Role

1. Go to IAM Console → Roles → Create Role
2. Select "AWS Service" → "EC2"
3. Attach the `BedrockAnalyticsPolicy` you created
4. Name the role: `EC2-BedrockAnalytics-Role`

## Step 2: Request Bedrock Model Access

1. Go to AWS Bedrock Console
2. Navigate to "Model access" in the left sidebar
3. Request access to:
   - **Anthropic Claude 3.5 Sonnet** (`anthropic.claude-3-5-sonnet-20241022-v2:0`)
   - **Twelve Labs Pegasus** (`us.twelvelabs.pegasus-1-2-v1:0`)
4. Wait for approval (Claude is usually instant, Pegasus may take 1-2 business days)

## Step 3: Create S3 Bucket

1. Go to S3 Console
2. Create a new bucket (e.g., `your-app-analytics-bucket`)
3. Enable versioning (recommended)
4. Set appropriate bucket policy if needed
5. Note the bucket name for configuration

## Step 4: Launch EC2 Instance

### 4.1 Instance Configuration

1. **AMI**: Ubuntu 22.04 LTS or Amazon Linux 2023
2. **Instance Type**: t3.medium or larger (recommended: t3.large for better performance)
3. **Key Pair**: Create or select existing key pair
4. **Security Group**: 
   - SSH (22) from your IP
   - HTTP (80) from anywhere (0.0.0.0/0)
   - HTTPS (443) from anywhere (0.0.0.0/0)
   - Custom TCP (8000) from anywhere (for FastAPI backend)
   - Custom TCP (3000) from anywhere (for React frontend)

### 4.2 Attach IAM Role

1. In "Advanced details" section
2. Select the `EC2-BedrockAnalytics-Role` you created

## Step 5: Connect and Setup Instance

### 5.1 Connect to Instance

```bash
ssh -i your-key.pem ubuntu@your-ec2-public-ip
```

### 5.2 Update System

```bash
sudo apt update && sudo apt upgrade -y
```

### 5.3 Install Dependencies

```bash
# Install Python 3.11+
sudo apt install python3.11 python3.11-venv python3-pip -y

# Install Node.js 18+
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Install Git
sudo apt install git -y

# Install additional system dependencies
sudo apt install build-essential libssl-dev libffi-dev python3-dev -y
```

## Step 6: Clone and Setup Application

### 6.1 Clone Repository

```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo
```

### 6.2 Setup Backend

```bash
cd backend

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt
```

### 6.3 Setup Frontend

```bash
cd ../frontend

# Install Node.js dependencies
npm install

# Build for production
npm run build
```

## Step 7: Configure Environment

### 7.1 Create Backend Environment File

```bash
cd ../backend
cp .env.example .env
nano .env
```

Configure the `.env` file:

```bash
# MongoDB Configuration (use MongoDB Atlas or local MongoDB)
mongo_db_url=mongodb://localhost:27017/analytics

# AWS Configuration (leave empty - using IAM role)
aws_access_key_id=
aws_secret_access_key=
bucket_name=your-app-analytics-bucket
AWS_REGION=us-east-1

# Bedrock Configuration
USE_BEDROCK_ONLY=true

# Optional: Keep these empty if using Bedrock only
openai_api_key=
gemini_api_key=
gcp_project_id=
```

## Step 8: Install and Configure MongoDB

### 8.1 Install MongoDB

```bash
# Import MongoDB public key
wget -qO - https://www.mongodb.org/static/pgp/server-7.0.asc | sudo apt-key add -

# Add MongoDB repository
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/7.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-7.0.list

# Update and install
sudo apt update
sudo apt install -y mongodb-org

# Start and enable MongoDB
sudo systemctl start mongod
sudo systemctl enable mongod
```

## Step 9: Setup Process Management

### 9.1 Install PM2

```bash
sudo npm install -g pm2
```

### 9.2 Create PM2 Configuration

Create `ecosystem.config.js` in the project root:

```javascript
module.exports = {
  apps: [
    {
      name: 'analytics-backend',
      cwd: './backend',
      script: 'uvicorn',
      args: 'app:app --host 0.0.0.0 --port 8000',
      interpreter: './venv/bin/python',
      env: {
        NODE_ENV: 'production'
      }
    },
    {
      name: 'analytics-frontend',
      cwd: './frontend',
      script: 'npx',
      args: 'serve -s dist -l 3000',
      env: {
        NODE_ENV: 'production'
      }
    }
  ]
};
```

## Step 10: Setup Nginx (Optional)

### 10.1 Install Nginx

```bash
sudo apt install nginx -y
```

### 10.2 Configure Nginx

Create `/etc/nginx/sites-available/analytics`:

```nginx
server {
    listen 80;
    server_name your-domain.com;  # Replace with your domain or EC2 public IP

    # Frontend
    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }

    # Backend API
    location /api/ {
        proxy_pass http://localhost:8000/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
        
        # Increase timeout for large file uploads
        proxy_read_timeout 300s;
        proxy_connect_timeout 75s;
    }

    # Increase max body size for file uploads
    client_max_body_size 100M;
}
```

Enable the site:

```bash
sudo ln -s /etc/nginx/sites-available/analytics /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## Step 11: Start Application

### 11.1 Start with PM2

```bash
# From project root directory
pm2 start ecosystem.config.js

# Save PM2 configuration
pm2 save

# Setup PM2 to start on boot
pm2 startup
# Follow the instructions provided by the command above
```

### 11.2 Check Status

```bash
pm2 status
pm2 logs
```

## Step 12: Configure SSL (Optional but Recommended)

### 12.1 Install Certbot

```bash
sudo apt install certbot python3-certbot-nginx -y
```

### 12.2 Get SSL Certificate

```bash
sudo certbot --nginx -d your-domain.com
```

## Step 13: Monitoring and Maintenance

### 13.1 Setup Log Rotation

```bash
sudo nano /etc/logrotate.d/analytics
```

Add:

```
/home/ubuntu/your-repo/backend/logs/*.log {
    daily
    missingok
    rotate 52
    compress
    delaycompress
    notifempty
    create 644 ubuntu ubuntu
}
```

### 13.2 Setup Monitoring

```bash
# Monitor PM2 processes
pm2 monit

# Check system resources
htop

# Monitor logs
pm2 logs --lines 100
```

## Step 14: Testing the Deployment

### 14.1 Test Backend

```bash
curl http://your-ec2-ip:8000/docs
```

### 14.2 Test Frontend

Open browser and navigate to:
- `http://your-ec2-ip` (if using Nginx)
- `http://your-ec2-ip:3000` (direct access)

### 14.3 Test Bedrock Integration

1. Create a new flow in the application
2. Upload an image/video/audio file
3. Verify it processes using Bedrock models
4. Check logs for any errors:
   ```bash
   pm2 logs analytics-backend
   ```

## Troubleshooting

### Common Issues

1. **Bedrock Access Denied**:
   - Verify IAM role is attached to EC2 instance
   - Check model access in Bedrock console
   - Ensure correct region configuration

2. **S3 Access Issues**:
   - Verify bucket name in environment variables
   - Check IAM permissions for S3

3. **MongoDB Connection Issues**:
   - Ensure MongoDB is running: `sudo systemctl status mongod`
   - Check connection string in `.env`

4. **Port Access Issues**:
   - Verify security group settings
   - Check if ports are open: `sudo netstat -tlnp`

5. **File Upload Issues**:
   - Check Nginx client_max_body_size
   - Verify disk space: `df -h`

### Useful Commands

```bash
# Check application status
pm2 status

# Restart applications
pm2 restart all

# View logs
pm2 logs

# Check system resources
htop
df -h

# Check network connections
sudo netstat -tlnp

# Test AWS credentials
aws sts get-caller-identity

# Test Bedrock access
aws bedrock list-foundation-models --region us-east-1
```

## Security Considerations

1. **Keep system updated**:
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```

2. **Configure firewall**:
   ```bash
   sudo ufw enable
   sudo ufw allow ssh
   sudo ufw allow 80
   sudo ufw allow 443
   ```

3. **Regular backups**:
   - Setup automated MongoDB backups
   - Consider EBS snapshots for the EC2 instance

4. **Monitor logs**:
   - Setup CloudWatch for log monitoring
   - Configure alerts for errors

## Cost Optimization

1. **Use appropriate instance size**:
   - Start with t3.medium, scale as needed
   - Consider Reserved Instances for long-term use

2. **Monitor Bedrock usage**:
   - Set up billing alerts
   - Monitor token usage in CloudWatch

3. **Optimize S3 storage**:
   - Use lifecycle policies for old files
   - Consider S3 Intelligent Tiering

This completes the AWS EC2 deployment guide. Your application should now be running with AWS Bedrock models for AI processing.