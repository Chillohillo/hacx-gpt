#!/bin/bash

# iOS WiFi Security Demonstration Toolkit - Complete Installation Script
# MBA AI Study Project - Educational Purpose Only

echo "=================================================================="
echo "iOS WiFi Security Demonstration Toolkit - Complete Installation"
echo "MBA AI Study Project - Educational Purpose Only"
echo "=================================================================="
echo

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "${BLUE}[HEADER]${NC} $1"
}

# Check if running as root (optional, but recommended for some features)
if [[ $EUID -eq 0 ]]; then
    print_warning "Running as root - this is fine for installation"
else
    print_status "Running as regular user - some features may require sudo"
fi

# Step 1: Check and install Python
print_header "Step 1: Checking Python installation..."

if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2)
    print_status "Python3 found: $PYTHON_VERSION"
else
    print_error "Python3 not found. Installing..."
    
    # Detect OS and install Python
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        if command -v apt-get &> /dev/null; then
            sudo apt-get update
            sudo apt-get install -y python3 python3-pip python3-venv
        elif command -v yum &> /dev/null; then
            sudo yum install -y python3 python3-pip
        elif command -v dnf &> /dev/null; then
            sudo dnf install -y python3 python3-pip
        else
            print_error "Unsupported Linux distribution. Please install Python3 manually."
            exit 1
        fi
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        if command -v brew &> /dev/null; then
            brew install python3
        else
            print_error "Homebrew not found. Please install Python3 manually or install Homebrew first."
            exit 1
        fi
    else
        print_error "Unsupported operating system. Please install Python3 manually."
        exit 1
    fi
fi

# Step 2: Check Python version
PYTHON_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

if [[ $PYTHON_MAJOR -lt 3 ]] || [[ $PYTHON_MINOR -lt 8 ]]; then
    print_error "Python 3.8+ required. Current version: $PYTHON_VERSION"
    exit 1
fi

print_status "Python version check passed: $PYTHON_VERSION"

# Step 3: Create virtual environment (optional but recommended)
print_header "Step 2: Setting up virtual environment..."

if [[ ! -d "wifi_demo_env" ]]; then
    print_status "Creating virtual environment..."
    python3 -m venv wifi_demo_env
    print_status "Virtual environment created: wifi_demo_env"
else
    print_status "Virtual environment already exists: wifi_demo_env"
fi

# Step 4: Activate virtual environment
print_header "Step 3: Activating virtual environment..."

if [[ -f "wifi_demo_env/bin/activate" ]]; then
    source wifi_demo_env/bin/activate
    print_status "Virtual environment activated"
else
    print_warning "Could not activate virtual environment. Continuing with system Python..."
fi

# Step 5: Install required packages
print_header "Step 4: Installing required packages..."

# Check if pip is available
if ! command -v pip3 &> /dev/null; then
    print_error "pip3 not found. Installing..."
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        sudo apt-get install -y python3-pip
    fi
fi

# Install basic packages (most are included with Python)
print_status "Installing basic packages..."

# Try to install optional packages (these might not be available on all systems)
print_status "Checking for optional packages..."

# Check for tkinter (GUI support)
python3 -c "import tkinter" 2>/dev/null
if [[ $? -eq 0 ]]; then
    print_status "Tkinter is available - GUI will work"
    GUI_AVAILABLE=true
else
    print_warning "Tkinter not available - GUI features will be limited"
    print_status "To install tkinter:"
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo "  sudo apt-get install python3-tk"
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        echo "  brew install python-tk"
    fi
    GUI_AVAILABLE=false
fi

# Step 6: Make scripts executable
print_header "Step 5: Making scripts executable..."

chmod +x ios_wifi_demo.py
chmod +x advanced_wifi_exploit_demo.py
chmod +x ios_advanced_exploit_demo.py
chmod +x wifi_demo_gui.py

print_status "All scripts made executable"

# Step 7: Test basic functionality
print_header "Step 6: Testing basic functionality..."

print_status "Testing basic demo..."
python3 ios_wifi_demo.py --scan > /dev/null 2>&1
if [[ $? -eq 0 ]]; then
    print_status "Basic demo test: PASSED"
else
    print_error "Basic demo test: FAILED"
fi

print_status "Testing advanced demo..."
python3 advanced_wifi_exploit_demo.py --recon > /dev/null 2>&1
if [[ $? -eq 0 ]]; then
    print_status "Advanced demo test: PASSED"
else
    print_error "Advanced demo test: FAILED"
fi

print_status "Testing ultimate demo..."
python3 ios_advanced_exploit_demo.py --demo > /dev/null 2>&1
if [[ $? -eq 0 ]]; then
    print_status "Ultimate demo test: PASSED"
else
    print_error "Ultimate demo test: FAILED"
fi

# Step 8: Create quick start script
print_header "Step 7: Creating quick start script..."

cat > run_demo.sh << 'EOF'
#!/bin/bash

# Quick Start Script for iOS WiFi Security Demonstration
# MBA AI Study Project

echo "=================================================================="
echo "iOS WiFi Security Demonstration Toolkit - Quick Start"
echo "=================================================================="
echo

# Activate virtual environment if it exists
if [[ -f "wifi_demo_env/bin/activate" ]]; then
    source wifi_demo_env/bin/activate
    echo "[INFO] Virtual environment activated"
fi

echo "Available demonstrations:"
echo "1. Basic Demo: python3 ios_wifi_demo.py --demo"
echo "2. Advanced Demo: python3 advanced_wifi_exploit_demo.py --demo"
echo "3. Ultimate Demo: python3 ios_advanced_exploit_demo.py --demo"
echo "4. GUI Demo: python3 wifi_demo_gui.py (if tkinter available)"
echo

read -p "Which demo would you like to run? (1-4): " choice

case $choice in
    1)
        echo "Running Basic Demo..."
        python3 ios_wifi_demo.py --demo
        ;;
    2)
        echo "Running Advanced Demo..."
        python3 advanced_wifi_exploit_demo.py --demo
        ;;
    3)
        echo "Running Ultimate Demo..."
        python3 ios_advanced_exploit_demo.py --demo
        ;;
    4)
        echo "Running GUI Demo..."
        python3 wifi_demo_gui.py
        ;;
    *)
        echo "Invalid choice. Running Ultimate Demo..."
        python3 ios_advanced_exploit_demo.py --demo
        ;;
esac
EOF

chmod +x run_demo.sh
print_status "Quick start script created: run_demo.sh"

# Step 9: Create system-wide shortcut (optional)
print_header "Step 8: Creating system shortcuts..."

# Create desktop shortcut if on Linux with GUI
if [[ "$OSTYPE" == "linux-gnu"* ]] && [[ -n "$DISPLAY" ]]; then
    if [[ -d "$HOME/Desktop" ]]; then
        cat > "$HOME/Desktop/WiFi Demo.desktop" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=WiFi Security Demo
Comment=iOS WiFi Security Demonstration Toolkit
Exec=$PWD/run_demo.sh
Icon=network-wireless
Terminal=true
Categories=Network;Security;
EOF
        chmod +x "$HOME/Desktop/WiFi Demo.desktop"
        print_status "Desktop shortcut created"
    fi
fi

# Step 10: Final setup and information
print_header "Step 9: Installation Complete!"

echo
echo "=================================================================="
echo "🎉 INSTALLATION COMPLETE! 🎉"
echo "=================================================================="
echo
echo "Your iOS WiFi Security Demonstration Toolkit is ready!"
echo
echo "📁 Files installed:"
echo "  ✅ ios_wifi_demo.py - Basic demonstration"
echo "  ✅ advanced_wifi_exploit_demo.py - Advanced demonstration"
echo "  ✅ ios_advanced_exploit_demo.py - Ultimate demonstration"
echo "  ✅ wifi_demo_gui.py - GUI interface"
echo "  ✅ run_demo.sh - Quick start script"
echo "  ✅ All documentation and reports"
echo
echo "🚀 Quick Start:"
echo "  ./run_demo.sh"
echo
echo "📖 Manual Start:"
echo "  python3 ios_advanced_exploit_demo.py --demo"
echo
echo "📚 Documentation:"
echo "  README_DEMO.md - Complete instructions"
echo "  FINAL_DEMO_PACKAGE.md - Package overview"
echo
echo "🔒 Safety Reminder:"
echo "  This toolkit is for EDUCATIONAL PURPOSES ONLY"
echo "  All attacks are simulated - no real malicious activities"
echo
echo "🎯 Ready for your MBA AI presentation!"
echo
echo "=================================================================="

# Step 11: Optional: Show demo immediately
read -p "Would you like to run a quick demo now? (y/n): " run_demo

if [[ $run_demo == "y" || $run_demo == "Y" ]]; then
    echo
    print_header "Running quick demo..."
    python3 ios_advanced_exploit_demo.py --demo
fi

echo
print_status "Installation script completed successfully!"
print_status "You can now use ./run_demo.sh to start any demonstration."