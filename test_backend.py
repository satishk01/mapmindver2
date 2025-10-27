#!/usr/bin/env python3
"""
Test script to check backend functionality
"""
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

def test_backend():
    """Test if backend is running and responding"""
    base_url = "http://localhost:8000"
    
    print("🧪 Testing Backend Connection")
    print("=" * 40)
    
    # Test 1: Health check
    try:
        response = requests.get(f"{base_url}/")
        print(f"✅ Backend is running: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ Backend is not running!")
        print("Please start the backend first:")
        print("cd backend && python start_app.py")
        return False
    except Exception as e:
        print(f"❌ Error connecting to backend: {e}")
        return False
    
    # Test 2: Check environment
    use_bedrock = os.getenv('USE_BEDROCK_ONLY', 'false').lower() == 'true'
    aws_region = os.getenv('AWS_REGION', 'us-east-1')
    
    print(f"🔧 Configuration:")
    print(f"   USE_BEDROCK_ONLY: {use_bedrock}")
    print(f"   AWS_REGION: {aws_region}")
    
    # Test 3: Try to get flows (this will test MongoDB connection)
    try:
        response = requests.get(f"{base_url}/flows")
        print(f"✅ Database connection: {response.status_code}")
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
    
    return True

if __name__ == "__main__":
    test_backend()