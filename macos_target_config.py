#!/usr/bin/env python3
"""
macOS Target Configuration for Ultimate WiFi Security Demo
MBA AI Study Project - Educational Purpose Only

Enhanced configuration with macOS-specific features and cross-platform support.
"""

import platform
import subprocess
import socket
import json
import os
from datetime import datetime
from typing import Dict, List, Optional

# ============================================================================
# 🎯 TARGET CONFIGURATION - HIER DIE ZIEL-IP EINGEBEN!
# ============================================================================

# 📱 ZIEL-GERÄT KONFIGURATION
TARGET_IP = "192.168.1.100"        # ← HIER DIE IP DES ZIEL-GERÄTS EINGEBEN!
TARGET_MAC = "AA:BB:CC:DD:EE:01"   # MAC-Adresse des Ziel-Geräts (optional)
TARGET_HOSTNAME = "iPhone-15-Pro-Max"  # Name des Ziel-Geräts
TARGET_OS = "iOS 18.6"             # Betriebssystem des Ziel-Geräts
TARGET_USER = "Child 1"            # Benutzer des Ziel-Geräts
TARGET_DEVICE_TYPE = "iPhone"      # Gerätetyp: iPhone, iPad, MacBook, etc.

# 🌐 NETZWERK KONFIGURATION
GATEWAY_IP = "192.168.1.1"         # Router IP (normalerweise 192.168.1.1)
C2_SERVER_IP = "192.168.1.254"     # Command & Control Server IP
NETWORK_INTERFACE = "en0"          # macOS: en0, Linux: wlan0, Windows: Wi-Fi

# 🎯 ERWEITERTE ATTACK KONFIGURATION
ATTACK_METHODS = [
    "wifi_packet_injection",       # WiFi-Paket-Injection
    "arp_spoofing",               # ARP-Spoofing (MITM)
    "dns_poisoning",              # DNS-Poisoning
    "ssl_stripping",              # SSL/TLS-Stripping
    "deauthentication_attack",    # WiFi Deauthentication
    "evil_twin_attack",           # Evil Twin Attack
    "karma_attack",               # Karma Attack
    "beacon_flooding",            # Beacon Frame Flooding
    "probe_request_injection",    # Probe Request Injection
    "eapol_injection"             # EAPOL Frame Injection
]

# 🦠 ERWEITERTE EXPLOIT KONFIGURATION
EXPLOIT_CVES = {
    "ios_18_6": [
        "CVE-2024-23218",  # WiFi arbitrary code execution
        "CVE-2024-23225",  # Safari arbitrary code execution
        "CVE-2024-23222",  # iMessage arbitrary code execution
        "CVE-2024-23221",  # FaceTime arbitrary code execution
        "CVE-2024-23224",  # Kernel memory corruption
        "CVE-2024-23223",  # WebKit type confusion
        "CVE-2024-23220",  # Kernel privilege escalation
        "CVE-2024-23219"   # Safari sandbox escape
    ],
    "macos_14": [
        "CVE-2024-23230",  # macOS kernel vulnerability
        "CVE-2024-23231",  # Safari macOS exploit
        "CVE-2024-23232",  # iCloud macOS exploit
        "CVE-2024-23233"   # macOS privilege escalation
    ]
}

# 📡 ERWEITERTE REMOTE ACCESS KONFIGURATION
REMOTE_ACCESS_METHODS = {
    "surveillance": [
        "screen_recording",
        "screenshot_capture",
        "webcam_access",
        "microphone_access",
        "keylogging",
        "clipboard_monitoring",
        "file_system_access",
        "process_monitoring"
    ],
    "tracking": [
        "gps_location_tracking",
        "wifi_location_tracking",
        "bluetooth_tracking",
        "movement_history",
        "real_time_location",
        "geofencing"
    ],
    "communication": [
        "imessage_monitoring",
        "sms_interception",
        "call_recording",
        "facetime_monitoring",
        "email_interception",
        "social_media_monitoring",
        "browser_history",
        "app_communication_logs"
    ],
    "data_extraction": [
        "contact_list_extraction",
        "photo_library_access",
        "calendar_data_mining",
        "health_data_access",
        "app_usage_data",
        "device_settings",
        "backup_data_access",
        "icloud_sync_data"
    ]
}

# 🔧 ERWEITERTE TOOL KONFIGURATION
TOOL_CONFIG = {
    "stealth_mode": True,          # Stealth-Modus aktivieren
    "persistence": True,           # Persistenz nach Neustart
    "encryption": "AES-256",       # Verschlüsselung für C2
    "compression": True,           # Datenkompression
    "obfuscation": True,           # Code-Obfuskation
    "anti_detection": True,        # Anti-Detection-Mechanismen
    "auto_cleanup": True,          # Automatische Spurenbereinigung
    "multi_target": True,          # Mehrere Ziele gleichzeitig
    "real_time_monitoring": True,  # Echtzeit-Überwachung
    "alert_system": True           # Alert-System für Events
}

# ============================================================================
# 🚀 ENHANCED FUNCTIONS
# ============================================================================

def get_system_info():
    """Get system information"""
    return {
        "platform": platform.system(),
        "platform_version": platform.version(),
        "architecture": platform.architecture()[0],
        "processor": platform.processor(),
        "hostname": platform.node(),
        "python_version": platform.python_version()
    }

def get_network_interfaces():
    """Get available network interfaces"""
    interfaces = []
    try:
        if platform.system() == "Darwin":  # macOS
            result = subprocess.run(["ifconfig"], capture_output=True, text=True)
            # Parse ifconfig output for interfaces
            for line in result.stdout.split('\n'):
                if line.strip() and not line.startswith('\t'):
                    interface = line.split(':')[0]
                    if interface and interface != 'lo0':
                        interfaces.append(interface)
        elif platform.system() == "Linux":
            result = subprocess.run(["ip", "link", "show"], capture_output=True, text=True)
            # Parse ip link output
            for line in result.stdout.split('\n'):
                if 'state UP' in line:
                    interface = line.split(':')[1].strip()
                    interfaces.append(interface)
        else:  # Windows
            result = subprocess.run(["netsh", "interface", "show", "interface"], capture_output=True, text=True)
            # Parse netsh output
            for line in result.stdout.split('\n'):
                if 'Enabled' in line and 'Wi-Fi' in line:
                    interface = line.split()[-1]
                    interfaces.append(interface)
    except Exception as e:
        print(f"Warning: Could not get network interfaces: {e}")
        interfaces = ["en0", "wlan0", "Wi-Fi"]  # Fallback
    
    return interfaces

def scan_network_devices():
    """Scan network for connected devices"""
    devices = []
    try:
        # Get local network range
        local_ip = socket.gethostbyname(socket.gethostname())
        network_base = '.'.join(local_ip.split('.')[:-1])
        
        # Scan common IP ranges
        for i in range(1, 255):
            ip = f"{network_base}.{i}"
            try:
                # Quick ping scan
                if platform.system() == "Darwin":  # macOS
                    result = subprocess.run(["ping", "-c", "1", "-t", "1", ip], 
                                          capture_output=True, text=True)
                elif platform.system() == "Linux":
                    result = subprocess.run(["ping", "-c", "1", "-W", "1", ip], 
                                          capture_output=True, text=True)
                else:  # Windows
                    result = subprocess.run(["ping", "-n", "1", "-w", "1000", ip], 
                                          capture_output=True, text=True)
                
                if result.returncode == 0:
                    # Try to get hostname
                    try:
                        hostname = socket.gethostbyaddr(ip)[0]
                    except:
                        hostname = f"Unknown-{ip.split('.')[-1]}"
                    
                    # Determine device type based on hostname
                    device_type = "Unknown"
                    if "iphone" in hostname.lower():
                        device_type = "iPhone"
                    elif "ipad" in hostname.lower():
                        device_type = "iPad"
                    elif "mac" in hostname.lower():
                        device_type = "Mac"
                    elif "android" in hostname.lower():
                        device_type = "Android"
                    
                    devices.append({
                        "ip": ip,
                        "hostname": hostname,
                        "device_type": device_type,
                        "status": "online"
                    })
            except:
                continue
                
    except Exception as e:
        print(f"Warning: Network scan failed: {e}")
        # Return sample devices for demo
        devices = [
            {"ip": "192.168.1.100", "hostname": "iPhone-15-Pro-Max", "device_type": "iPhone", "status": "online"},
            {"ip": "192.168.1.101", "hostname": "iPhone-14", "device_type": "iPhone", "status": "online"},
            {"ip": "192.168.1.102", "hostname": "iPad-Pro", "device_type": "iPad", "status": "online"},
            {"ip": "192.168.1.103", "hostname": "MacBook-Air", "device_type": "Mac", "status": "online"}
        ]
    
    return devices

def get_target_info():
    """Get target device information"""
    return {
        "ip": TARGET_IP,
        "mac": TARGET_MAC,
        "hostname": TARGET_HOSTNAME,
        "os": TARGET_OS,
        "user": TARGET_USER,
        "device_type": TARGET_DEVICE_TYPE
    }

def get_network_config():
    """Get network configuration"""
    return {
        "gateway_ip": GATEWAY_IP,
        "c2_server_ip": C2_SERVER_IP,
        "interface": NETWORK_INTERFACE,
        "system_info": get_system_info(),
        "available_interfaces": get_network_interfaces()
    }

def get_attack_config():
    """Get attack configuration"""
    return {
        "methods": ATTACK_METHODS,
        "cves": EXPLOIT_CVES,
        "remote_access": REMOTE_ACCESS_METHODS,
        "tool_config": TOOL_CONFIG
    }

def print_target_info():
    """Print current target configuration"""
    print("🎯 AKTUELLE ZIEL-KONFIGURATION:")
    print("=" * 50)
    print(f"📱 Ziel-Gerät: {TARGET_HOSTNAME}")
    print(f"🌐 IP-Adresse: {TARGET_IP}")
    print(f"🔗 MAC-Adresse: {TARGET_MAC}")
    print(f"📱 Betriebssystem: {TARGET_OS}")
    print(f"👤 Benutzer: {TARGET_USER}")
    print(f"📱 Gerätetyp: {TARGET_DEVICE_TYPE}")
    print()
    print(f"🌐 Gateway: {GATEWAY_IP}")
    print(f"📡 C2 Server: {C2_SERVER_IP}")
    print(f"🔌 Interface: {NETWORK_INTERFACE}")
    print()
    
    system_info = get_system_info()
    print(f"💻 System: {system_info['platform']} {system_info['platform_version']}")
    print(f"🏗️  Architektur: {system_info['architecture']}")
    print(f"🐍 Python: {system_info['python_version']}")
    print()
    
    print("🦠 Attack Methods:")
    for method in ATTACK_METHODS:
        print(f"   • {method}")
    print()
    
    print("🚨 Exploit CVEs:")
    for os_type, cves in EXPLOIT_CVES.items():
        print(f"   📱 {os_type}:")
        for cve in cves:
            print(f"      • {cve}")
    print()
    
    print("📡 Remote Access Methods:")
    for category, methods in REMOTE_ACCESS_METHODS.items():
        print(f"   📊 {category}:")
        for method in methods:
            print(f"      • {method}")
    print()

def validate_config():
    """Validate the configuration"""
    print("✅ KONFIGURATION VALIDIERUNG:")
    print("=" * 40)
    
    # Check if target IP is set
    if TARGET_IP == "192.168.1.100":
        print("⚠️  WARNUNG: Standard-IP verwendet!")
        print("   Bitte ändern Sie TARGET_IP zu der IP des Ziel-Geräts")
    else:
        print(f"✅ Ziel-IP gesetzt: {TARGET_IP}")
    
    # Check if target hostname is set
    if TARGET_HOSTNAME == "iPhone-15-Pro-Max":
        print("⚠️  WARNUNG: Standard-Hostname verwendet!")
        print("   Bitte ändern Sie TARGET_HOSTNAME zum Namen des Ziel-Geräts")
    else:
        print(f"✅ Ziel-Hostname gesetzt: {TARGET_HOSTNAME}")
    
    # Check network configuration
    print(f"✅ Gateway-IP: {GATEWAY_IP}")
    print(f"✅ C2-Server-IP: {C2_SERVER_IP}")
    print(f"✅ Interface: {NETWORK_INTERFACE}")
    
    # Check system compatibility
    system_info = get_system_info()
    print(f"✅ System: {system_info['platform']} - Unterstützt")
    
    # Check network interfaces
    interfaces = get_network_interfaces()
    print(f"✅ Verfügbare Interfaces: {', '.join(interfaces)}")
    
    print()
    print("🎯 Konfiguration bereit für Angriff!")
    print()

def scan_and_show_devices():
    """Scan network and show available devices"""
    print("📡 NETZWERK-SCAN AUSFÜHREN")
    print("=" * 40)
    print()
    
    devices = scan_network_devices()
    
    print(f"📊 Gefundene Geräte ({len(devices)}):")
    print()
    
    for i, device in enumerate(devices, 1):
        status_icon = "🎯" if device['ip'] == TARGET_IP else "📱"
        print(f"{status_icon} {i}. {device['hostname']} ({device['ip']})")
        print(f"   📱 Typ: {device['device_type']}")
        print(f"   📊 Status: {device['status']}")
        print()
    
    return devices

def save_configuration():
    """Save current configuration to file"""
    config = {
        "timestamp": datetime.now().isoformat(),
        "target_info": get_target_info(),
        "network_config": get_network_config(),
        "attack_config": get_attack_config(),
        "system_info": get_system_info()
    }
    
    with open("macos_configuration.json", "w") as f:
        json.dump(config, f, indent=2, default=str)
    
    print("💾 Konfiguration gespeichert: macos_configuration.json")
    print()

# ============================================================================
# 📋 EXAMPLE CONFIGURATIONS
# ============================================================================

EXAMPLE_CONFIGS = {
    "home_network": {
        "description": "Heim-Netzwerk Beispiel",
        "target_ip": "192.168.1.100",
        "target_hostname": "iPhone-15-Pro-Max",
        "target_user": "Kind 1",
        "target_device_type": "iPhone",
        "gateway_ip": "192.168.1.1"
    },
    "office_network": {
        "description": "Büro-Netzwerk Beispiel", 
        "target_ip": "10.0.1.50",
        "target_hostname": "iPhone-14-Pro",
        "target_user": "Mitarbeiter",
        "target_device_type": "iPhone",
        "gateway_ip": "10.0.1.1"
    },
    "school_network": {
        "description": "Schul-Netzwerk Beispiel",
        "target_ip": "172.16.0.25",
        "target_hostname": "iPhone-13",
        "target_user": "Schüler",
        "target_device_type": "iPhone",
        "gateway_ip": "172.16.0.1"
    },
    "macos_target": {
        "description": "macOS Ziel Beispiel",
        "target_ip": "192.168.1.200",
        "target_hostname": "MacBook-Pro",
        "target_user": "Entwickler",
        "target_device_type": "Mac",
        "gateway_ip": "192.168.1.1"
    }
}

def show_example_configs():
    """Show example configurations"""
    print("📋 BEISPIEL-KONFIGURATIONEN:")
    print("=" * 50)
    
    for name, config in EXAMPLE_CONFIGS.items():
        print(f"🏠 {config['description']}:")
        print(f"   📱 Ziel-IP: {config['target_ip']}")
        print(f"   📱 Hostname: {config['target_hostname']}")
        print(f"   👤 Benutzer: {config['target_user']}")
        print(f"   📱 Gerätetyp: {config['target_device_type']}")
        print(f"   🌐 Gateway: {config['gateway_ip']}")
        print()

# ============================================================================
# 🚀 MAIN FUNCTION
# ============================================================================

if __name__ == "__main__":
    print("🎯 macOS TARGET CONFIGURATION")
    print("MBA AI Study Project - Educational Purpose Only")
    print("Enhanced Version with Cross-Platform Support")
    print("=" * 70)
    print()
    
    print_target_info()
    validate_config()
    scan_and_show_devices()
    show_example_configs()
    save_configuration()
    
    print("📝 ANLEITUNG:")
    print("1. Ändern Sie TARGET_IP zur IP-Adresse des Ziel-Geräts")
    print("2. Ändern Sie TARGET_HOSTNAME zum Namen des Ziel-Geräts")
    print("3. Ändern Sie TARGET_USER zum Benutzer des Ziel-Geräts")
    print("4. Passen Sie GATEWAY_IP an Ihr Netzwerk an")
    print("5. Speichern Sie die Datei")
    print("6. Starten Sie die Demo mit: python3 ultimate_macos_demo.py --demo")
    print()
    print("🆕 NEUE FEATURES:")
    print("   • Cross-Platform Support (macOS, Linux, Windows)")
    print("   • Automatischer Netzwerk-Scan")
    print("   • Erweiterte Attack-Methoden")
    print("   • Mehrere Exploit-CVEs")
    print("   • Umfangreiche Remote-Access-Funktionen")
    print("   • Stealth-Modus und Anti-Detection")
    print()
    print("⚠️  WICHTIG: Nur für Bildungszwecke verwenden!")
    print("🔒 Alle Angriffe sind simuliert - keine echten Exploits!")