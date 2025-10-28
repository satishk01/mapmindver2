#!/usr/bin/env python3
"""
Test script to debug PDF processing issues
"""

import requests
import os
import time

def test_pdf_processing():
    """Test PDF processing with a simple PDF"""
    
    # Configuration
    base_url = "http://184.73.104.73:8000"
    
    print("🧪 PDF Processing Test")
    print("=" * 50)
    
    # First, create a test flow
    print("1️⃣ Creating test flow...")
    flow_data = {
        "flow_name": "Test PDF Flow",
        "summary": "Test flow for PDF processing",
        "flow_json": "",
        "flow_type": "manual"
    }
    
    try:
        response = requests.post(
            f"{base_url}/create-flow/",
            json=flow_data,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        if response.status_code == 200:
            flow_id = response.json()["flow_id"]
            print(f"✅ Flow created: {flow_id}")
        else:
            print(f"❌ Flow creation failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return
            
    except Exception as e:
        print(f"❌ Error creating flow: {e}")
        return
    
    # Test with a simple text file first (to verify the endpoint works)
    print("\n2️⃣ Testing with simple text content...")
    
    # Create a simple test file
    test_content = "This is a test document for PDF processing. It contains some sample text to verify that the processing pipeline is working correctly."
    
    # Save as a temporary file
    with open("test_document.txt", "w") as f:
        f.write(test_content)
    
    try:
        with open("test_document.txt", "rb") as f:
            files = {"file": ("test_document.txt", f, "text/plain")}
            data = {
                "flow_id": flow_id,
                "processing_type": "gpt"  # This should use Claude since USE_BEDROCK_ONLY=true
            }
            
            print(f"📡 Uploading test file...")
            print(f"   URL: {base_url}/component-create-pdf")
            print(f"   Flow ID: {flow_id}")
            print(f"   Processing type: gpt (will use Claude)")
            
            start_time = time.time()
            
            response = requests.post(
                f"{base_url}/component-create-pdf",
                files=files,
                data=data,
                timeout=120  # 2 minute timeout
            )
            
            end_time = time.time()
            processing_time = end_time - start_time
            
            print(f"⏱️  Processing time: {processing_time:.2f} seconds")
            
            if response.status_code == 200:
                print(f"✅ File processing successful!")
                print(f"   Response: {response.json()}")
            else:
                print(f"❌ File processing failed: {response.status_code}")
                print(f"   Response: {response.text}")
                
    except requests.exceptions.Timeout:
        print(f"⏰ Request timed out after 2 minutes")
    except Exception as e:
        print(f"❌ Error processing file: {e}")
    finally:
        # Clean up
        if os.path.exists("test_document.txt"):
            os.remove("test_document.txt")
    
    print("\n" + "=" * 50)
    print("🏁 Test completed")

if __name__ == "__main__":
    test_pdf_processing()