@echo off
REM WiFi Security Research Toolkit Installation Script
REM For Windows systems

echo ==========================================
echo WiFi Security Research Toolkit Installer
echo ==========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from https://python.org
    pause
    exit /b 1
)

echo ✓ Python found
python --version

REM Check Python version
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo ✓ Python version: %PYTHON_VERSION%

REM Install pip if not available
python -m pip --version >nul 2>&1
if errorlevel 1 (
    echo Installing pip...
    python -m ensurepip --upgrade
)

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install Python dependencies
echo Installing Python dependencies...
python -m pip install -r requirements.txt

REM Create necessary directories
echo Creating directories...
if not exist reports mkdir reports
if not exist logs mkdir logs
if not exist configs mkdir configs

REM Create a simple launcher script
echo Creating launcher...
echo @echo off > wifi_toolkit.bat
echo python wifi_security_toolkit.py %%* >> wifi_toolkit.bat

echo.
echo ==========================================
echo Installation Complete!
echo ==========================================
echo.
echo Usage:
echo   wifi_toolkit.bat                    # Run the toolkit
echo   wifi_toolkit.bat --scan             # Run network scan
echo   wifi_toolkit.bat --analyze          # Run security analysis
echo   wifi_toolkit.bat --report           # Generate reports
echo.
echo Documentation:
echo   README_WIFI_TOOLKIT.md             # User guide
echo   RESEARCH_METHODOLOGY.md            # Research methodology
echo.
echo ⚠️  IMPORTANT: This tool is for educational and authorized research only!
echo    Always obtain proper authorization before testing networks.
echo.
pause