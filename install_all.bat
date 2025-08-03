@echo off
REM iOS WiFi Security Demonstration Toolkit - Complete Installation Script
REM MBA AI Study Project - Educational Purpose Only

echo ==================================================================
echo iOS WiFi Security Demonstration Toolkit - Complete Installation
echo MBA AI Study Project - Educational Purpose Only
echo ==================================================================
echo.

REM Check if running as administrator
net session >nul 2>&1
if %errorLevel% == 0 (
    echo [INFO] Running as administrator - this is fine for installation
) else (
    echo [INFO] Running as regular user - some features may require admin rights
)

REM Step 1: Check Python installation
echo [HEADER] Step 1: Checking Python installation...

python --version >nul 2>&1
if %errorLevel% == 0 (
    for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
    echo [INFO] Python found: %PYTHON_VERSION%
) else (
    python3 --version >nul 2>&1
    if %errorLevel% == 0 (
        for /f "tokens=2" %%i in ('python3 --version 2^>^&1') do set PYTHON_VERSION=%%i
        echo [INFO] Python3 found: %PYTHON_VERSION%
    ) else (
        echo [ERROR] Python not found. Please install Python 3.8+ from https://python.org
        echo [INFO] After installing Python, run this script again.
        pause
        exit /b 1
    )
)

REM Step 2: Check pip installation
echo [HEADER] Step 2: Checking pip installation...

pip --version >nul 2>&1
if %errorLevel% == 0 (
    echo [INFO] pip found
) else (
    pip3 --version >nul 2>&1
    if %errorLevel% == 0 (
        echo [INFO] pip3 found
    ) else (
        echo [ERROR] pip not found. Please install pip or upgrade Python.
        pause
        exit /b 1
    )
)

REM Step 3: Create virtual environment
echo [HEADER] Step 3: Setting up virtual environment...

if not exist "wifi_demo_env" (
    echo [INFO] Creating virtual environment...
    python -m venv wifi_demo_env
    if %errorLevel% == 0 (
        echo [INFO] Virtual environment created: wifi_demo_env
    ) else (
        echo [WARNING] Could not create virtual environment. Continuing with system Python...
    )
) else (
    echo [INFO] Virtual environment already exists: wifi_demo_env
)

REM Step 4: Activate virtual environment
echo [HEADER] Step 4: Activating virtual environment...

if exist "wifi_demo_env\Scripts\activate.bat" (
    call wifi_demo_env\Scripts\activate.bat
    echo [INFO] Virtual environment activated
) else (
    echo [WARNING] Could not activate virtual environment. Continuing with system Python...
)

REM Step 5: Check for tkinter (GUI support)
echo [HEADER] Step 5: Checking GUI support...

python -c "import tkinter" >nul 2>&1
if %errorLevel% == 0 (
    echo [INFO] Tkinter is available - GUI will work
    set GUI_AVAILABLE=true
) else (
    echo [WARNING] Tkinter not available - GUI features will be limited
    echo [INFO] Tkinter is usually included with Python installation
    set GUI_AVAILABLE=false
)

REM Step 6: Test basic functionality
echo [HEADER] Step 6: Testing basic functionality...

echo [INFO] Testing basic demo...
python ios_wifi_demo.py --scan >nul 2>&1
if %errorLevel% == 0 (
    echo [INFO] Basic demo test: PASSED
) else (
    echo [ERROR] Basic demo test: FAILED
)

echo [INFO] Testing advanced demo...
python advanced_wifi_exploit_demo.py --recon >nul 2>&1
if %errorLevel% == 0 (
    echo [INFO] Advanced demo test: PASSED
) else (
    echo [ERROR] Advanced demo test: FAILED
)

echo [INFO] Testing ultimate demo...
python ios_advanced_exploit_demo.py --demo >nul 2>&1
if %errorLevel% == 0 (
    echo [INFO] Ultimate demo test: PASSED
) else (
    echo [ERROR] Ultimate demo test: FAILED
)

REM Step 7: Create quick start script
echo [HEADER] Step 7: Creating quick start script...

(
echo @echo off
echo REM Quick Start Script for iOS WiFi Security Demonstration
echo REM MBA AI Study Project
echo.
echo echo ==================================================================
echo echo iOS WiFi Security Demonstration Toolkit - Quick Start
echo echo ==================================================================
echo echo.
echo.
echo REM Activate virtual environment if it exists
echo if exist "wifi_demo_env\Scripts\activate.bat" ^(
echo     call wifi_demo_env\Scripts\activate.bat
echo     echo [INFO] Virtual environment activated
echo ^)
echo.
echo echo Available demonstrations:
echo echo 1. Basic Demo: python ios_wifi_demo.py --demo
echo echo 2. Advanced Demo: python advanced_wifi_exploit_demo.py --demo
echo echo 3. Ultimate Demo: python ios_advanced_exploit_demo.py --demo
echo echo 4. GUI Demo: python wifi_demo_gui.py ^(if tkinter available^)
echo echo.
echo.
echo set /p choice="Which demo would you like to run? ^(1-4^): "
echo.
echo if "%%choice%%"=="1" ^(
echo     echo Running Basic Demo...
echo     python ios_wifi_demo.py --demo
echo ^) else if "%%choice%%"=="2" ^(
echo     echo Running Advanced Demo...
echo     python advanced_wifi_exploit_demo.py --demo
echo ^) else if "%%choice%%"=="3" ^(
echo     echo Running Ultimate Demo...
echo     python ios_advanced_exploit_demo.py --demo
echo ^) else if "%%choice%%"=="4" ^(
echo     echo Running GUI Demo...
echo     python wifi_demo_gui.py
echo ^) else ^(
echo     echo Invalid choice. Running Ultimate Demo...
echo     python ios_advanced_exploit_demo.py --demo
echo ^)
echo.
echo pause
) > run_demo.bat

echo [INFO] Quick start script created: run_demo.bat

REM Step 8: Create desktop shortcut
echo [HEADER] Step 8: Creating desktop shortcut...

set DESKTOP=%USERPROFILE%\Desktop
if exist "%DESKTOP%" (
    (
    echo @echo off
    echo cd /d "%~dp0"
    echo call run_demo.bat
    ) > "%DESKTOP%\WiFi Demo.bat"
    echo [INFO] Desktop shortcut created: %DESKTOP%\WiFi Demo.bat
) else (
    echo [WARNING] Desktop folder not found. Skipping shortcut creation.
)

REM Step 9: Final setup and information
echo [HEADER] Step 9: Installation Complete!

echo.
echo ==================================================================
echo 🎉 INSTALLATION COMPLETE! 🎉
echo ==================================================================
echo.
echo Your iOS WiFi Security Demonstration Toolkit is ready!
echo.
echo 📁 Files installed:
echo   ✅ ios_wifi_demo.py - Basic demonstration
echo   ✅ advanced_wifi_exploit_demo.py - Advanced demonstration
echo   ✅ ios_advanced_exploit_demo.py - Ultimate demonstration
echo   ✅ wifi_demo_gui.py - GUI interface
echo   ✅ run_demo.bat - Quick start script
echo   ✅ All documentation and reports
echo.
echo 🚀 Quick Start:
echo   run_demo.bat
echo.
echo 📖 Manual Start:
echo   python ios_advanced_exploit_demo.py --demo
echo.
echo 📚 Documentation:
echo   README_DEMO.md - Complete instructions
echo   FINAL_DEMO_PACKAGE.md - Package overview
echo.
echo 🔒 Safety Reminder:
echo   This toolkit is for EDUCATIONAL PURPOSES ONLY
echo   All attacks are simulated - no real malicious activities
echo.
echo 🎯 Ready for your MBA AI presentation!
echo.
echo ==================================================================

REM Step 10: Optional: Show demo immediately
set /p run_demo="Would you like to run a quick demo now? (y/n): "

if /i "%run_demo%"=="y" (
    echo.
    echo [HEADER] Running quick demo...
    python ios_advanced_exploit_demo.py --demo
)

echo.
echo [INFO] Installation script completed successfully!
echo [INFO] You can now use run_demo.bat to start any demonstration.
echo.
pause