#!/bin/bash

# Fix for OpenCV and unstructured dependencies on EC2
echo "Installing system dependencies for OpenCV and unstructured..."

# Detect OS and use appropriate package manager
if command -v yum &> /dev/null; then
    echo "Detected Amazon Linux/RHEL/CentOS - using yum"
    
    # Update system packages
    sudo yum update -y
    
    # Install OpenGL and graphics libraries
    sudo yum install -y mesa-libGL mesa-libGL-devel
    sudo yum install -y libXext libSM libXrender
    sudo yum install -y mesa-libGLU mesa-libGLU-devel
    
    # Install additional dependencies for unstructured
    sudo yum install -y gcc gcc-c++ make
    sudo yum install -y python3-devel
    sudo yum install -y libffi-devel openssl-devel
    
    # Install poppler for PDF processing
    sudo yum install -y poppler-utils
    
    # Install tesseract for OCR
    sudo yum install -y tesseract tesseract-langpack-eng
    
elif command -v apt-get &> /dev/null; then
    echo "Detected Ubuntu/Debian - using apt-get"
    
    # Update system packages
    sudo apt-get update -y
    
    # Install OpenGL and graphics libraries
    sudo apt-get install -y libgl1-mesa-glx libgl1-mesa-dev
    sudo apt-get install -y libglib2.0-0 libsm6 libxext6 libxrender-dev
    sudo apt-get install -y libglu1-mesa libglu1-mesa-dev
    
    # Install additional dependencies for unstructured
    sudo apt-get install -y gcc g++ make
    sudo apt-get install -y python3-dev
    sudo apt-get install -y libffi-dev libssl-dev
    
    # Install poppler for PDF processing
    sudo apt-get install -y poppler-utils
    
    # Install tesseract for OCR
    sudo apt-get install -y tesseract-ocr tesseract-ocr-eng
    
else
    echo "Unsupported package manager. Please install dependencies manually."
    exit 1
fi

echo "System dependencies installed successfully!"
echo ""
echo "Next steps:"
echo "1. Restart your Python application: uvicorn app:app --reload"
echo "2. If you still get errors, try reinstalling opencv-python:"
echo "   pip uninstall opencv-python opencv-python-headless"
echo "   pip install opencv-python-headless"
echo ""
echo "3. For headless servers, you might need to set display:"
echo "   export DISPLAY=:0.0"