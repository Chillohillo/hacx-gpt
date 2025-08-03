#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ultimate WiFi Security Research Toolkit
Version 2.1 - Strictly for Educational and Research Purposes

This toolkit demonstrates security concepts for educational purposes only.
It is designed to help security professionals understand vulnerabilities
and develop defensive strategies. All features are simulated and do not
perform actual exploitation.

WARNING: This tool is for authorized security research only.
Run with sudo in controlled test environments only.
"""

import os
import sys
import json
import time
import threading
import subprocess
import socket
import random
import math
import argparse
import platform
from datetime import datetime
from collections import defaultdict
from typing import Dict, List, Optional, Tuple
import ipaddress

# GUI Libraries
try:
    import tkinter as tk
    from tkinter import ttk, scrolledtext, filedialog, messagebox
    GUI_AVAILABLE = True
except ImportError:
    GUI_AVAILABLE = False

# Network Libraries
try:
    import scapy.all as scapy
    from scapy.layers.inet import IP, ICMP
    from scapy.layers.l2 import Ether, ARP
    from scapy.layers.dot11 import Dot11, Dot11Beacon, Dot11Elt, Dot11ProbeResp
    SCAPY_AVAILABLE = True
except ImportError:
    SCAPY_AVAILABLE = False

# Data Visualization
try:
    import matplotlib
    matplotlib.use('TkAgg' if GUI_AVAILABLE else 'Agg')
    import matplotlib.pyplot as plt
    import matplotlib.animation as animation
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

# Report Generation
try:
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.lib import colors
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False

# Rich Console Output
try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.progress import Progress, SpinnerColumn, TextColumn
    from rich.live import Live
    from rich.text import Text
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False
    # Fallback for when rich is not available
    class Console:
        def __init__(self):
            pass
        def print(self, *args, **kwargs):
            print(*args)

# Configuration
class Config:
    """Centralized configuration for the WiFi Security Toolkit."""
    
    # Tool Settings
    TOOL_NAME = "WiFi Security Research Toolkit"
    VERSION = "2.1"
    AUTHOR = "Security Research Team"
    
    # Network Settings
    SCAN_TIMEOUT = 5
    MAX_RETRIES = 3
    PACKET_COUNT = 100
    
    # Security Settings
    TEST_NETWORK_PREFIXES = [
        "192.168.1.", "192.168.0.", "10.0.0.", "172.16.0.",
        "192.168.100.", "192.168.50.", "10.0.1.", "172.20.0."
    ]
    
    # File Paths
    REPORTS_DIR = "reports"
    LOGS_DIR = "logs"
    CONFIGS_DIR = "configs"
    
    # Colors for console output
    class colors:
        SUCCESS = "\033[92m"
        WARNING = "\033[93m"
        ERROR = "\033[91m"
        INFO = "\033[94m"
        RESET = "\033[0m"
        BOLD = "\033[1m"

class NetworkDevice:
    """Represents a network device with security information."""
    
    def __init__(self, ip: str, mac: str = None, hostname: str = None, os: str = None):
        self.ip = ip
        self.mac = mac
        self.hostname = hostname
        self.os = os
        self.vulnerabilities = []
        self.ports = []
        self.services = []
        self.last_seen = datetime.now()
        self.security_score = 100  # 0-100, higher is more secure
        
    def to_dict(self) -> Dict:
        """Convert device to dictionary for JSON serialization."""
        return {
            'ip': self.ip,
            'mac': self.mac,
            'hostname': self.hostname,
            'os': self.os,
            'vulnerabilities': self.vulnerabilities,
            'ports': self.ports,
            'services': self.services,
            'last_seen': self.last_seen.isoformat(),
            'security_score': self.security_score
        }

class WiFiNetwork:
    """Represents a WiFi network with security information."""
    
    def __init__(self, ssid: str, bssid: str, channel: int, encryption: str):
        self.ssid = ssid
        self.bssid = bssid
        self.channel = channel
        self.encryption = encryption
        self.signal_strength = 0
        self.clients = []
        self.vulnerabilities = []
        self.security_score = 100
        
    def to_dict(self) -> Dict:
        """Convert network to dictionary for JSON serialization."""
        return {
            'ssid': self.ssid,
            'bssid': self.bssid,
            'channel': self.channel,
            'encryption': self.encryption,
            'signal_strength': self.signal_strength,
            'clients': self.clients,
            'vulnerabilities': self.vulnerabilities,
            'security_score': self.security_score
        }

class NetworkScanner:
    """Handles network discovery and device enumeration."""
    
    def __init__(self, console: Console = None):
        self.console = console
        self.devices = {}
        self.networks = {}
        self.scan_results = {}
        
    def is_test_network(self, ip: str) -> bool:
        """Check if IP is in a test network range."""
        try:
            ip_obj = ipaddress.ip_address(ip)
            for prefix in Config.TEST_NETWORK_PREFIXES:
                if ip.startswith(prefix):
                    return True
            return False
        except:
            return False
    
    def scan_network(self, network: str) -> Dict:
        """Scan network for devices using ARP requests."""
        if not SCAPY_AVAILABLE:
            self._log("Scapy not available. Using ping scan.", "warning")
            return self._ping_scan(network)
        
        self._log(f"Scanning network: {network}", "info")
        devices = {}
        
        try:
            # Create ARP request packet
            arp_request = scapy.ARP(pdst=network)
            broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
            arp_request_broadcast = broadcast/arp_request
            
            # Send packets and capture responses
            answered_list = scapy.srp(arp_request_broadcast, timeout=Config.SCAN_TIMEOUT, verbose=False)[0]
            
            for element in answered_list:
                ip = element[1].psrc
                mac = element[1].hwsrc
                
                if self.is_test_network(ip):
                    device = NetworkDevice(ip=ip, mac=mac)
                    devices[ip] = device
                    self._log(f"Found device: {ip} ({mac})", "success")
                    
        except Exception as e:
            self._log(f"Error during network scan: {e}", "error")
            
        return devices
    
    def _ping_scan(self, network: str) -> Dict:
        """Fallback ping scan when Scapy is not available."""
        devices = {}
        base_ip = network.rstrip('.')
        
        self._log("Using ping scan (fallback method)", "warning")
        
        for i in range(1, 255):
            ip = f"{base_ip}.{i}"
            if self._ping_host(ip):
                device = NetworkDevice(ip=ip)
                devices[ip] = device
                self._log(f"Found device: {ip}", "success")
                
        return devices
    
    def _ping_host(self, ip: str) -> bool:
        """Ping a single host to check if it's alive."""
        try:
            param = '-n' if platform.system().lower() == 'windows' else '-c'
            command = ['ping', param, '1', ip]
            return subprocess.call(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0
        except:
            return False
    
    def detect_os(self, ip: str) -> str:
        """Attempt to detect OS using various methods."""
        # This is a simplified OS detection
        # In a real implementation, you'd use more sophisticated methods
        os_signatures = {
            'Linux': ['Linux', 'Ubuntu', 'Debian'],
            'Windows': ['Windows', 'Microsoft'],
            'macOS': ['Darwin', 'Mac'],
            'iOS': ['iPhone', 'iPad', 'iOS'],
            'Android': ['Android']
        }
        
        # Simulate OS detection
        detected_os = random.choice(['Linux', 'Windows', 'macOS', 'iOS', 'Android'])
        return detected_os
    
    def scan_ports(self, ip: str, ports: List[int] = None) -> List[int]:
        """Scan common ports on a device."""
        if ports is None:
            ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 993, 995, 3306, 3389, 5432, 8080]
        
        open_ports = []
        for port in ports:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex((ip, port))
                if result == 0:
                    open_ports.append(port)
                sock.close()
            except:
                pass
                
        return open_ports
    
    def _log(self, message: str, level: str = "info"):
        """Log messages with appropriate formatting."""
        if self.console:
            color_map = {
                "info": "blue",
                "success": "green", 
                "warning": "yellow",
                "error": "red"
            }
            color = color_map.get(level, "white")
            self.console.print(f"[{color}]{message}[/{color}]")
        else:
            print(f"[{level.upper()}] {message}")

class SecurityAnalyzer:
    """Analyzes security vulnerabilities in networks and devices."""
    
    def __init__(self, console: Console = None):
        self.console = console
        self.vulnerability_db = self._load_vulnerability_db()
        
    def _load_vulnerability_db(self) -> Dict:
        """Load vulnerability database."""
        return {
            'weak_encryption': {
                'name': 'Weak WiFi Encryption',
                'description': 'Network uses WEP or WPA1 encryption',
                'severity': 'High',
                'mitigation': 'Upgrade to WPA2/WPA3'
            },
            'open_network': {
                'name': 'Open WiFi Network',
                'description': 'Network has no encryption',
                'severity': 'Critical',
                'mitigation': 'Enable WPA2/WPA3 encryption'
            },
            'default_credentials': {
                'name': 'Default Credentials',
                'description': 'Device uses default username/password',
                'severity': 'High',
                'mitigation': 'Change default credentials'
            },
            'open_ports': {
                'name': 'Unnecessary Open Ports',
                'description': 'Device has unnecessary services exposed',
                'severity': 'Medium',
                'mitigation': 'Close unused ports and services'
            },
            'outdated_firmware': {
                'name': 'Outdated Firmware',
                'description': 'Device firmware is outdated',
                'severity': 'Medium',
                'mitigation': 'Update to latest firmware'
            }
        }
    
    def analyze_device(self, device: NetworkDevice) -> List[Dict]:
        """Analyze a single device for vulnerabilities."""
        vulnerabilities = []
        
        # Check for open ports
        if device.ports:
            if any(port in [21, 23, 3389] for port in device.ports):
                vulnerabilities.append(self.vulnerability_db['open_ports'])
        
        # Simulate other vulnerability checks
        if random.random() < 0.3:  # 30% chance of default credentials
            vulnerabilities.append(self.vulnerability_db['default_credentials'])
        
        if random.random() < 0.4:  # 40% chance of outdated firmware
            vulnerabilities.append(self.vulnerability_db['outdated_firmware'])
        
        device.vulnerabilities = vulnerabilities
        device.security_score = max(0, 100 - len(vulnerabilities) * 20)
        
        return vulnerabilities
    
    def analyze_network(self, network: WiFiNetwork) -> List[Dict]:
        """Analyze a WiFi network for vulnerabilities."""
        vulnerabilities = []
        
        # Check encryption
        if network.encryption.lower() in ['wep', 'wpa1', 'none']:
            if network.encryption.lower() == 'none':
                vulnerabilities.append(self.vulnerability_db['open_network'])
            else:
                vulnerabilities.append(self.vulnerability_db['weak_encryption'])
        
        network.vulnerabilities = vulnerabilities
        network.security_score = max(0, 100 - len(vulnerabilities) * 25)
        
        return vulnerabilities

class AttackSimulator:
    """Simulates various WiFi attacks for educational purposes."""
    
    def __init__(self, console: Console = None):
        self.console = console
        self.is_running = False
        self.attack_thread = None
        
    def deauth_attack_simulation(self, target_bssid: str, duration: int = 30):
        """Simulate deauthentication attack (educational only)."""
        if not self.is_test_environment():
            self._log("Attack simulation only allowed in test environments!", "error")
            return False
        
        self._log(f"Simulating deauthentication attack on {target_bssid}", "warning")
        self._log("This is for educational purposes only!", "warning")
        
        # Simulate attack progress
        if RICH_AVAILABLE:
            with Progress() as progress:
                task = progress.add_task("Deauth Attack Simulation", total=duration)
                
                for i in range(duration):
                    time.sleep(1)
                    progress.update(task, advance=1)
                    
                    if i % 5 == 0:
                        self._log(f"Simulated deauth packet {i+1} sent", "info")
        else:
            # Fallback progress simulation
            for i in range(duration):
                time.sleep(1)
                if i % 5 == 0:
                    self._log(f"Simulated deauth packet {i+1} sent", "info")
        
        self._log("Deauthentication attack simulation completed", "success")
        return True
    
    def evil_twin_simulation(self, target_ssid: str, duration: int = 30):
        """Simulate evil twin attack (educational only)."""
        if not self.is_test_environment():
            self._log("Attack simulation only allowed in test environments!", "error")
            return False
        
        self._log(f"Simulating evil twin attack for {target_ssid}", "warning")
        self._log("This is for educational purposes only!", "warning")
        
        # Simulate creating fake AP
        if RICH_AVAILABLE:
            with Progress() as progress:
                task = progress.add_task("Evil Twin Simulation", total=duration)
                
                for i in range(duration):
                    time.sleep(1)
                    progress.update(task, advance=1)
                    
                    if i % 10 == 0:
                        self._log(f"Simulated fake AP beacon {i+1} sent", "info")
        else:
            # Fallback progress simulation
            for i in range(duration):
                time.sleep(1)
                if i % 10 == 0:
                    self._log(f"Simulated fake AP beacon {i+1} sent", "info")
        
        self._log("Evil twin attack simulation completed", "success")
        return True
    
    def karma_attack_simulation(self, duration: int = 30):
        """Simulate KARMA attack (educational only)."""
        if not self.is_test_environment():
            self._log("Attack simulation only allowed in test environments!", "error")
            return False
        
        self._log("Simulating KARMA attack", "warning")
        self._log("This is for educational purposes only!", "warning")
        
        # Simulate attack progress
        if RICH_AVAILABLE:
            with Progress() as progress:
                task = progress.add_task("KARMA Attack Simulation", total=duration)
                
                for i in range(duration):
                    time.sleep(1)
                    progress.update(task, advance=1)
                    
                    if i % 8 == 0:
                        self._log(f"Simulated probe response {i+1} sent", "info")
        else:
            # Fallback progress simulation
            for i in range(duration):
                time.sleep(1)
                if i % 8 == 0:
                    self._log(f"Simulated probe response {i+1} sent", "info")
        
        self._log("KARMA attack simulation completed", "success")
        return True
    
    def is_test_environment(self) -> bool:
        """Check if we're in a test environment."""
        # Check if we're in a test network
        try:
            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)
            
            for prefix in Config.TEST_NETWORK_PREFIXES:
                if local_ip.startswith(prefix):
                    return True
            return False
        except:
            return False
    
    def _log(self, message: str, level: str = "info"):
        """Log messages with appropriate formatting."""
        if self.console:
            color_map = {
                "info": "blue",
                "success": "green", 
                "warning": "yellow",
                "error": "red"
            }
            color = color_map.get(level, "white")
            self.console.print(f"[{color}]{message}[/{color}]")
        else:
            print(f"[{level.upper()}] {message}")

class ReportGenerator:
    """Generates security reports in various formats."""
    
    def __init__(self, console: Console = None):
        self.console = console
        self.reports_dir = Config.REPORTS_DIR
        os.makedirs(self.reports_dir, exist_ok=True)
        
    def generate_json_report(self, devices: Dict, networks: Dict, filename: str = None) -> str:
        """Generate JSON report."""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"wifi_security_report_{timestamp}.json"
        
        filepath = os.path.join(self.reports_dir, filename)
        
        report_data = {
            'scan_timestamp': datetime.now().isoformat(),
            'devices': {ip: device.to_dict() for ip, device in devices.items()},
            'networks': {ssid: network.to_dict() for ssid, network in networks.items()},
            'summary': {
                'total_devices': len(devices),
                'total_networks': len(networks),
                'high_risk_devices': len([d for d in devices.values() if d.security_score < 50]),
                'high_risk_networks': len([n for n in networks.values() if n.security_score < 50])
            }
        }
        
        with open(filepath, 'w') as f:
            json.dump(report_data, f, indent=2)
        
        self._log(f"JSON report saved to: {filepath}", "success")
        return filepath
    
    def generate_pdf_report(self, devices: Dict, networks: Dict, filename: str = None) -> str:
        """Generate PDF report."""
        if not REPORTLAB_AVAILABLE:
            self._log("ReportLab not available. Skipping PDF report.", "warning")
            return None
        
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"wifi_security_report_{timestamp}.pdf"
        
        filepath = os.path.join(self.reports_dir, filename)
        
        doc = SimpleDocTemplate(filepath, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []
        
        # Title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=1
        )
        story.append(Paragraph("WiFi Security Research Report", title_style))
        story.append(Spacer(1, 12))
        
        # Summary
        story.append(Paragraph("Executive Summary", styles['Heading2']))
        story.append(Paragraph(f"""
        This report presents the findings of a comprehensive WiFi security assessment conducted on {datetime.now().strftime('%B %d, %Y')}.
        
        Key Findings:
        • Total devices discovered: {len(devices)}
        • Total networks analyzed: {len(networks)}
        • High-risk devices: {len([d for d in devices.values() if d.security_score < 50])}
        • High-risk networks: {len([n for n in networks.values() if n.security_score < 50])}
        """, styles['Normal']))
        story.append(Spacer(1, 12))
        
        # Devices section
        if devices:
            story.append(Paragraph("Network Devices", styles['Heading2']))
            device_data = [['IP Address', 'MAC', 'OS', 'Security Score', 'Vulnerabilities']]
            
            for device in devices.values():
                vulns = len(device.vulnerabilities)
                device_data.append([
                    device.ip,
                    device.mac or 'Unknown',
                    device.os or 'Unknown',
                    str(device.security_score),
                    str(vulns)
                ])
            
            device_table = Table(device_data)
            device_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 14),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            story.append(device_table)
            story.append(Spacer(1, 12))
        
        # Networks section
        if networks:
            story.append(Paragraph("WiFi Networks", styles['Heading2']))
            network_data = [['SSID', 'BSSID', 'Channel', 'Encryption', 'Security Score']]
            
            for network in networks.values():
                network_data.append([
                    network.ssid,
                    network.bssid,
                    str(network.channel),
                    network.encryption,
                    str(network.security_score)
                ])
            
            network_table = Table(network_data)
            network_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 14),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            story.append(network_table)
        
        doc.build(story)
        self._log(f"PDF report saved to: {filepath}", "success")
        return filepath
    
    def _log(self, message: str, level: str = "info"):
        """Log messages with appropriate formatting."""
        if self.console:
            color_map = {
                "info": "blue",
                "success": "green", 
                "warning": "yellow",
                "error": "red"
            }
            color = color_map.get(level, "white")
            self.console.print(f"[{color}]{message}[/{color}]")
        else:
            print(f"[{level.upper()}] {message}")

class WiFiSecurityToolkit:
    """Main WiFi Security Research Toolkit."""
    
    def __init__(self):
        self.console = Console() if RICH_AVAILABLE else None
        self.scanner = NetworkScanner(self.console)
        self.analyzer = SecurityAnalyzer(self.console)
        self.attacker = AttackSimulator(self.console)
        self.reporter = ReportGenerator(self.console)
        
    def display_banner(self):
        """Display the toolkit banner."""
        banner = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                    WiFi Security Research Toolkit v2.1                        ║
║                        Educational & Research Purposes Only                   ║
║                              Authorized Testing Only                         ║
╚══════════════════════════════════════════════════════════════════════════════╝
        """
        if self.console:
            self.console.print(Panel(banner, style="bold cyan"))
        else:
            print(banner)
    
    def display_menu(self):
        """Display the main menu."""
        menu = """
[1] Network Discovery
[2] Security Analysis
[3] Attack Simulations (Educational Only)
[4] Generate Reports
[5] Interactive Mode
[6] Exit
        """
        if self.console:
            self.console.print(Panel(menu, title="Main Menu", border_style="cyan"))
        else:
            print(menu)
    
    def network_discovery(self):
        """Perform network discovery."""
        self._log("Starting network discovery...", "info")
        
        # Get local network
        try:
            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)
            network = '.'.join(local_ip.split('.')[:-1]) + '.0/24'
        except:
            network = "192.168.1.0/24"  # Fallback
        
        self._log(f"Scanning network: {network}", "info")
        
        # Scan for devices
        devices = self.scanner.scan_network(network)
        
        # Analyze each device
        for device in devices.values():
            device.os = self.scanner.detect_os(device.ip)
            device.ports = self.scanner.scan_ports(device.ip)
            self.analyzer.analyze_device(device)
        
        self.scanner.devices = devices
        
        # Display results
        self._display_devices(devices)
        
        return devices
    
    def security_analysis(self):
        """Perform comprehensive security analysis."""
        self._log("Starting security analysis...", "info")
        
        # First discover devices if not already done
        if not self.scanner.devices:
            self.network_discovery()
        
        # Analyze each device
        total_vulns = 0
        for device in self.scanner.devices.values():
            vulns = self.analyzer.analyze_device(device)
            total_vulns += len(vulns)
            
            if vulns:
                self._log(f"Device {device.ip} has {len(vulns)} vulnerabilities", "warning")
        
        self._log(f"Security analysis complete. Found {total_vulns} total vulnerabilities.", "info")
        
        return self.scanner.devices
    
    def attack_simulations(self):
        """Run attack simulations (educational only)."""
        self._log("Attack Simulations (Educational Purposes Only)", "warning")
        
        if not self.attacker.is_test_environment():
            self._log("ERROR: Attack simulations only allowed in test environments!", "error")
            return
        
        menu = """
[1] Deauthentication Attack Simulation
[2] Evil Twin Attack Simulation  
[3] KARMA Attack Simulation
[4] Back to Main Menu
        """
        
        while True:
            if self.console:
                self.console.print(Panel(menu, title="Attack Simulations", border_style="red"))
            else:
                print(menu)
            
            choice = input("Select attack simulation: ")
            
            if choice == '1':
                target = input("Enter target BSSID: ")
                self.attacker.deauth_attack_simulation(target)
            elif choice == '2':
                target = input("Enter target SSID: ")
                self.attacker.evil_twin_simulation(target)
            elif choice == '3':
                self.attacker.karma_attack_simulation()
            elif choice == '4':
                break
            else:
                self._log("Invalid choice", "error")
    
    def generate_reports(self):
        """Generate security reports."""
        self._log("Generating reports...", "info")
        
        # Ensure we have data to report
        if not self.scanner.devices:
            self._log("No devices found. Running network discovery first...", "info")
            self.network_discovery()
        
        # Generate JSON report
        json_path = self.reporter.generate_json_report(
            self.scanner.devices, 
            self.scanner.networks
        )
        
        # Generate PDF report
        pdf_path = self.reporter.generate_pdf_report(
            self.scanner.devices,
            self.scanner.networks
        )
        
        self._log("Report generation complete!", "success")
        
        if json_path:
            self._log(f"JSON report: {json_path}", "info")
        if pdf_path:
            self._log(f"PDF report: {pdf_path}", "info")
    
    def interactive_mode(self):
        """Run in interactive mode."""
        self._log("Starting interactive mode...", "info")
        
        while True:
            try:
                command = input("wifi-toolkit> ")
                
                if command.lower() in ['exit', 'quit']:
                    break
                elif command.lower() == 'scan':
                    self.network_discovery()
                elif command.lower() == 'analyze':
                    self.security_analysis()
                elif command.lower() == 'report':
                    self.generate_reports()
                elif command.lower() == 'help':
                    self._display_help()
                else:
                    self._log(f"Unknown command: {command}", "error")
                    
            except KeyboardInterrupt:
                break
            except Exception as e:
                self._log(f"Error: {e}", "error")
    
    def _display_devices(self, devices: Dict):
        """Display discovered devices in a table."""
        if not devices:
            self._log("No devices found", "warning")
            return
        
        if self.console:
            table = Table(title="Discovered Devices")
            table.add_column("IP Address", style="cyan")
            table.add_column("MAC Address", style="magenta")
            table.add_column("OS", style="green")
            table.add_column("Security Score", style="yellow")
            table.add_column("Vulnerabilities", style="red")
            
            for device in devices.values():
                vulns = len(device.vulnerabilities)
                score_color = "green" if device.security_score >= 70 else "yellow" if device.security_score >= 40 else "red"
                
                table.add_row(
                    device.ip,
                    device.mac or "Unknown",
                    device.os or "Unknown",
                    f"[{score_color}]{device.security_score}[/{score_color}]",
                    str(vulns)
                )
            
            self.console.print(table)
        else:
            print("\nDiscovered Devices:")
            print("-" * 80)
            print(f"{'IP':<15} {'MAC':<17} {'OS':<10} {'Score':<8} {'Vulns':<6}")
            print("-" * 80)
            
            for device in devices.values():
                print(f"{device.ip:<15} {device.mac or 'Unknown':<17} {device.os or 'Unknown':<10} {device.security_score:<8} {len(device.vulnerabilities):<6}")
    
    def _display_help(self):
        """Display help information."""
        help_text = """
Available Commands:
  scan     - Discover devices on network
  analyze  - Perform security analysis
  report   - Generate security reports
  help     - Show this help
  exit     - Exit interactive mode
        """
        self._log(help_text, "info")
    
    def _log(self, message: str, level: str = "info"):
        """Log messages with appropriate formatting."""
        if self.console:
            color_map = {
                "info": "blue",
                "success": "green", 
                "warning": "yellow",
                "error": "red"
            }
            color = color_map.get(level, "white")
            self.console.print(f"[{color}]{message}[/{color}]")
        else:
            print(f"[{level.upper()}] {message}")
    
    def run(self):
        """Main application loop."""
        self.display_banner()
        
        while True:
            self.display_menu()
            choice = input("Select option: ")
            
            if choice == '1':
                self.network_discovery()
            elif choice == '2':
                self.security_analysis()
            elif choice == '3':
                self.attack_simulations()
            elif choice == '4':
                self.generate_reports()
            elif choice == '5':
                self.interactive_mode()
            elif choice == '6':
                self._log("Exiting...", "info")
                break
            else:
                self._log("Invalid choice", "error")

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="WiFi Security Research Toolkit")
    parser.add_argument('--cli', action='store_true', help='Run in CLI mode')
    parser.add_argument('--gui', action='store_true', help='Run in GUI mode')
    parser.add_argument('--scan', action='store_true', help='Run network scan')
    parser.add_argument('--analyze', action='store_true', help='Run security analysis')
    parser.add_argument('--report', action='store_true', help='Generate reports')
    
    args = parser.parse_args()
    
    # Check if running with appropriate privileges
    if os.name != 'nt' and os.geteuid() != 0:
        print("Warning: This tool may require root privileges for full functionality.")
        print("Consider running with sudo for network scanning features.")
    
    toolkit = WiFiSecurityToolkit()
    
    if args.cli or args.gui:
        toolkit.run()
    elif args.scan:
        toolkit.network_discovery()
    elif args.analyze:
        toolkit.security_analysis()
    elif args.report:
        toolkit.generate_reports()
    else:
        toolkit.run()

if __name__ == "__main__":
    main()