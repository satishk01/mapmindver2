#!/usr/bin/env python3
"""
Test flow creation endpoint
"""
import requests
import json

def test_flow_creation():
    """Test creating a new flow"""
    base_url = "http://localhost:8000"
    
    print("🧪 Testing Flow Creation")
    print("=" * 30)
    
    # Test creating a manual flow
    try:
        data = {
            "flow_name": "Test Manual Flow",
            "flow_type": "manual"
        }
        
        response = requests.post(
            f"{base_url}/create-flow/",
            json=data,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"✅ Manual flow creation: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"   Flow ID: {result.get('flow_id')}")
            print(f"   Flow Type: {result.get('flow_type')}")
            return result.get('flow_id')
        else:
            print(f"❌ Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Flow creation failed: {e}")
        return None

if __name__ == "__main__":
    flow_id = test_flow_creation()
    if flow_id:
        print(f"\n✅ Flow created successfully! ID: {flow_id}")
        print("You can now upload PDFs to this flow.")
    else:
        print("\n❌ Flow creation failed.")