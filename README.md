# WiFi Security Research Toolkit

Ein umfassendes Python-Toolkit zur Erforschung von WiFi-Sicherheitslücken in Heimnetzwerken, mit besonderem Fokus auf iOS-Geräte. Entwickelt für Sicherheitsforscher, Penetration Tester und Bildungseinrichtungen.

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-Educational%20Use-green)
![Platform](https://img.shields.io/badge/platform-Linux-lightgrey)

## ⚠️ Wichtiger Hinweis

**Dieses Toolkit ist ausschließlich für autorisierte Sicherheitsforschung und Bildungszwecke bestimmt. Die Nutzung in nicht-autorisierten Umgebungen ist illegal und ethisch inakzeptabel.**

## 🎯 Hauptfunktionen

### 🔍 Netzwerkerkennung
- **Automatisierte Geräteerkennung**: ARP-basierte Identifizierung aller Geräte im lokalen Netzwerk
- **OS-Fingerprinting**: Spezielle Erkennung von iOS-Geräten und anderen Betriebssystemen
- **WiFi-Scanning**: Umfassende Analyse von Access Points und deren Konfigurationen
- **Vendor-Identifikation**: MAC-basierte Herstellererkennung

### 🛡️ Sicherheitsanalyse
- **Schwachstellenerkennung**: Automatisierte Identifizierung von Sicherheitslücken
- **Konfigurationsprüfung**: Analyse von Router- und Client-Konfigurationen
- **Verschlüsselungsanalyse**: Bewertung der verwendeten Verschlüsselungsverfahren
- **Korrelationsanalyse**: Verknüpfung von Schwachstellen zwischen Geräten

### 🎭 Angriffssimulationen (Nur in Testumgebungen)
- **Deauthentication Attacks**: Simulation von Verbindungsunterbrechungen
- **Evil Twin Access Points**: Demonstration von Rogue AP-Angriffen
- **Karma Attacks**: Analyse automatischer Verbindungsversuche
- **Sicherheitsmechanismen**: Automatische Deaktivierung außerhalb von Testumgebungen

### 📊 Berichtssystem
- **JSON-Reports**: Strukturierte, maschinenlesbare Berichte
- **PDF-Dokumentation**: Professionelle Sicherheitsberichte
- **Echtzeitanalyse**: Live-Monitoring und -Analyse
- **Visualisierung**: Netzwerktopologie und Schwachstellenheatmaps

## 🚀 Installation

### Systemanforderungen
- **Betriebssystem**: Linux (Ubuntu 20.04+ empfohlen)
- **Python**: 3.8 oder höher
- **Netzwerk**: WiFi-Adapter mit Monitor-Mode-Unterstützung
- **Berechtigungen**: Root-Zugriff für Netzwerkoperationen

### Schritt-für-Schritt Installation

1. **Repository klonen**
```bash
git clone https://github.com/your-repo/wifi-security-toolkit.git
cd wifi-security-toolkit
```

2. **Abhängigkeiten installieren**
```bash
# Automatische Installation
pip install -r requirements.txt

# Oder manuell
pip install scapy python-nmap matplotlib numpy reportlab psutil
```

3. **Systempakete installieren** (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install nmap aircrack-ng wireless-tools
```

4. **Berechtigungen setzen**
```bash
# WiFi-Adapter für Monitor-Mode vorbereiten
sudo airmon-ng start wlan0
```

## 💻 Verwendung

### Command Line Interface (CLI)

#### Grundlegende Netzwerkerkennung
```bash
# Geräte im lokalen Netzwerk entdecken
sudo python wifi_security_toolkit.py discover --range 192.168.1.0/24

# WiFi-Netzwerke scannen
sudo python wifi_security_toolkit.py scan --duration 60

# Vollständiger Scan (Geräte + WiFi)
sudo python wifi_security_toolkit.py analyze --range 192.168.1.0/24
```

#### Sicherheitsanalyse
```bash
# Umfassende Sicherheitsanalyse
sudo python wifi_security_toolkit.py analyze --range 192.168.1.0/24

# Berichte generieren
python wifi_security_toolkit.py report --pdf
```

#### Angriffssimulationen (Nur in Testumgebungen)
```bash
# Deauthentication-Simulation
sudo python wifi_security_toolkit.py attack --type deauth --target-bssid AA:BB:CC:DD:EE:FF

# Evil Twin-Simulation
sudo python wifi_security_toolkit.py attack --type eviltwin --target-ssid "TestNetwork"

# Karma-Attack-Simulation
sudo python wifi_security_toolkit.py attack --type karma
```

### Grafische Benutzeroberfläche (GUI)

```bash
# GUI starten
sudo python wifi_security_toolkit.py gui
```

Die GUI bietet folgende Features:
- **Interaktive Netzwerkkarte**: Visuelle Darstellung der Netzwerktopologie
- **Echtzeitmonitoring**: Live-Updates während der Scans
- **Schwachstellenvisualisierung**: Heatmaps und Diagramme
- **Exportfunktionen**: Direkte Berichterstellung aus der GUI

## 📁 Projektstruktur

```
wifi-security-toolkit/
├── wifi_security_toolkit.py    # Hauptmodul mit CLI
├── wifi_gui.py                 # GUI-Modul
├── requirements.txt            # Python-Abhängigkeiten
├── RESEARCH_METHODOLOGY.md     # Forschungsmethodik
├── README.md                   # Diese Datei
├── LICENSE.txt                 # Lizenzinformationen
├── examples/                   # Beispielkonfigurationen
│   ├── test_network_config.yaml
│   └── research_protocol.md
└── security_reports/           # Ausgabeverzeichnis (wird erstellt)
    ├── *.json                  # JSON-Berichte
    ├── *.pdf                   # PDF-Berichte
    └── wifi_security.log       # Logdateien
```

## 🔧 Konfiguration

### Testumgebung einrichten

Das Toolkit funktioniert nur in autorisierten Testumgebungen. Folgende Indikatoren werden geprüft:

```python
# Automatische Erkennung von Testumgebungen
TEST_NETWORK_SSIDS = ["TestLab-", "Research-", "Security-Test-"]
AUTHORIZED_ENVIRONMENTS = ["192.168.1.0/24", "10.0.0.0/8", "172.16.0.0/12"]
```

### Beispiel-Testlabor

```yaml
# examples/test_network_config.yaml
test_network:
  name: "SecurityResearchLab"
  ssid_prefix: "TestLab-"
  isolated: true
  
access_points:
  - ssid: "TestLab-WEP"
    encryption: "WEP"
    purpose: "Legacy encryption testing"
  
  - ssid: "TestLab-Open"
    encryption: "None"
    purpose: "Open network analysis"
```

## 📊 Ausgabeformate

### JSON-Berichte
```json
{
  "scan_info": {
    "timestamp": "2024-01-15T10:30:00Z",
    "devices_discovered": 12,
    "access_points_found": 3,
    "total_vulnerabilities": 8
  },
  "devices": {
    "aa:bb:cc:dd:ee:ff": {
      "ip": "192.168.1.100",
      "vendor": "Apple",
      "os_info": "iOS/macOS",
      "vulnerabilities": [...]
    }
  },
  "vulnerabilities_summary": {
    "high_risk": 2,
    "medium_risk": 4,
    "low_risk": 2
  }
}
```

### PDF-Berichte
- Executive Summary
- Detaillierte Findings
- Risikobewertung
- Empfehlungen
- Technische Details

## 🛡️ Sicherheitsfeatures

### Automatische Sicherheitsvalidierung
```python
def validate_environment():
    """Prüft automatisch auf autorisierte Testumgebung"""
    indicators = [
        check_hostname_patterns(),      # "test", "lab", "research"
        check_network_ssids(),          # TestLab-Präfixe
        check_vm_environment(),         # VirtualBox, VMware
        check_isolated_network()       # Keine Internet-Verbindung
    ]
    return any(indicators)
```

### Ethische Sicherheitsmaßnahmen
- ✅ Automatische Deaktivierung außerhalb von Testumgebungen
- ✅ Umfassendes Logging aller Aktivitäten
- ✅ Nur Simulation von Angriffen, keine echten Exploits
- ✅ Explizite Zustimmung für alle Tests erforderlich

## 🔬 Forschungsanwendungen

### iOS-spezifische Analyse
```python
# Beispiel: iOS-Geräteerkennung
def identify_ios_devices(devices):
    apple_ouis = ["00:23:12", "04:0C:CE", "08:74:02", "0C:74:C2"]
    ios_devices = []
    
    for device in devices:
        if any(device.mac.startswith(oui) for oui in apple_ouis):
            device.os_type = "iOS/macOS"
            ios_devices.append(device)
    
    return ios_devices
```

### Schwachstellenkorrelation
- Analyse von Gerät-zu-AP-Schwachstellen
- Kombinierte Risikobewerung
- Angriffsketten-Identifikation

## 📚 Dokumentation

- **[RESEARCH_METHODOLOGY.md](RESEARCH_METHODOLOGY.md)**: Detaillierte Forschungsmethodik
- **[examples/](examples/)**: Beispielkonfigurationen und Protokolle
- **Inline-Dokumentation**: Umfassende Code-Kommentare

## 🤝 Beitragen

Wir freuen uns über Beiträge zur Verbesserung des Toolkits:

1. Fork das Repository
2. Erstelle einen Feature-Branch (`git checkout -b feature/AmazingFeature`)
3. Committe deine Änderungen (`git commit -m 'Add some AmazingFeature'`)
4. Push zum Branch (`git push origin feature/AmazingFeature`)
5. Öffne einen Pull Request

### Entwicklungsrichtlinien
- **PEP-8 konform**: Code-Style nach Python-Standards
- **Dokumentation**: Alle neuen Features dokumentieren
- **Tests**: Unit-Tests für neue Funktionen
- **Sicherheit**: Ethische Richtlinien beachten

## 📄 Lizenz

Dieses Projekt steht unter einer Educational Use License. Siehe [LICENSE.txt](LICENSE.txt) für Details.

**Wichtige Einschränkungen:**
- Nur für Bildungs- und Forschungszwecke
- Keine kommerzielle Nutzung ohne explizite Genehmigung
- Nur in autorisierten Testumgebungen verwenden

## ⚖️ Rechtliche Hinweise

### Haftungsausschluss
Die Entwickler übernehmen keine Verantwortung für den Missbrauch dieses Tools. Nutzer sind verpflichtet:

- Nur in autorisierten Umgebungen zu testen
- Alle geltenden Gesetze zu beachten
- Keine Schäden an fremden Systemen zu verursachen
- Ethische Forschungsstandards einzuhalten

### Compliance
- **DSGVO-konform**: Keine Sammlung persönlicher Daten
- **Forschungsethik**: Nach wissenschaftlichen Standards
- **Responsible Disclosure**: Schwachstellen werden verantwortlich gemeldet

## 🆘 Support und Hilfe

### Häufige Probleme

**Problem**: "Permission denied" bei Netzwerkoperationen
```bash
# Lösung: Root-Rechte verwenden
sudo python wifi_security_toolkit.py scan
```

**Problem**: "Interface not found"
```bash
# Lösung: WiFi-Interface prüfen
iwconfig
# Interface für Monitor-Mode aktivieren
sudo airmon-ng start wlan0
```

**Problem**: GUI startet nicht
```bash
# Lösung: Abhängigkeiten prüfen
pip install matplotlib tkinter
```

### Community und Support
- **Issues**: GitHub Issues für Bug Reports
- **Diskussionen**: GitHub Discussions für Fragen
- **Wiki**: Detaillierte Anleitungen und FAQs

## 🔮 Roadmap

### Version 2.0 (Geplant)
- [ ] **Erweiterte iOS-Analyse**: Tiefere Analyse von iOS-spezifischen Schwachstellen
- [ ] **Machine Learning**: Automatische Anomalieerkennung
- [ ] **API-Integration**: RESTful API für externe Tools
- [ ] **Mobile App**: Begleit-App für Feldforschung

### Version 1.5 (In Entwicklung)
- [ ] **Bluetooth-Analyse**: Erweiterung auf Bluetooth-Sicherheit
- [ ] **Erweiterte Visualisierung**: 3D-Netzwerkkarten
- [ ] **Plugin-System**: Erweiterbare Architektur
- [ ] **Cloud-Integration**: Sichere Cloud-basierte Analysen

## 📞 Kontakt

- **Hauptentwickler**: Security Research Team
- **E-Mail**: security-research@example.com
- **GitHub**: [https://github.com/your-repo/wifi-security-toolkit](https://github.com/your-repo/wifi-security-toolkit)

---

**Entwickelt mit ❤️ für die Cybersecurity-Community**

*"Security through education, not exploitation"*
