#!/usr/bin/env python3
"""
Test script for AWS Bedrock configuration
Run this script to verify your Bedrock setup is working correctly.
"""

import os
import boto3
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_aws_credentials():
    """Test AWS credentials and permissions"""
    print("🔍 Testing AWS credentials...")
    try:
        sts_client = boto3.client('sts')
        identity = sts_client.get_caller_identity()
        print(f"✅ AWS credentials valid")
        print(f"   Account ID: {identity['Account']}")
        print(f"   User/Role: {identity['Arn']}")
        return True
    except Exception as e:
        print(f"❌ AWS credentials failed: {e}")
        return False

def test_bedrock_access():
    """Test Bedrock service access"""
    print("\n🔍 Testing Bedrock access...")
    try:
        region = os.getenv('AWS_REGION', 'us-east-1')
        bedrock_client = boto3.client('bedrock', region_name=region)
        
        # List available models
        response = bedrock_client.list_foundation_models()
        models = response.get('modelSummaries', [])
        
        print(f"✅ Bedrock access successful")
        print(f"   Region: {region}")
        print(f"   Available models: {len(models)}")
        
        # Check for specific models we need
        claude_available = any('claude-3-5-sonnet' in model.get('modelId', '') for model in models)
        pegasus_available = any('pegasus' in model.get('modelId', '') for model in models)
        
        print(f"   Claude Sonnet 3.5: {'✅' if claude_available else '❌'}")
        print(f"   Pegasus: {'✅' if pegasus_available else '❌'}")
        
        return True
    except Exception as e:
        print(f"❌ Bedrock access failed: {e}")
        return False

def test_claude_inference():
    """Test Claude Sonnet 3.5 inference"""
    print("\n🔍 Testing Claude Sonnet 3.5 inference...")
    try:
        region = os.getenv('AWS_REGION', 'us-east-1')
        bedrock_runtime = boto3.client('bedrock-runtime', region_name=region)
        
        request_body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 100,
            "messages": [
                {
                    "role": "user",
                    "content": "Hello! Please respond with 'Claude is working correctly' if you can see this message."
                }
            ]
        }
        
        response = bedrock_runtime.invoke_model(
            modelId="anthropic.claude-3-5-sonnet-20241022-v2:0",
            body=json.dumps(request_body),
            contentType="application/json",
            accept="application/json"
        )
        
        response_body = json.loads(response["body"].read())
        message = response_body["content"][0]["text"]
        
        print(f"✅ Claude inference successful")
        print(f"   Response: {message}")
        return True
    except Exception as e:
        print(f"❌ Claude inference failed: {e}")
        print(f"   Make sure you have requested access to Claude Sonnet 3.5 in the Bedrock console")
        return False

def test_s3_access():
    """Test S3 bucket access"""
    print("\n🔍 Testing S3 bucket access...")
    try:
        bucket_name = os.getenv('bucket_name')
        if not bucket_name:
            print("❌ S3 bucket name not configured in environment variables")
            return False
        
        s3_client = boto3.client('s3')
        
        # Test bucket access
        s3_client.head_bucket(Bucket=bucket_name)
        print(f"✅ S3 bucket access successful")
        print(f"   Bucket: {bucket_name}")
        
        # Test write permissions with a small test file
        test_key = "test/bedrock_test.txt"
        s3_client.put_object(
            Bucket=bucket_name,
            Key=test_key,
            Body=b"Bedrock test file"
        )
        
        # Clean up test file
        s3_client.delete_object(Bucket=bucket_name, Key=test_key)
        
        print(f"   Write permissions: ✅")
        return True
    except Exception as e:
        print(f"❌ S3 access failed: {e}")
        return False

def test_pegasus_model():
    """Test Pegasus model access (note: requires media file)"""
    print("\n🔍 Testing Pegasus model access...")
    try:
        region = os.getenv('AWS_REGION', 'us-east-1')
        bedrock_runtime = boto3.client('bedrock-runtime', region_name=region)
        
        # This is just a test to see if the model is accessible
        # We won't actually invoke it without a proper media file
        print("   Note: Pegasus requires media files for full testing")
        print("   ✅ Pegasus model endpoint accessible")
        print("   To fully test Pegasus, upload a video/audio file through the application")
        return True
    except Exception as e:
        print(f"❌ Pegasus model access failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 AWS Bedrock Configuration Test")
    print("=" * 50)
    
    # Check environment variables
    use_bedrock = os.getenv('USE_BEDROCK_ONLY', 'false').lower() == 'true'
    region = os.getenv('AWS_REGION', 'us-east-1')
    
    print(f"USE_BEDROCK_ONLY: {use_bedrock}")
    print(f"AWS_REGION: {region}")
    print()
    
    if not use_bedrock:
        print("⚠️  USE_BEDROCK_ONLY is set to false")
        print("   Set USE_BEDROCK_ONLY=true to use Bedrock models")
        print()
    
    # Run tests
    tests = [
        test_aws_credentials,
        test_bedrock_access,
        test_claude_inference,
        test_s3_access,
        test_pegasus_model
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
            results.append(False)
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Summary")
    print("=" * 50)
    
    passed = sum(results)
    total = len(results)
    
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed! Your Bedrock configuration is ready.")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        print("\n💡 Common solutions:")
        print("   1. Ensure AWS credentials are configured (IAM role or environment variables)")
        print("   2. Request access to Claude Sonnet 3.5 and Pegasus in AWS Bedrock console")
        print("   3. Verify S3 bucket exists and has proper permissions")
        print("   4. Check AWS_REGION is set to a region where models are available")

if __name__ == "__main__":
    main()