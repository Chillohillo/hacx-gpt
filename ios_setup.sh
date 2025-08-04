#!/usr/bin/env bash
set -e

# Kickbase Ultimate Analyzer - iOS Setup Script
# ==============================================
# Automatisierte Installation und Einrichtung für iOS-Version
# Unterstützt macOS, Linux und Cloud-Deployment

# Farben für Output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
NC='\033[0m' # No Color

# Emoji für bessere UX
ROCKET="🚀"
CHECK="✅"
CROSS="❌"
WARNING="⚠️"
INFO="ℹ️"
PHONE="📱"
CLOUD="☁️"

# Logging Funktionen
log_info() {
    echo -e "${BLUE}${INFO} $1${NC}"
}

log_success() {
    echo -e "${GREEN}${CHECK} $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}${WARNING} $1${NC}"
}

log_error() {
    echo -e "${RED}${CROSS} $1${NC}"
}

log_header() {
    echo -e "\n${PURPLE}${ROCKET} $1${NC}\n"
}

# Banner anzeigen
show_banner() {
    echo -e "${CYAN}"
    cat << "EOF"
    ██╗ ██████╗ ███████╗    ██╗  ██╗██╗ ██████╗██╗  ██╗██████╗  █████╗ ███████╗███████╗
    ██║██╔═══██╗██╔════╝    ██║ ██╔╝██║██╔════╝██║ ██╔╝██╔══██╗██╔══██╗██╔════╝██╔════╝
    ██║██║   ██║███████╗    █████╔╝ ██║██║     █████╔╝ ██████╔╝███████║███████╗█████╗  
    ██║██║   ██║╚════██║    ██╔═██╗ ██║██║     ██╔═██╗ ██╔══██╗██╔══██║╚════██║██╔══╝  
    ██║╚██████╔╝███████║    ██║  ██╗██║╚██████╗██║  ██╗██████╔╝██║  ██║███████║███████╗
    ╚═╝ ╚═════╝ ╚══════╝    ╚═╝  ╚═╝╚═╝ ╚═════╝╚═╝  ╚═╝╚═════╝ ╚═╝  ╚═╝╚══════╝╚══════╝
                                                                                        
                            Ultimate Analyzer - iOS Edition v2.0.0
EOF
    echo -e "${NC}"
    echo -e "${WHITE}📱 Mobile-optimierte Kickbase-Analysen für iOS Geräte${NC}"
    echo -e "${WHITE}🚀 Progressive Web App + Native iOS Shortcuts Integration${NC}\n"
}

# System erkennen
detect_system() {
    if [[ "$OSTYPE" == "darwin"* ]]; then
        OS="macOS"
        PACKAGE_MANAGER="brew"
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        if command -v apt-get >/dev/null 2>&1; then
            OS="Ubuntu/Debian"
            PACKAGE_MANAGER="apt"
        elif command -v yum >/dev/null 2>&1; then
            OS="CentOS/RHEL"
            PACKAGE_MANAGER="yum"
        else
            OS="Linux"
            PACKAGE_MANAGER="unknown"
        fi
    else
        OS="Unknown"
        PACKAGE_MANAGER="unknown"
    fi
    
    log_info "Erkanntes System: $OS"
}

# Sudo-Rechte prüfen
check_sudo() {
    if [[ $EUID -eq 0 ]]; then
        log_warning "Läuft als Root - das ist nicht empfohlen"
        SUDO=""
    else
        if sudo -n true 2>/dev/null; then
            log_success "Sudo-Rechte verfügbar"
            SUDO="sudo"
        else
            log_error "Sudo-Rechte erforderlich"
            exit 1
        fi
    fi
}

# System aktualisieren
update_system() {
    log_header "System wird aktualisiert..."
    
    case $PACKAGE_MANAGER in
        "brew")
            brew update && brew upgrade
            ;;
        "apt")
            $SUDO apt-get update && $SUDO apt-get upgrade -y
            ;;
        "yum")
            $SUDO yum update -y
            ;;
        *)
            log_warning "Unbekannter Package Manager - Update übersprungen"
            ;;
    esac
    
    log_success "System aktualisiert"
}

# Python installieren
install_python() {
    log_header "Python 3.11+ wird installiert..."
    
    if command -v python3.11 >/dev/null 2>&1; then
        log_success "Python 3.11+ bereits installiert"
        return
    fi
    
    case $PACKAGE_MANAGER in
        "brew")
            brew install python@3.11
            ;;
        "apt")
            $SUDO apt-get install -y python3.11 python3.11-pip python3.11-venv python3.11-dev
            ;;
        "yum")
            $SUDO yum install -y python311 python311-pip python311-devel
            ;;
        *)
            log_error "Bitte installieren Sie Python 3.11+ manuell"
            exit 1
            ;;
    esac
    
    log_success "Python installiert"
}

# System-Dependencies installieren
install_system_dependencies() {
    log_header "System-Dependencies werden installiert..."
    
    case $PACKAGE_MANAGER in
        "brew")
            brew install curl wget git nodejs npm redis postgresql docker docker-compose
            ;;
        "apt")
            $SUDO apt-get install -y \
                curl wget git \
                nodejs npm \
                build-essential \
                libssl-dev libffi-dev \
                libxml2-dev libxslt1-dev \
                libjpeg-dev libpng-dev zlib1g-dev \
                sqlite3 libsqlite3-dev \
                redis-server \
                postgresql postgresql-contrib \
                docker.io docker-compose
            ;;
        "yum")
            $SUDO yum install -y \
                curl wget git \
                nodejs npm \
                gcc gcc-c++ make \
                openssl-devel libffi-devel \
                libxml2-devel libxslt-devel \
                libjpeg-devel libpng-devel zlib-devel \
                sqlite-devel \
                redis \
                postgresql postgresql-server \
                docker docker-compose
            ;;
    esac
    
    log_success "System-Dependencies installiert"
}

# iOS-spezifische Tools installieren
install_ios_tools() {
    log_header "iOS-spezifische Tools werden installiert..."
    
    if [[ "$OS" == "macOS" ]]; then
        # Xcode Command Line Tools
        if ! xcode-select -p >/dev/null 2>&1; then
            log_info "Xcode Command Line Tools werden installiert..."
            xcode-select --install
        fi
        
        # iOS Simulator (optional)
        if command -v brew >/dev/null 2>&1; then
            brew install --cask ios-app-installer
        fi
        
        log_success "iOS-Tools installiert"
    else
        log_warning "iOS-spezifische Tools nur auf macOS verfügbar"
    fi
}

# Python Virtual Environment erstellen
create_venv() {
    log_header "Python Virtual Environment wird erstellt..."
    
    if [[ -d "venv" ]]; then
        log_info "Virtual Environment bereits vorhanden"
        return
    fi
    
    python3.11 -m venv venv
    source venv/bin/activate
    
    # Pip upgraden
    pip install --upgrade pip setuptools wheel
    
    log_success "Virtual Environment erstellt"
}

# Python Dependencies installieren
install_python_dependencies() {
    log_header "Python Dependencies werden installiert..."
    
    source venv/bin/activate
    
    # iOS-spezifische Requirements
    pip install -r ios_requirements.txt
    
    # Zusätzliche iOS-Tools
    if [[ "$OS" == "macOS" ]]; then
        pip install pyobjc pyobjc-framework-UIKit pyobjc-framework-UserNotifications
    fi
    
    log_success "Python Dependencies installiert"
}

# Konfiguration einrichten
setup_configuration() {
    log_header "Konfiguration wird eingerichtet..."
    
    # Verzeichnisse erstellen
    mkdir -p {data/ios,data/pwa,data/celery,logs/ios,logs/pwa,logs/celery,logs/push,certs,ssl,static,config,sql}
    
    # .env Datei erstellen falls nicht vorhanden
    if [[ ! -f ".env" ]]; then
        log_info "Erstelle .env Datei..."
        cat > .env << EOF
# iOS Kickbase Ultimate Analyzer - Environment Configuration
# ==========================================================

# Kickbase Login Credentials
KICKBASE_EMAIL=ihre@email.com
KICKBASE_PASSWORD=ihr_passwort
KICKBASE_LEAGUE_ID=ihre_liga_id

# JWT Secret (ÄNDERN SIE DIES!)
JWT_SECRET=$(openssl rand -base64 32)

# Database
POSTGRES_PASSWORD=$(openssl rand -base64 16)

# AI API Keys
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...

# iOS Push Notifications (Apple Developer Account erforderlich)
APNS_KEY_ID=your_apns_key_id
APNS_TEAM_ID=your_team_id

# Grafana
GRAFANA_PASSWORD=$(openssl rand -base64 12)

# Redis (optional)
REDIS_URL=redis://localhost:6379

# Log Level
LOG_LEVEL=INFO
EOF
        log_success ".env Datei erstellt - Bitte konfigurieren Sie Ihre Werte"
    fi
    
    # iOS-spezifische Konfigurationsdateien
    create_ios_config_files
    
    log_success "Konfiguration eingerichtet"
}

# iOS-spezifische Konfigurationsdateien erstellen
create_ios_config_files() {
    # Nginx Konfiguration für PWA
    cat > config/nginx.conf << 'EOF'
events {
    worker_connections 1024;
}

http {
    upstream backend {
        server kickbase-ios-backend:8000;
    }
    
    upstream pwa {
        server kickbase-ios-pwa:8501;
    }
    
    server {
        listen 80;
        server_name _;
        
        # PWA Service Worker
        location /sw.js {
            proxy_pass http://pwa;
            add_header Cache-Control "no-cache";
        }
        
        # PWA Manifest
        location /manifest.json {
            proxy_pass http://pwa;
            add_header Content-Type application/json;
        }
        
        # API Routes
        location /api/ {
            proxy_pass http://backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }
        
        # PWA Routes
        location / {
            proxy_pass http://pwa;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            
            # PWA Headers
            add_header X-Frame-Options DENY;
            add_header X-Content-Type-Options nosniff;
        }
        
        # Health Check
        location /health {
            return 200 "OK";
            add_header Content-Type text/plain;
        }
    }
}
EOF

    # Redis Konfiguration
    cat > config/redis.conf << 'EOF'
# Redis iOS Configuration
bind 0.0.0.0
port 6379
timeout 0
save 900 1
save 300 10
save 60 10000
maxmemory 256mb
maxmemory-policy allkeys-lru
EOF

    # Prometheus Konfiguration
    cat > config/prometheus.yml << 'EOF'
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'kickbase-ios-backend'
    static_configs:
      - targets: ['kickbase-ios-backend:8000']
  
  - job_name: 'kickbase-ios-pwa'
    static_configs:
      - targets: ['kickbase-ios-pwa:8501']
EOF

    log_info "iOS-Konfigurationsdateien erstellt"
}

# Docker Setup
setup_docker() {
    log_header "Docker wird eingerichtet..."
    
    # Docker Service starten
    case $OS in
        "macOS")
            if ! docker info >/dev/null 2>&1; then
                log_info "Bitte starten Sie Docker Desktop"
                open /Applications/Docker.app
                sleep 10
            fi
            ;;
        "Ubuntu/Debian"|"CentOS/RHEL")
            $SUDO systemctl start docker
            $SUDO systemctl enable docker
            $SUDO usermod -aG docker $USER
            ;;
    esac
    
    # Dockerfiles erstellen
    create_dockerfiles
    
    log_success "Docker eingerichtet"
}

# Dockerfiles erstellen
create_dockerfiles() {
    # iOS Backend Dockerfile
    cat > Dockerfile.ios << 'EOF'
FROM python:3.11-slim

LABEL maintainer="Kickbase iOS Ultimate" \
      version="2.0.0" \
      description="iOS Backend für Kickbase Ultimate Analyzer"

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    build-essential gcc g++ \
    libssl-dev libffi-dev \
    libxml2-dev libxslt1-dev \
    libjpeg-dev libpng-dev zlib1g-dev \
    sqlite3 libsqlite3-dev \
    postgresql-client \
    curl wget \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY ios_requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r ios_requirements.txt

COPY . .

RUN mkdir -p data logs certs && \
    chmod +x *.py

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8000/ || exit 1

CMD ["python", "ios_cloud_backend.py"]
EOF

    # PWA Dockerfile
    cat > Dockerfile.pwa << 'EOF'
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    STREAMLIT_SERVER_PORT=8501 \
    STREAMLIT_SERVER_ADDRESS=0.0.0.0

RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY ios_requirements.txt .
RUN pip install --no-cache-dir -r ios_requirements.txt

COPY . .

EXPOSE 8501

HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

CMD ["streamlit", "run", "ios_kickbase_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
EOF

    log_info "Dockerfiles erstellt"
}

# iOS Shortcuts installieren
install_ios_shortcuts() {
    log_header "iOS Shortcuts werden vorbereitet..."
    
    if [[ "$OS" == "macOS" ]]; then
        # QR-Code für Shortcuts generieren
        if command -v python3 >/dev/null 2>&1; then
            python3 << 'EOF'
import qrcode
import json

# Shortcuts URL generieren
shortcuts_url = "https://www.icloud.com/shortcuts/your-shortcut-id"

# QR-Code erstellen
qr = qrcode.QRCode(version=1, box_size=10, border=5)
qr.add_data(shortcuts_url)
qr.make(fit=True)

img = qr.make_image(fill_color="black", back_color="white")
img.save("static/ios_shortcuts_qr.png")
print("✅ QR-Code für iOS Shortcuts erstellt: static/ios_shortcuts_qr.png")
EOF
        fi
        
        log_success "iOS Shortcuts vorbereitet"
        log_info "Scannen Sie den QR-Code in static/ios_shortcuts_qr.png mit Ihrem iPhone"
    else
        log_warning "iOS Shortcuts Setup nur auf macOS verfügbar"
    fi
}

# Services testen
test_installation() {
    log_header "Installation wird getestet..."
    
    # Python Import Test
    if source venv/bin/activate && python -c "import streamlit, fastapi, redis, pandas, numpy, plotly; print('✅ Alle Python-Module verfügbar')"; then
        log_success "Python-Module Test bestanden"
    else
        log_error "Python-Module Test fehlgeschlagen"
        return 1
    fi
    
    # Docker Test
    if docker --version >/dev/null 2>&1; then
        log_success "Docker verfügbar"
    else
        log_warning "Docker nicht verfügbar - nur lokale Installation möglich"
    fi
    
    log_success "Installation erfolgreich getestet"
}

# Services starten
start_services() {
    log_header "Services werden gestartet..."
    
    case $1 in
        "local")
            start_local_services
            ;;
        "docker")
            start_docker_services
            ;;
        *)
            log_info "Verfügbare Modi: local, docker"
            ;;
    esac
}

# Lokale Services starten
start_local_services() {
    log_info "Starte lokale Services..."
    
    source venv/bin/activate
    
    # Backend im Hintergrund starten
    nohup python ios_cloud_backend.py > logs/ios/backend.log 2>&1 &
    echo $! > .backend.pid
    
    # PWA starten
    log_info "PWA wird gestartet..."
    log_info "Öffnen Sie http://localhost:8501 in Ihrem Browser"
    
    streamlit run ios_kickbase_app.py --server.port=8501 --server.address=0.0.0.0
}

# Docker Services starten
start_docker_services() {
    log_info "Starte Docker Services..."
    
    if [[ ! -f "ios_deployment.yml" ]]; then
        log_error "ios_deployment.yml nicht gefunden"
        return 1
    fi
    
    docker-compose -f ios_deployment.yml up -d
    
    log_success "Docker Services gestartet"
    log_info "PWA: http://localhost:8501"
    log_info "API: http://localhost:8000"
    log_info "Grafana: http://localhost:3000"
}

# Services stoppen
stop_services() {
    log_header "Services werden gestoppt..."
    
    # Lokale Services stoppen
    if [[ -f ".backend.pid" ]]; then
        kill $(cat .backend.pid) 2>/dev/null || true
        rm .backend.pid
    fi
    
    # Docker Services stoppen
    if [[ -f "ios_deployment.yml" ]]; then
        docker-compose -f ios_deployment.yml down
    fi
    
    log_success "Services gestoppt"
}

# Logs anzeigen
show_logs() {
    log_header "Logs werden angezeigt..."
    
    case $1 in
        "backend")
            tail -f logs/ios/backend.log
            ;;
        "docker")
            docker-compose -f ios_deployment.yml logs -f
            ;;
        *)
            log_info "Verfügbare Log-Typen: backend, docker"
            ;;
    esac
}

# Status anzeigen
show_status() {
    log_header "System Status"
    
    # Python Status
    if source venv/bin/activate 2>/dev/null; then
        log_success "Python Virtual Environment: Aktiv"
    else
        log_warning "Python Virtual Environment: Nicht aktiv"
    fi
    
    # Docker Status
    if docker info >/dev/null 2>&1; then
        log_success "Docker: Verfügbar"
        
        # Container Status
        if docker-compose -f ios_deployment.yml ps 2>/dev/null; then
            log_info "Docker Container Status angezeigt"
        fi
    else
        log_warning "Docker: Nicht verfügbar"
    fi
    
    # Service Status
    if curl -s http://localhost:8501 >/dev/null; then
        log_success "PWA: Läuft (http://localhost:8501)"
    else
        log_warning "PWA: Nicht erreichbar"
    fi
    
    if curl -s http://localhost:8000 >/dev/null; then
        log_success "API: Läuft (http://localhost:8000)"
    else
        log_warning "API: Nicht erreichbar"
    fi
}

# Hilfe anzeigen
show_help() {
    echo -e "${WHITE}Kickbase iOS Ultimate Analyzer - Setup Script${NC}\n"
    echo -e "${CYAN}VERWENDUNG:${NC}"
    echo -e "  ./ios_setup.sh [BEFEHL] [OPTIONEN]\n"
    echo -e "${CYAN}BEFEHLE:${NC}"
    echo -e "  ${GREEN}install${NC}        Vollständige Installation"
    echo -e "  ${GREEN}start local${NC}    Services lokal starten"
    echo -e "  ${GREEN}start docker${NC}   Services mit Docker starten"
    echo -e "  ${GREEN}stop${NC}           Services stoppen"
    echo -e "  ${GREEN}status${NC}         System-Status anzeigen"
    echo -e "  ${GREEN}logs [TYPE]${NC}    Logs anzeigen (backend|docker)"
    echo -e "  ${GREEN}update${NC}         System aktualisieren"
    echo -e "  ${GREEN}help${NC}           Diese Hilfe anzeigen\n"
    echo -e "${CYAN}BEISPIELE:${NC}"
    echo -e "  ./ios_setup.sh install"
    echo -e "  ./ios_setup.sh start local"
    echo -e "  ./ios_setup.sh start docker"
    echo -e "  ./ios_setup.sh logs backend\n"
    echo -e "${CYAN}WEITERE INFORMATIONEN:${NC}"
    echo -e "  📱 PWA: http://localhost:8501"
    echo -e "  🔧 API: http://localhost:8000"
    echo -e "  📊 Grafana: http://localhost:3000"
    echo -e "  📋 Logs: ./logs/"
}

# Hauptfunktion
main() {
    show_banner
    
    case "${1:-install}" in
        "install")
            detect_system
            check_sudo
            update_system
            install_python
            install_system_dependencies
            install_ios_tools
            create_venv
            install_python_dependencies
            setup_configuration
            setup_docker
            install_ios_shortcuts
            test_installation
            
            log_success "Installation abgeschlossen!"
            log_info "Starten Sie die Services mit: ./ios_setup.sh start local"
            ;;
        "start")
            start_services $2
            ;;
        "stop")
            stop_services
            ;;
        "status")
            show_status
            ;;
        "logs")
            show_logs $2
            ;;
        "update")
            update_system
            ;;
        "help"|"--help"|"-h")
            show_help
            ;;
        *)
            log_error "Unbekannter Befehl: $1"
            show_help
            exit 1
            ;;
    esac
}

# Error Handler
trap 'log_error "Fehler in Zeile $LINENO. Exit Code: $?"' ERR

# Script ausführen
main "$@"