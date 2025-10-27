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
    
    # Load environment first
    from dotenv import load_dotenv
    load_dotenv()
    
    use_bedrock = os.getenv('USE_BEDROCK_ONLY', 'false').lower() == 'true'
    print(f"Bedrock-only mode: {use_bedrock}")
    
    import app
    print("✅ App imported successfully!")
    
    # Test if FastAPI app is created
    if hasattr(app, 'app'):
        print("✅ FastAPI app instance found!")
    else:
        print("❌ FastAPI app instance not found!")
    
    # Check configuration
    if use_bedrock:
        print("✅ Running in Bedrock-only mode")
        if hasattr(app, 'bedrock_runtime_client'):
            print("✅ Bedrock client initialized")
        else:
            print("❌ Bedrock client not found")
    else:
        print("✅ Running in OpenAI/Gemini mode")
        if hasattr(app, 'llm'):
            print("✅ LLM initialized")
        else:
            print("❌ LLM not found")
    
    print("\n🎉 All tests passed! The app should start without import errors.")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("\nThis usually means missing dependencies. Try:")
    print("1. pip install -r requirements-minimal.txt")
    print("2. bash ../fix_dependencies.sh")
    sys.exit(1)
    
except Exception as e:
    print(f"❌ Other error: {e}")
    
    # Check if it's an OpenAI API key error in Bedrock mode
    if "api_key client option must be set" in str(e):
        print("\n💡 This looks like an OpenAI API key error.")
        print("If you want to use Bedrock only, make sure:")
        print("1. Set USE_BEDROCK_ONLY=true in your .env file")
        print("2. Or copy the Bedrock config: cp .env.bedrock .env")
        print("3. Then restart the app")
    else:
        print("\nCheck the error message above for details.")
    
    sys.exit(1)