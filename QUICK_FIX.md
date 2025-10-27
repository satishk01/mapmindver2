# Quick Fix for OpenCV/Graphics Library Error

## The Problem
You're getting this error when starting the application:
```
ImportError: libGL.so.1: cannot open shared object file: No such file or directory
```

This happens because the `unstructured` package requires OpenCV, which needs system graphics libraries.

## Quick Solutions

### Option 1: Install System Dependencies (Recommended)

**For Amazon Linux/RHEL/CentOS:**
```bash
sudo yum install -y mesa-libGL mesa-libGL-devel libXext libSM libXrender
sudo yum install -y gcc gcc-c++ make python3-devel
```

**For Ubuntu/Debian:**
```bash
sudo apt-get install -y libgl1-mesa-glx libglib2.0-0 libsm6 libxext6 libxrender-dev
sudo apt-get install -y gcc g++ make python3-dev
```

**Or use the provided script:**
```bash
bash fix_dependencies.sh
```

### Option 2: Use Minimal Requirements (Fastest)

If you want to get the app running quickly without heavy dependencies:

```bash
cd backend
pip uninstall -r requirements.txt -y
pip install -r requirements-minimal.txt
```

This will disable some advanced PDF processing features but keep the core functionality working.

### Option 3: Use Headless OpenCV

```bash
pip uninstall opencv-python opencv-python-headless -y
pip install opencv-python-headless
export DISPLAY=:0.0
```

## Start the Application

After applying any of the above fixes:

```bash
cd backend
source venv/bin/activate

# Option A: Use the smart startup script
python start_app.py

# Option B: Start directly
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

## Verify It's Working

1. Open your browser to `http://your-server-ip:8000/docs`
2. You should see the FastAPI documentation
3. Try creating a flow and uploading a simple text file first
4. If that works, try other file types

## What Features Are Affected?

- **With minimal requirements**: Advanced PDF table extraction is disabled, but basic PDF processing still works via AWS Textract
- **With full requirements**: All features work including advanced PDF processing with unstructured and camelot

## Need Help?

If you're still having issues:

1. Check the full error message
2. Run the diagnostic script: `python test_bedrock.py`
3. Check the troubleshooting section in `AWS_EC2_DEPLOYMENT.md`

The application is designed to work gracefully even with missing optional dependencies!