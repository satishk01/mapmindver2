#!/usr/bin/env python3
"""
Model switching utility for GenAI Mind Map Flow Builder
This script helps you switch between OpenAI/Gemini and AWS Bedrock models.
"""

import os
import sys
from pathlib import Path

def update_env_file(use_bedrock: bool):
    """Update the .env file with the appropriate configuration"""
    env_path = Path(".env")
    
    if not env_path.exists():
        print("❌ .env file not found. Please create one based on .env.example")
        return False
    
    # Read current .env file
    with open(env_path, 'r') as f:
        lines = f.readlines()
    
    # Update or add USE_BEDROCK_ONLY setting
    updated_lines = []
    bedrock_setting_found = False
    
    for line in lines:
        if line.startswith('USE_BEDROCK_ONLY='):
            updated_lines.append(f'USE_BEDROCK_ONLY={str(use_bedrock).lower()}\n')
            bedrock_setting_found = True
        else:
            updated_lines.append(line)
    
    # Add setting if not found
    if not bedrock_setting_found:
        updated_lines.append(f'\n# Bedrock Configuration\nUSE_BEDROCK_ONLY={str(use_bedrock).lower()}\n')
    
    # Write updated .env file
    with open(env_path, 'w') as f:
        f.writelines(updated_lines)
    
    return True

def check_requirements(use_bedrock: bool):
    """Check if required environment variables are set"""
    required_vars = ['mongo_db_url', 'bucket_name']
    
    if use_bedrock:
        required_vars.extend(['AWS_REGION'])
        optional_vars = ['openai_api_key', 'gemini_api_key']
        print("🔍 Checking AWS Bedrock requirements...")
    else:
        required_vars.extend(['openai_api_key', 'gemini_api_key'])
        optional_vars = ['AWS_REGION']
        print("🔍 Checking OpenAI/Gemini requirements...")
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Missing required environment variables: {', '.join(missing_vars)}")
        return False
    
    print("✅ All required environment variables are set")
    
    # Check optional variables
    missing_optional = []
    for var in optional_vars:
        if not os.getenv(var):
            missing_optional.append(var)
    
    if missing_optional:
        print(f"⚠️  Optional variables not set: {', '.join(missing_optional)}")
    
    return True

def display_model_info(use_bedrock: bool):
    """Display information about the selected models"""
    if use_bedrock:
        print("\n🤖 AWS Bedrock Models Configuration")
        print("=" * 40)
        print("Text Processing: Claude Sonnet 3.5")
        print("Image Analysis: Claude Sonnet 3.5 (with vision)")
        print("Video/Audio: Pegasus")
        print("YouTube: Pegasus")
        print("\n📋 Requirements:")
        print("- AWS credentials (IAM role or environment variables)")
        print("- Access to Claude Sonnet 3.5 and Pegasus models in Bedrock")
        print("- S3 bucket for media file storage")
        print("- AWS_REGION environment variable")
    else:
        print("\n🤖 OpenAI/Gemini Models Configuration")
        print("=" * 40)
        print("Text Processing: OpenAI GPT-4o")
        print("Image Analysis: Google Gemini 2.0 Flash")
        print("Video/Audio: Google Gemini 2.0 Flash")
        print("YouTube: Google Vertex AI Gemini 2.0 Flash")
        print("\n📋 Requirements:")
        print("- OpenAI API key")
        print("- Google Gemini API key")
        print("- Google Cloud Project ID")
        print("- Google Cloud service account JSON file")

def main():
    """Main function"""
    print("🔄 GenAI Mind Map Flow Builder - Model Switcher")
    print("=" * 60)
    
    if len(sys.argv) != 2 or sys.argv[1] not in ['bedrock', 'openai']:
        print("Usage: python switch_models.py [bedrock|openai]")
        print("\nExamples:")
        print("  python switch_models.py bedrock   # Switch to AWS Bedrock models")
        print("  python switch_models.py openai    # Switch to OpenAI/Gemini models")
        sys.exit(1)
    
    use_bedrock = sys.argv[1] == 'bedrock'
    
    # Display model information
    display_model_info(use_bedrock)
    
    # Confirm with user
    model_type = "AWS Bedrock" if use_bedrock else "OpenAI/Gemini"
    confirm = input(f"\n❓ Switch to {model_type} models? (y/N): ").lower().strip()
    
    if confirm != 'y':
        print("❌ Operation cancelled")
        sys.exit(0)
    
    # Update .env file
    print(f"\n🔧 Updating configuration to use {model_type} models...")
    
    if not update_env_file(use_bedrock):
        sys.exit(1)
    
    print("✅ Configuration updated successfully")
    
    # Load updated environment
    from dotenv import load_dotenv
    load_dotenv(override=True)
    
    # Check requirements
    if not check_requirements(use_bedrock):
        print("\n⚠️  Configuration updated but some requirements are missing.")
        print("Please update your .env file with the missing variables.")
        sys.exit(1)
    
    print(f"\n🎉 Successfully switched to {model_type} models!")
    
    # Provide next steps
    if use_bedrock:
        print("\n📝 Next steps:")
        print("1. Ensure AWS credentials are configured")
        print("2. Request access to models in AWS Bedrock console")
        print("3. Test configuration: python test_bedrock.py")
        print("4. Restart your application")
    else:
        print("\n📝 Next steps:")
        print("1. Ensure OpenAI API key is valid")
        print("2. Ensure Google Cloud credentials are configured")
        print("3. Restart your application")
    
    print(f"\n💡 Current configuration: USE_BEDROCK_ONLY={str(use_bedrock).lower()}")

if __name__ == "__main__":
    main()