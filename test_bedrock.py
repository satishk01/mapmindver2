#!/usr/bin/env python3
"""
Test AWS Bedrock Claude connection
"""
import boto3
import json
import os
from dotenv import load_dotenv

load_dotenv()

def test_bedrock_connection():
    """Test if Bedrock Claude is accessible"""
    print("🧪 Testing AWS Bedrock Connection")
    print("=" * 40)
    
    # Check environment variables
    aws_region = os.getenv('AWS_REGION', 'us-east-1')
    use_bedrock = os.getenv('USE_BEDROCK_ONLY', 'false').lower() == 'true'
    
    print(f"AWS_REGION: {aws_region}")
    print(f"USE_BEDROCK_ONLY: {use_bedrock}")
    
    if not use_bedrock:
        print("⚠️  USE_BEDROCK_ONLY is not set to true")
        return False
    
    try:
        # Initialize Bedrock client
        print("🔧 Initializing Bedrock client...")
        bedrock_runtime_client = boto3.client(
            'bedrock-runtime',
            region_name=aws_region
        )
        
        # Test simple Claude request
        print("🤖 Testing Claude API call...")
        request_body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 100,
            "messages": [
                {
                    "role": "user",
                    "content": "Hello, please respond with 'Claude is working correctly!'"
                }
            ]
        }
        
        response = bedrock_runtime_client.invoke_model(
            modelId="anthropic.claude-3-5-sonnet-20241022-v2:0",
            body=json.dumps(request_body),
            contentType="application/json",
            accept="application/json"
        )
        
        response_body = json.loads(response["body"].read())
        claude_response = response_body["content"][0]["text"]
        
        print(f"✅ Claude Response: {claude_response}")
        return True
        
    except Exception as e:
        print(f"❌ Bedrock connection failed: {e}")
        print("\nPossible issues:")
        print("1. AWS credentials not configured")
        print("2. Bedrock not available in your region")
        print("3. Claude model not accessible")
        print("4. Network connectivity issues")
        return False

def test_aws_credentials():
    """Test AWS credentials"""
    print("\n🔑 Testing AWS Credentials")
    print("=" * 30)
    
    try:
        sts_client = boto3.client('sts')
        identity = sts_client.get_caller_identity()
        print(f"✅ AWS Account: {identity.get('Account', 'Unknown')}")
        print(f"✅ User/Role: {identity.get('Arn', 'Unknown')}")
        return True
    except Exception as e:
        print(f"❌ AWS credentials test failed: {e}")
        print("\nPlease configure AWS credentials:")
        print("1. aws configure")
        print("2. Set environment variables")
        print("3. Use IAM roles (if on EC2)")
        return False

if __name__ == "__main__":
    print("🚀 AWS Bedrock Diagnostic Test")
    print("=" * 50)
    
    # Test AWS credentials first
    if not test_aws_credentials():
        exit(1)
    
    # Test Bedrock connection
    if not test_bedrock_connection():
        exit(1)
    
    print("\n✅ All tests passed! Bedrock should work correctly.")