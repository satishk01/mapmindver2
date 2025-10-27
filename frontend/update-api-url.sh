#!/bin/bash

# Script to update API URL in frontend environment files
# Usage: ./update-api-url.sh YOUR_EC2_PUBLIC_IP

if [ $# -eq 0 ]; then
    echo "Usage: $0 <EC2_PUBLIC_IP>"
    echo "Example: $0 54.123.45.67"
    exit 1
fi

EC2_IP=$1

# Validate IP format (basic check)
if [[ ! $EC2_IP =~ ^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$ ]]; then
    echo "Error: Invalid IP address format. Please provide a valid IP address."
    echo "Example: 54.123.45.67"
    exit 1
fi

echo "Updating API URL to: http://$EC2_IP:8000"

# Update .env file
sed -i "s/YOUR_EC2_PUBLIC_IP/$EC2_IP/g" .env
echo "Updated .env"

# Update .env.production file
sed -i "s/YOUR_EC2_PUBLIC_IP/$EC2_IP/g" .env.production
echo "Updated .env.production"

echo "✅ API URL updated successfully!"
echo "Frontend will now use: http://$EC2_IP:8000"
echo ""
echo "Next steps:"
echo "1. Restart your frontend development server if it's running"
echo "2. Build and deploy your frontend for production"