#!/usr/bin/env python3
"""
Check existing flows and create one if needed
"""
import requests
import json

def check_and_create_flows():
    """Check existing flows and create one if needed"""
    base_url = "http://localhost:8000"
    
    print("🔍 Checking Flows")
    print("=" * 30)
    
    try:
        # Check existing flows
        response = requests.get(f"{base_url}/flows")
        flows = response.json()
        
        print(f"✅ Flows endpoint accessible: {response.status_code}")
        
        if isinstance(flows, list):
            print(f"📊 Found {len(flows)} flows")
            
            if len(flows) == 0:
                print("⚠️  No flows found. You need to create a flow first.")
                print("\nTo create a flow:")
                print("1. Go to the frontend application")
                print("2. Click on the drawer/menu icon")
                print("3. Click 'NEW' to create a new flow")
                print("4. Then try uploading a PDF")
                return False
            else:
                for i, flow in enumerate(flows):
                    print(f"   Flow {i+1}:")
                    print(f"     ID: {flow.get('_id')}")
                    print(f"     Name: {flow.get('flow_name', 'Unknown')}")
                    print(f"     Type: {flow.get('flow_type', 'Unknown')}")
        else:
            print(f"📊 Single flow object: {flows}")
            
        return True
        
    except Exception as e:
        print(f"❌ Failed to check flows: {e}")
        return False

if __name__ == "__main__":
    check_and_create_flows()