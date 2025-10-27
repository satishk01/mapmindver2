# 🚀 Quick Start Guide - Fixed Version

## The Issue Was Fixed ✅

The indentation errors in `backend/app.py` have been resolved. The application should now start properly.

## Quick Start Steps

### 1. Test the Fix

```bash
cd backend
python test_import.py
```

If this passes, proceed to step 2. If not, see troubleshooting below.

### 2. Start the Application

**Option A: Use the smart startup script (recommended)**
```bash
cd backend
python start_app.py
```

**Option B: Start directly**
```bash
cd backend
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

### 3. Verify It's Working

Open your browser to: `http://your-server-ip:8000/docs`

You should see the FastAPI documentation interface.

## If You Still Get Errors

### OpenCV/Graphics Library Errors

If you see:
```
ImportError: libGL.so.1: cannot open shared object file: No such file or directory
```

**Solution 1: Install system dependencies**
```bash
bash fix_dependencies.sh
```

**Solution 2: Use minimal requirements (fastest)**
```bash
pip uninstall -r requirements.txt -y
pip install -r requirements-minimal.txt
```

### Missing Dependencies

If you see import errors for specific packages:

```bash
# For missing basic dependencies
pip install fastapi uvicorn pymongo boto3 python-dotenv

# For AI/ML dependencies
pip install openai google-generativeai langchain chromadb

# For AWS Bedrock (if using USE_BEDROCK_ONLY=true)
pip install boto3 botocore
```

### Environment Configuration

Make sure you have a `.env` file in the `backend/` directory:

```bash
cd backend
cp .env.example .env
# Edit .env with your actual values
```

Minimum required variables:
```env
mongo_db_url=mongodb://localhost:27017/
bucket_name=your-s3-bucket
USE_BEDROCK_ONLY=false
```

## Test Different Features

### 1. Basic Text Processing
- Create a flow
- Upload a simple .txt file
- Ask questions about it

### 2. AWS Bedrock (if configured)
```bash
# Switch to Bedrock models
python switch_models.py bedrock

# Test Bedrock configuration
python test_bedrock.py
```

### 3. PDF Processing
- Upload a PDF file
- Choose processing type:
  - `aws`: Uses AWS Textract (most reliable)
  - `gpt`: Uses OpenAI (requires API key)
  - `custom`: Uses unstructured + camelot (requires system dependencies)

## Architecture Overview

The application now has:

- **Graceful dependency handling**: Missing optional packages won't crash the app
- **Multiple AI model support**: OpenAI/Gemini OR AWS Bedrock
- **Flexible PDF processing**: Multiple processing backends
- **Better error messages**: Clear guidance when things go wrong

## Need Help?

1. **Check logs**: Look at the console output for specific error messages
2. **Run diagnostics**: `python test_import.py` and `python test_bedrock.py`
3. **Check guides**: 
   - `QUICK_FIX.md` for immediate solutions
   - `AWS_EC2_DEPLOYMENT.md` for full deployment
   - `backend/BEDROCK_MIGRATION.md` for Bedrock setup

## Success Indicators

✅ **App starts without errors**
✅ **FastAPI docs accessible at /docs**
✅ **Can create flows and upload files**
✅ **AI processing works (OpenAI/Gemini or Bedrock)**

The application is now much more robust and should handle various deployment scenarios gracefully!