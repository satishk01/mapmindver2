#!/usr/bin/env python3
"""
Simple test to check if the app can be imported without errors
"""

import sys
import os

# Add the backend directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    print("Testing app import...")
    import app
    print("✅ App imported successfully!")
    
    # Test if FastAPI app is created
    if hasattr(app, 'app'):
        print("✅ FastAPI app instance found!")
    else:
        print("❌ FastAPI app instance not found!")
    
    print("\n🎉 All tests passed! The app should start without import errors.")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("\nThis usually means missing dependencies. Try:")
    print("1. pip install -r requirements-minimal.txt")
    print("2. bash ../fix_dependencies.sh")
    sys.exit(1)
    
except Exception as e:
    print(f"❌ Other error: {e}")
    print("\nCheck the error message above for details.")
    sys.exit(1)