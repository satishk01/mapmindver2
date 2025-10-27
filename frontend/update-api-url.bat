@echo off
REM Script to update API URL in frontend environment files
REM Usage: update-api-url.bat YOUR_EC2_PUBLIC_IP

if "%1"=="" (
    echo Usage: %0 ^<EC2_PUBLIC_IP^>
    echo Example: %0 54.123.45.67
    exit /b 1
)

set EC2_IP=%1

echo Updating API URL to: http://%EC2_IP%:8000

REM Update .env file
powershell -Command "(Get-Content .env) -replace 'YOUR_EC2_PUBLIC_IP', '%EC2_IP%' | Set-Content .env"
echo Updated .env

REM Update .env.production file
powershell -Command "(Get-Content .env.production) -replace 'YOUR_EC2_PUBLIC_IP', '%EC2_IP%' | Set-Content .env.production"
echo Updated .env.production

echo ✅ API URL updated successfully!
echo Frontend will now use: http://%EC2_IP%:8000
echo.
echo Next steps:
echo 1. Restart your frontend development server if it's running
echo 2. Build and deploy your frontend for production