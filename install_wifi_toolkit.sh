#!/bin/bash

# WiFi Security Research Toolkit Installation Script
# For Linux systems (Ubuntu/Debian)

echo "=========================================="
echo "WiFi Security Research Toolkit Installer"
echo "=========================================="
echo ""

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   echo "This script should not be run as root"
   echo "Please run as a regular user"
   exit 1
fi

# Check Python version
python_version=$(python3 --version 2>&1 | grep -oP '\d+\.\d+')
if [[ $(echo "$python_version >= 3.8" | bc -l) -eq 0 ]]; then
    echo "Error: Python 3.8 or higher is required"
    echo "Current version: $python_version"
    exit 1
fi

echo "✓ Python version check passed ($python_version)"

# Update package list
echo "Updating package list..."
sudo apt-get update

# Install system dependencies
echo "Installing system dependencies..."
sudo apt-get install -y \
    python3-pip \
    python3-dev \
    libpcap-dev \
    libffi-dev \
    libssl-dev \
    build-essential \
    git

# Install Python dependencies
echo "Installing Python dependencies..."
pip3 install --user -r requirements.txt

# Install additional system packages for WiFi analysis
echo "Installing WiFi analysis tools..."
sudo apt-get install -y \
    aircrack-ng \
    wireshark \
    tcpdump \
    iwconfig

# Create necessary directories
echo "Creating directories..."
mkdir -p reports logs configs

# Set up permissions
echo "Setting up permissions..."
chmod +x wifi_security_toolkit.py

# Create a simple launcher script
cat > wifi_toolkit << 'EOF'
#!/bin/bash
python3 wifi_security_toolkit.py "$@"
EOF

chmod +x wifi_toolkit

echo ""
echo "=========================================="
echo "Installation Complete!"
echo "=========================================="
echo ""
echo "Usage:"
echo "  ./wifi_toolkit                    # Run the toolkit"
echo "  ./wifi_toolkit --scan             # Run network scan"
echo "  ./wifi_toolkit --analyze          # Run security analysis"
echo "  ./wifi_toolkit --report           # Generate reports"
echo ""
echo "For network scanning features, run with sudo:"
echo "  sudo ./wifi_toolkit"
echo ""
echo "Documentation:"
echo "  README_WIFI_TOOLKIT.md           # User guide"
echo "  RESEARCH_METHODOLOGY.md          # Research methodology"
echo ""
echo "⚠️  IMPORTANT: This tool is for educational and authorized research only!"
echo "   Always obtain proper authorization before testing networks."
echo ""