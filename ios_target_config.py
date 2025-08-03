#!/usr/bin/env python3
"""
Target Configuration for iOS WiFi Security Demo
MBA AI Study Project - Educational Purpose Only

Configure your target iPhone here!
"""

# ============================================================================
# 🎯 TARGET CONFIGURATION - HIER DIE ZIEL-IP EINGEBEN!
# ============================================================================

# 📱 ZIEL-iPHONE KONFIGURATION
TARGET_IP = "192.168.1.100"        # ← HIER DIE IP DES ZIEL-iPHONES EINGEBEN!
TARGET_MAC = "AA:BB:CC:DD:EE:01"   # MAC-Adresse des Ziel-iPhones (optional)
TARGET_HOSTNAME = "iPhone-15-Pro-Max"  # Name des Ziel-iPhones
TARGET_OS = "iOS 18.6"             # Betriebssystem des Ziel-iPhones
TARGET_USER = "Child 1"            # Benutzer des Ziel-iPhones

# 🌐 NETZWERK KONFIGURATION
GATEWAY_IP = "192.168.1.1"         # Router IP (normalerweise 192.168.1.1)
C2_SERVER_IP = "192.168.1.254"     # Command & Control Server IP
NETWORK_INTERFACE = "wlan0"        # WiFi Interface

# 🎯 ATTACK KONFIGURATION
ATTACK_METHODS = [
    "wifi_packet_injection",       # WiFi-Paket-Injection
    "arp_spoofing",               # ARP-Spoofing (MITM)
    "dns_poisoning",              # DNS-Poisoning
    "ssl_stripping"               # SSL/TLS-Stripping
]

# 🦠 EXPLOIT KONFIGURATION
EXPLOIT_CVES = [
    "CVE-2024-23218",  # WiFi arbitrary code execution
    "CVE-2024-23225",  # Safari arbitrary code execution
    "CVE-2024-23222",  # iMessage arbitrary code execution
    "CVE-2024-23221"   # FaceTime arbitrary code execution
]

# 📡 REMOTE ACCESS KONFIGURATION
REMOTE_ACCESS_METHODS = [
    "screen_recording",
    "keylogging",
    "location_tracking",
    "call_monitoring",
    "message_interception",
    "app_usage_tracking",
    "file_system_access",
    "camera_access",
    "microphone_access",
    "contact_list_access",
    "calendar_access",
    "photo_library_access",
    "safari_history_access",
    "app_store_activity",
    "health_data_access"
]

# ============================================================================
# 🚀 QUICK START FUNCTIONS
# ============================================================================

def get_target_info():
    """Get target device information"""
    return {
        "ip": TARGET_IP,
        "mac": TARGET_MAC,
        "hostname": TARGET_HOSTNAME,
        "os": TARGET_OS,
        "user": TARGET_USER
    }

def get_network_config():
    """Get network configuration"""
    return {
        "gateway_ip": GATEWAY_IP,
        "c2_server_ip": C2_SERVER_IP,
        "interface": NETWORK_INTERFACE
    }

def get_attack_config():
    """Get attack configuration"""
    return {
        "methods": ATTACK_METHODS,
        "cves": EXPLOIT_CVES,
        "remote_access": REMOTE_ACCESS_METHODS
    }

def print_target_info():
    """Print current target configuration"""
    print("🎯 AKTUELLE ZIEL-KONFIGURATION:")
    print("=" * 50)
    print(f"📱 Ziel-iPhone: {TARGET_HOSTNAME}")
    print(f"🌐 IP-Adresse: {TARGET_IP}")
    print(f"🔗 MAC-Adresse: {TARGET_MAC}")
    print(f"📱 Betriebssystem: {TARGET_OS}")
    print(f"👤 Benutzer: {TARGET_USER}")
    print()
    print(f"🌐 Gateway: {GATEWAY_IP}")
    print(f"📡 C2 Server: {C2_SERVER_IP}")
    print(f"🔌 Interface: {NETWORK_INTERFACE}")
    print()
    print("🦠 Attack Methods:")
    for method in ATTACK_METHODS:
        print(f"   • {method}")
    print()
    print("🚨 Exploit CVEs:")
    for cve in EXPLOIT_CVES:
        print(f"   • {cve}")
    print()

def validate_config():
    """Validate the configuration"""
    print("✅ KONFIGURATION VALIDIERUNG:")
    print("=" * 40)
    
    # Check if target IP is set
    if TARGET_IP == "192.168.1.100":
        print("⚠️  WARNUNG: Standard-IP verwendet!")
        print("   Bitte ändern Sie TARGET_IP zu der IP des Ziel-iPhones")
    else:
        print(f"✅ Ziel-IP gesetzt: {TARGET_IP}")
    
    # Check if target hostname is set
    if TARGET_HOSTNAME == "iPhone-15-Pro-Max":
        print("⚠️  WARNUNG: Standard-Hostname verwendet!")
        print("   Bitte ändern Sie TARGET_HOSTNAME zum Namen des Ziel-iPhones")
    else:
        print(f"✅ Ziel-Hostname gesetzt: {TARGET_HOSTNAME}")
    
    # Check network configuration
    print(f"✅ Gateway-IP: {GATEWAY_IP}")
    print(f"✅ C2-Server-IP: {C2_SERVER_IP}")
    print(f"✅ Interface: {NETWORK_INTERFACE}")
    
    print()
    print("🎯 Konfiguration bereit für Angriff!")
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
        "gateway_ip": "192.168.1.1"
    },
    "office_network": {
        "description": "Büro-Netzwerk Beispiel", 
        "target_ip": "10.0.1.50",
        "target_hostname": "iPhone-14-Pro",
        "target_user": "Mitarbeiter",
        "gateway_ip": "10.0.1.1"
    },
    "school_network": {
        "description": "Schul-Netzwerk Beispiel",
        "target_ip": "172.16.0.25",
        "target_hostname": "iPhone-13",
        "target_user": "Schüler",
        "gateway_ip": "172.16.0.1"
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
        print(f"   🌐 Gateway: {config['gateway_ip']}")
        print()

# ============================================================================
# 🚀 MAIN FUNCTION
# ============================================================================

if __name__ == "__main__":
    print("🎯 iOS TARGET CONFIGURATION")
    print("MBA AI Study Project - Educational Purpose Only")
    print("=" * 60)
    print()
    
    print_target_info()
    validate_config()
    show_example_configs()
    
    print("📝 ANLEITUNG:")
    print("1. Ändern Sie TARGET_IP zur IP-Adresse des Ziel-iPhones")
    print("2. Ändern Sie TARGET_HOSTNAME zum Namen des Ziel-iPhones")
    print("3. Ändern Sie TARGET_USER zum Benutzer des Ziel-iPhones")
    print("4. Passen Sie GATEWAY_IP an Ihr Netzwerk an")
    print("5. Speichern Sie die Datei")
    print("6. Starten Sie die Demo mit: python3 ios_ultimate_exploit_demo.py --demo")
    print()
    print("⚠️  WICHTIG: Nur für Bildungszwecke verwenden!")
    print("🔒 Alle Angriffe sind simuliert - keine echten Exploits!")