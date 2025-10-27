#!/bin/bash

echo "🚀 Setting up Bedrock-only mode..."

# Navigate to backend directory
cd backend

# Copy Bedrock configuration
if [ -f ".env.bedrock" ]; then
    cp .env.bedrock .env
    echo "✅ Copied Bedrock configuration to .env"
else
    echo "❌ .env.bedrock file not found"
    exit 1
fi

# Update bucket name if provided
if [ ! -z "$1" ]; then
    sed -i "s/your-s3-bucket-name/$1/g" .env
    echo "✅ Updated S3 bucket name to: $1"
else
    echo "⚠️  Please update the bucket_name in .env file"
fi

# Test the configuration
echo ""
echo "🔍 Testing configuration..."
python test_import.py

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 Bedrock-only mode setup complete!"
    echo ""
    echo "Next steps:"
    echo "1. Make sure your S3 bucket name is correct in .env"
    echo "2. Ensure your EC2 instance has the proper IAM role"
    echo "3. Start the app: python start_app.py"
    echo ""
    echo "To test Bedrock access: python test_bedrock.py"
else
    echo ""
    echo "❌ Setup failed. Please check the errors above."
fi