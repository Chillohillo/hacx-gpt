# WiFi Security Research Toolkit

## Overview

The WiFi Security Research Toolkit is a comprehensive Python-based tool designed for educational and research purposes in the field of network security. This toolkit enables security researchers to analyze WiFi networks, identify vulnerabilities, and understand various attack vectors in controlled test environments.

## ⚠️ IMPORTANT DISCLAIMER

**This tool is strictly for educational and authorized security research purposes only.**

- Use only on networks you own or have explicit permission to test
- All attack simulations are educational demonstrations
- This tool is designed for defensive security research
- Users are responsible for compliance with local laws and regulations

## Features

### 🔍 Network Discovery
- Automated device enumeration on local networks
- OS fingerprinting and device identification
- Port scanning and service detection
- MAC address resolution and vendor identification

### 🛡️ Security Analysis
- Vulnerability assessment of network devices
- WiFi encryption strength analysis
- Default credential detection
- Firmware version checking
- Security scoring system (0-100)

### 🎯 Attack Simulations (Educational Only)
- **Deauthentication Attack Simulation**: Demonstrates how devices can be disconnected from networks
- **Evil Twin Attack Simulation**: Shows how fake access points can be created
- **KARMA Attack Simulation**: Illustrates probe request exploitation

### 📊 Reporting & Documentation
- JSON report generation for automated processing
- PDF reports for research presentations
- Detailed vulnerability documentation
- Security recommendations and mitigation strategies

### 🖥️ User Interface
- **CLI Mode**: Command-line interface for automation
- **Interactive Mode**: Real-time analysis and testing
- **GUI Mode**: Graphical interface (optional tkinter-based)

## Installation

### Prerequisites
- Python 3.8 or higher
- Root/Administrator privileges (for network scanning)
- Linux/macOS/Windows support

### Quick Installation

```bash
# Clone the repository
git clone <repository-url>
cd wifi-security-toolkit

# Install dependencies
pip install -r requirements.txt

# For Linux users, install additional system dependencies
sudo apt-get install python3-scapy libpcap-dev
```

### Manual Installation

```bash
# Core dependencies
pip install scapy rich matplotlib reportlab

# Optional: GUI support
pip install tkinter

# Optional: Advanced WiFi analysis
pip install pywifi
```

## Usage

### Basic Usage

```bash
# Run the toolkit
python wifi_security_toolkit.py

# Run specific functions
python wifi_security_toolkit.py --scan
python wifi_security_toolkit.py --analyze
python wifi_security_toolkit.py --report
```

### Interactive Mode

```bash
# Start interactive session
python wifi_security_toolkit.py --cli

# Available commands:
# scan     - Discover devices on network
# analyze  - Perform security analysis
# report   - Generate security reports
# help     - Show help
# exit     - Exit interactive mode
```

### Command Line Options

```bash
python wifi_security_toolkit.py [OPTIONS]

Options:
  --cli      Run in CLI mode
  --gui      Run in GUI mode
  --scan     Run network scan
  --analyze  Run security analysis
  --report   Generate reports
  --help     Show help message
```

## Core Components

### 1. NetworkScanner
Handles network discovery and device enumeration:
- ARP-based device discovery
- Ping-based fallback scanning
- OS detection and fingerprinting
- Port scanning capabilities

### 2. SecurityAnalyzer
Performs comprehensive security analysis:
- Vulnerability database integration
- Security scoring algorithms
- Risk assessment and categorization
- Mitigation recommendation generation

### 3. AttackSimulator
Educational attack demonstrations:
- Controlled environment validation
- Simulated attack progress tracking
- Educational output and explanations
- Safety checks and warnings

### 4. ReportGenerator
Creates detailed security reports:
- JSON format for automation
- PDF format for presentations
- Executive summaries
- Technical details and recommendations

## Security Features

### Test Environment Validation
The toolkit includes built-in safety mechanisms:
- Automatic detection of test networks
- Prevention of attacks on production networks
- Clear warnings and disclaimers
- Educational context for all simulations

### Vulnerability Database
Comprehensive vulnerability tracking:
- Weak encryption detection
- Default credential identification
- Open port analysis
- Firmware version checking
- Security configuration assessment

## Output Formats

### Console Output
- Rich formatted tables
- Color-coded security scores
- Real-time progress indicators
- Detailed logging and status updates

### JSON Reports
```json
{
  "scan_timestamp": "2024-01-15T10:30:00",
  "devices": {
    "192.168.1.100": {
      "ip": "192.168.1.100",
      "mac": "00:11:22:33:44:55",
      "os": "Linux",
      "security_score": 75,
      "vulnerabilities": [...]
    }
  },
  "summary": {
    "total_devices": 5,
    "high_risk_devices": 1
  }
}
```

### PDF Reports
- Professional formatting
- Executive summaries
- Technical details
- Security recommendations
- Visual charts and tables

## Research Methodology

This toolkit implements several academic research methodologies:

### 1. Network Analysis
- Systematic network enumeration
- Device classification and categorization
- Service identification and mapping
- Topology analysis and visualization

### 2. Security Assessment
- Vulnerability correlation analysis
- Risk scoring and prioritization
- Threat modeling and analysis
- Security posture evaluation

### 3. Attack Simulation
- Controlled environment testing
- Educational demonstration
- Defensive strategy development
- Security awareness training

## Configuration

### Test Network Configuration
The toolkit automatically detects test networks:
```python
TEST_NETWORK_PREFIXES = [
    "192.168.1.", "192.168.0.", "10.0.0.", "172.16.0.",
    "192.168.100.", "192.168.50.", "10.0.1.", "172.20.0."
]
```

### Custom Configuration
Create a configuration file for custom settings:
```python
# config.py
SCAN_TIMEOUT = 10
MAX_RETRIES = 5
PACKET_COUNT = 200
```

## Troubleshooting

### Common Issues

1. **Permission Denied**
   ```bash
   # Run with sudo for network scanning
   sudo python wifi_security_toolkit.py
   ```

2. **Scapy Import Error**
   ```bash
   # Install scapy properly
   pip install scapy
   sudo apt-get install python3-scapy  # Linux
   ```

3. **GUI Not Available**
   ```bash
   # Install tkinter
   sudo apt-get install python3-tk  # Linux
   ```

### Debug Mode
```bash
# Enable debug output
python wifi_security_toolkit.py --debug
```

## Contributing

We welcome contributions to improve the toolkit:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

### Development Setup
```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
python -m pytest tests/

# Code formatting
black wifi_security_toolkit.py
```

## Legal and Ethical Considerations

### Authorized Use Only
- Use only on networks you own or have permission to test
- Obtain written authorization before testing
- Respect privacy and data protection laws
- Follow responsible disclosure practices

### Educational Purpose
- This tool is designed for learning and research
- All attack simulations are educational demonstrations
- Focus on defensive security and protection
- Promote security awareness and best practices

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:
- Create an issue on GitHub
- Check the documentation
- Review the troubleshooting section
- Contact the development team

## Acknowledgments

- Security research community
- Open source contributors
- Educational institutions
- Security professionals and researchers

---

**Remember: This tool is for educational and authorized security research only. Always use responsibly and ethically.**