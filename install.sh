#!/bin/bash

# Kickbase Ultimate Analyzer - Installation Script
# Unterstützt Ubuntu, Debian, Kali Linux und andere Debian-basierte Systeme

set -e

echo "🚀 Kickbase Ultimate Analyzer - Installation"
echo "============================================="

# Farben für Output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Funktionen
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# System-Erkennung
detect_system() {
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        OS=$NAME
        VER=$VERSION_ID
    else
        log_error "Betriebssystem konnte nicht erkannt werden"
        exit 1
    fi
    
    log_info "Erkanntes System: $OS $VER"
}

# Prüfe ob Root-Rechte benötigt werden
check_sudo() {
    if [[ $EUID -eq 0 ]]; then
        SUDO=""
    else
        SUDO="sudo"
    fi
}

# System-Updates
update_system() {
    log_info "Aktualisiere System-Pakete..."
    $SUDO apt update
    $SUDO apt upgrade -y
    log_success "System aktualisiert"
}

# Python Installation
install_python() {
    log_info "Installiere Python 3 und pip..."
    
    $SUDO apt install -y \
        python3 \
        python3-pip \
        python3-dev \
        python3-venv \
        python3-wheel \
        python3-setuptools
    
    # Upgrade pip
    python3 -m pip install --upgrade pip
    
    log_success "Python 3 installiert"
}

# System-Abhängigkeiten
install_system_dependencies() {
    log_info "Installiere System-Abhängigkeiten..."
    
    $SUDO apt install -y \
        curl \
        wget \
        git \
        build-essential \
        libssl-dev \
        libffi-dev \
        libxml2-dev \
        libxslt1-dev \
        libjpeg-dev \
        libpng-dev \
        zlib1g-dev \
        sqlite3 \
        libsqlite3-dev \
        chromium-browser \
        chromium-chromedriver \
        tor \
        proxychains4
    
    log_success "System-Abhängigkeiten installiert"
}

# Kali Linux spezifische Tools
install_kali_tools() {
    if [[ "$OS" == *"Kali"* ]]; then
        log_info "Installiere Kali Linux spezifische Tools..."
        
        $SUDO apt install -y \
            nmap \
            nikto \
            sqlmap \
            metasploit-framework \
            burpsuite \
            wireshark \
            john \
            hashcat
        
        log_success "Kali Tools installiert"
    fi
}

# Python Virtual Environment
create_venv() {
    log_info "Erstelle Python Virtual Environment..."
    
    if [ -d "venv" ]; then
        log_warning "Virtual Environment existiert bereits"
        read -p "Soll es neu erstellt werden? (y/n): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            rm -rf venv
        else
            return 0
        fi
    fi
    
    python3 -m venv venv
    source venv/bin/activate
    
    log_success "Virtual Environment erstellt"
}

# Python Abhängigkeiten
install_python_dependencies() {
    log_info "Installiere Python-Abhängigkeiten..."
    
    # Aktiviere Virtual Environment
    source venv/bin/activate
    
    # Upgrade pip im venv
    pip install --upgrade pip
    
    # Installiere Wheel für bessere Kompatibilität
    pip install wheel
    
    # Installiere Requirements
    if [ -f "requirements.txt" ]; then
        pip install -r requirements.txt
    else
        log_error "requirements.txt nicht gefunden!"
        exit 1
    fi
    
    log_success "Python-Abhängigkeiten installiert"
}

# Konfiguration erstellen
setup_configuration() {
    log_info "Erstelle Konfigurationsdateien..."
    
    # .env Datei
    if [ ! -f ".env" ]; then
        if [ -f ".env.template" ]; then
            cp .env.template .env
            log_info "Bitte bearbeite die .env Datei mit deinen Credentials"
        else
            log_warning ".env.template nicht gefunden"
        fi
    fi
    
    # Verzeichnisse erstellen
    mkdir -p kickbase_data exports logs cache temp
    
    log_success "Konfiguration erstellt"
}

# Chrome/Chromium für Selenium
setup_chrome() {
    log_info "Konfiguriere Chrome/Chromium für Selenium..."
    
    # Prüfe ob Chrome verfügbar ist
    if command -v google-chrome &> /dev/null; then
        CHROME_PATH=$(which google-chrome)
    elif command -v chromium-browser &> /dev/null; then
        CHROME_PATH=$(which chromium-browser)
    elif command -v chromium &> /dev/null; then
        CHROME_PATH=$(which chromium)
    else
        log_warning "Chrome/Chromium nicht gefunden"
        return 1
    fi
    
    log_success "Chrome/Chromium konfiguriert: $CHROME_PATH"
}

# Tor Konfiguration (für Kali Linux)
setup_tor() {
    if [[ "$OS" == *"Kali"* ]]; then
        log_info "Konfiguriere Tor für anonyme Requests..."
        
        # Tor Service starten
        $SUDO systemctl enable tor
        $SUDO systemctl start tor
        
        # Proxychains konfigurieren
        if [ -f "/etc/proxychains4.conf" ]; then
            $SUDO cp /etc/proxychains4.conf /etc/proxychains4.conf.backup
            echo "socks5 127.0.0.1 9050" | $SUDO tee -a /etc/proxychains4.conf > /dev/null
        fi
        
        log_success "Tor konfiguriert"
    fi
}

# Berechtigungen setzen
set_permissions() {
    log_info "Setze Dateiberechtigungen..."
    
    chmod +x kickbase_ultimate_analyzer.py
    chmod +x install.sh
    
    # Logs Verzeichnis
    chmod 755 logs
    
    log_success "Berechtigungen gesetzt"
}

# Service erstellen (Optional)
create_service() {
    read -p "Soll ein systemd Service erstellt werden? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        log_info "Erstelle systemd Service..."
        
        SERVICE_FILE="/etc/systemd/system/kickbase-analyzer.service"
        WORK_DIR=$(pwd)
        
        $SUDO tee $SERVICE_FILE > /dev/null <<EOF
[Unit]
Description=Kickbase Ultimate Analyzer
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$WORK_DIR
Environment=PATH=$WORK_DIR/venv/bin
ExecStart=$WORK_DIR/venv/bin/python $WORK_DIR/kickbase_ultimate_analyzer.py --mode scheduler
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF
        
        $SUDO systemctl daemon-reload
        $SUDO systemctl enable kickbase-analyzer.service
        
        log_success "Service erstellt: kickbase-analyzer.service"
        log_info "Starten: sudo systemctl start kickbase-analyzer"
        log_info "Status: sudo systemctl status kickbase-analyzer"
    fi
}

# Test Installation
test_installation() {
    log_info "Teste Installation..."
    
    source venv/bin/activate
    
    # Test Python Import
    if python3 -c "import pandas, numpy, sklearn, xgboost, lightgbm, requests, beautifulsoup4" 2>/dev/null; then
        log_success "Python-Pakete erfolgreich importiert"
    else
        log_error "Fehler beim Import von Python-Paketen"
        return 1
    fi
    
    # Test Hauptskript
    if python3 kickbase_ultimate_analyzer.py --help > /dev/null 2>&1; then
        log_success "Hauptskript funktioniert"
    else
        log_error "Fehler beim Ausführen des Hauptskripts"
        return 1
    fi
    
    log_success "Installation erfolgreich getestet!"
}

# Hauptinstallation
main() {
    echo "Starte Installation..."
    
    detect_system
    check_sudo
    
    # Installation Steps
    update_system
    install_python
    install_system_dependencies
    install_kali_tools
    create_venv
    install_python_dependencies
    setup_configuration
    setup_chrome
    setup_tor
    set_permissions
    create_service
    test_installation
    
    echo
    log_success "🎉 Installation abgeschlossen!"
    echo
    echo "Nächste Schritte:"
    echo "1. Bearbeite die .env Datei mit deinen Kickbase-Credentials"
    echo "2. Aktiviere das Virtual Environment: source venv/bin/activate"
    echo "3. Starte das Tool: python3 kickbase_ultimate_analyzer.py --mode quick"
    echo
    echo "Für Hilfe: python3 kickbase_ultimate_analyzer.py --help"
    echo
}

# Fehlerbehandlung
trap 'log_error "Installation fehlgeschlagen!"; exit 1' ERR

# Hauptfunktion ausführen
main "$@"
