#!/usr/bin/env python3
"""
Test PDF upload endpoint specifically
"""
import requests
import json
import os
from io import BytesIO

def create_test_pdf():
    """Create a simple test PDF content"""
    # This creates a minimal PDF-like content for testing
    # In a real scenario, you'd use a proper PDF library
    return b"%PDF-1.4\n1 0 obj\n<<\n/Type /Catalog\n/Pages 2 0 R\n>>\nendobj\n2 0 obj\n<<\n/Type /Pages\n/Kids [3 0 R]\n/Count 1\n>>\nendobj\n3 0 obj\n<<\n/Type /Page\n/Parent 2 0 R\n/MediaBox [0 0 612 792]\n>>\nendobj\nxref\n0 4\n0000000000 65535 f \n0000000009 00000 n \n0000000074 00000 n \n0000000120 00000 n \ntrailer\n<<\n/Size 4\n/Root 1 0 R\n>>\nstartxref\n179\n%%EOF"

def test_pdf_upload():
    """Test PDF upload endpoint"""
    base_url = "http://localhost:8000"
    
    print("🧪 Testing PDF Upload Endpoint")
    print("=" * 40)
    
    # Test 1: Check if backend is running
    try:
        response = requests.get(f"{base_url}/health")
        print(f"✅ Backend health check: {response.status_code}")
        health_data = response.json()
        print(f"   Bedrock enabled: {health_data.get('bedrock_enabled')}")
        print(f"   AWS region: {health_data.get('aws_region')}")
    except requests.exceptions.ConnectionError:
        print("❌ Backend is not running!")
        return False
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False
    
    # Test 2: Get flows to get a flow_id
    try:
        response = requests.get(f"{base_url}/flows")
        flows = response.json()
        
        if not flows or len(flows) == 0:
            print("⚠️  No flows found. Creating a test flow...")
            # You might need to create a flow first
            print("Please create a flow in the frontend first, then run this test.")
            return False
        
        flow_id = flows[0].get('_id') if isinstance(flows, list) else flows.get('_id')
        print(f"✅ Using flow ID: {flow_id}")
        
    except Exception as e:
        print(f"❌ Failed to get flows: {e}")
        return False
    
    # Test 3: Test PDF upload
    try:
        print("📄 Testing PDF upload...")
        
        # Create test PDF content
        pdf_content = create_test_pdf()
        
        # Prepare form data
        files = {
            'file': ('test.pdf', BytesIO(pdf_content), 'application/pdf')
        }
        data = {
            'flow_id': flow_id,
            'processing_type': 'gpt'
        }
        
        print(f"   Uploading to: {base_url}/component-create-pdf")
        print(f"   Flow ID: {flow_id}")
        print(f"   Processing type: gpt")
        
        response = requests.post(
            f"{base_url}/component-create-pdf",
            files=files,
            data=data,
            timeout=30  # 30 second timeout
        )
        
        print(f"✅ PDF upload response: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"   Component ID: {result.get('component_id')}")
            print(f"   Type: {result.get('type')}")
        else:
            print(f"❌ Upload failed: {response.text}")
            
    except requests.exceptions.Timeout:
        print("❌ Request timed out after 30 seconds")
        print("   This suggests the backend is hanging during processing")
    except Exception as e:
        print(f"❌ PDF upload failed: {e}")
        return False
    
    return True

if __name__ == "__main__":
    test_pdf_upload()