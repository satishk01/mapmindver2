#!/usr/bin/env python3
"""
Startup script for the GenAI Mind Map Flow Builder
This script handles dependency issues gracefully and provides helpful error messages.
"""

import sys
import os
import subprocess

def check_dependencies():
    """Check if critical dependencies are available"""
    missing_deps = []
    warnings = []
    
    # Check critical dependencies
    try:
        import fastapi
        import uvicorn
        import pymongo
        import boto3
    except ImportError as e:
        missing_deps.append(f"Critical dependency missing: {e}")
    
    # Check optional dependencies
    try:
        import cv2
    except ImportError:
        warnings.append("OpenCV not available - some PDF processing features may be limited")
    
    try:
        from unstructured.partition.pdf import partition_pdf
    except ImportError:
        warnings.append("Unstructured not available - advanced PDF processing disabled")
    
    try:
        import camelot
    except ImportError:
        warnings.append("Camelot not available - PDF table extraction disabled")
    
    try:
        import openai
    except ImportError:
        warnings.append("OpenAI not available - set USE_BEDROCK_ONLY=true to use only Bedrock")
    
    try:
        import google.generativeai
    except ImportError:
        warnings.append("Google Gemini not available - set USE_BEDROCK_ONLY=true to use only Bedrock")
    
    return missing_deps, warnings

def install_system_dependencies():
    """Suggest system dependency installation"""
    print("\n🔧 System Dependencies Required")
    print("=" * 50)
    print("It looks like you're missing system dependencies for OpenCV.")
    print("Please run the following commands to install them:")
    print()
    
    # Check OS and provide appropriate commands
    if os.path.exists('/etc/amazon-linux-release') or os.path.exists('/etc/redhat-release'):
        print("For Amazon Linux/RHEL/CentOS:")
        print("sudo yum install -y mesa-libGL mesa-libGL-devel libXext libSM libXrender")
        print("sudo yum install -y gcc gcc-c++ make python3-devel")
    elif os.path.exists('/etc/debian_version'):
        print("For Ubuntu/Debian:")
        print("sudo apt-get install -y libgl1-mesa-glx libglib2.0-0 libsm6 libxext6 libxrender-dev")
        print("sudo apt-get install -y gcc g++ make python3-dev")
    else:
        print("Please install OpenGL and development libraries for your system.")
    
    print()
    print("Or run the provided script:")
    print("bash fix_dependencies.sh")
    print()
    print("Alternatively, you can use the minimal requirements:")
    print("pip install -r requirements-minimal.txt")

def main():
    """Main startup function"""
    print("🚀 Starting GenAI Mind Map Flow Builder")
    print("=" * 50)
    
    # Check dependencies
    missing_deps, warnings = check_dependencies()
    
    if missing_deps:
        print("❌ Critical dependencies missing:")
        for dep in missing_deps:
            print(f"   {dep}")
        print("\nPlease install missing dependencies:")
        print("pip install -r requirements.txt")
        sys.exit(1)
    
    if warnings:
        print("⚠️  Optional dependencies missing:")
        for warning in warnings:
            print(f"   {warning}")
        print()
    
    # Check environment configuration
    from dotenv import load_dotenv
    load_dotenv()
    
    use_bedrock = os.getenv('USE_BEDROCK_ONLY', 'false').lower() == 'true'
    
    if use_bedrock:
        print("🤖 Using AWS Bedrock models")
        # Check AWS configuration
        if not os.getenv('AWS_REGION'):
            print("⚠️  AWS_REGION not set, using default: us-east-1")
    else:
        print("🤖 Using OpenAI/Gemini models")
        # Check API keys
        if not os.getenv('openai_api_key'):
            print("⚠️  OpenAI API key not set")
        if not os.getenv('gemini_api_key'):
            print("⚠️  Gemini API key not set")
    
    print()
    print("✅ Starting application...")
    
    # Start the application
    try:
        import uvicorn
        uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
    except ImportError as e:
        print(f"❌ Failed to start application: {e}")
        install_system_dependencies()
        sys.exit(1)
    except Exception as e:
        print(f"❌ Application error: {e}")
        print("\nIf you're getting OpenCV/graphics errors, try:")
        print("1. Install system dependencies: bash fix_dependencies.sh")
        print("2. Use minimal requirements: pip install -r requirements-minimal.txt")
        print("3. Set environment variable: export DISPLAY=:0.0")
        sys.exit(1)

if __name__ == "__main__":
    main()