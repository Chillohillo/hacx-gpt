#!/bin/bash

# iOS WiFi Exploit Demo Suite - Installation Script
# Educational Tool for MBA AI Studies

echo "🎓 Installing iOS WiFi Exploit Demo Suite..."
echo "⚠️  EDUCATIONAL PURPOSE ONLY ⚠️"

# Check if running as root
if [ "$EUID" -eq 0 ]; then
    echo "Running as root - good for network operations"
else
    echo "Warning: Some features may require root privileges"
    echo "Run with 'sudo ./install_demo.sh' for full functionality"
fi

# Install system dependencies
echo "📦 Installing system dependencies..."
sudo apt update
sudo apt install -y python3 python3-pip gcc libgl1-mesa-glx libglib2.0-0 libssl-dev

# Install Python dependencies
echo "🐍 Installing Python dependencies..."
pip3 install -r requirements.txt

# Run the setup script
echo "🔧 Setting up demo environment..."
python3 enhanced_grok4_exploit_suite.py

echo "✅ Installation complete!"
echo "🎯 Next steps:"
echo "1. Run: python3 ios_wifi_exploit_demo.py"
echo "2. Follow: LIVE_DEMO_GUIDE.md"
echo "3. Remember: FOR EDUCATIONAL PURPOSES ONLY"