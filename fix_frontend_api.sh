#!/bin/bash

# Script to update frontend API URLs for EC2 deployment
# Usage: ./fix_frontend_api.sh YOUR_EC2_PUBLIC_IP

if [ -z "$1" ]; then
    echo "Usage: $0 <EC2_PUBLIC_IP>"
    echo "Example: $0 54.123.45.67"
    exit 1
fi

EC2_IP=$1

echo "🔧 Updating frontend API URLs to use EC2 IP: $EC2_IP"

# Navigate to frontend directory
cd frontend

# Create backup
echo "📁 Creating backup of original files..."
mkdir -p backup
find src -name "*.jsx" -o -name "*.js" | xargs -I {} cp {} backup/

# Replace localhost:8000 with EC2 IP
echo "🔄 Replacing localhost:8000 with $EC2_IP:8000..."
find src -name "*.jsx" -o -name "*.js" | xargs sed -i "s|http://localhost:8000|http://$EC2_IP:8000|g"

echo "✅ Frontend API URLs updated!"
echo ""
echo "📋 Next steps:"
echo "1. Build the frontend: npm run build"
echo "2. Serve the built files or deploy to your web server"
echo ""
echo "🔄 To revert changes:"
echo "cp backup/* src/ (restore from backup)"