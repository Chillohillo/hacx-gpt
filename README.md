# 🚀 Kickbase Ultimate Analyzer

Ein umfangreiches Python-Tool für die Analyse von Kickbase Fantasy Football mit Machine Learning, AI-Integration und Cloud-Support.

## ✨ Features

### 🔄 API-Integration
- **Mehrere Kickbase API Wrapper** - Unterstützung für offizielle und inoffizielle APIs
- **Automatisches Fallback** - Wechselt zwischen verschiedenen API-Implementierungen
- **Rate Limiting** - Schützt vor API-Limits und Account-Sperren
- **Umfassende Datensammlung** - Spieler, Marktwerte, Statistiken, Verletzungen

### 🤖 Machine Learning
- **Mehrere ML-Modelle** - Random Forest, XGBoost, LightGBM, Gradient Boosting
- **Automatische Modell-Auswahl** - Wählt das beste Modell basierend auf Performance
- **Feature Engineering** - Erweiterte Features aus Rohdaten
- **Vorhersagen** - Spielerwert-Trends und Marktbewegungen
- **Cross-Validation** - Robuste Modell-Evaluation

### 🧠 AI-Integration
- **ChatGPT Integration** - Intelligente Analyse mit GPT-4
- **Claude Integration** - Alternative AI-Analyse mit Anthropic
- **Grok Support** - Vorbereitet für X.AI's Grok
- **Fallback-Analyse** - Funktioniert auch ohne AI-APIs
- **Mehrsprachig** - Deutsche Analysen und Empfehlungen

### ☁️ Cloud-Integration
- **Google Cloud Storage** - Automatischer Upload zu GCS
- **AWS S3** - S3 Bucket Integration
- **GitHub Integration** - Upload zu GitHub Repositories
- **Öffentliche URLs** - Teile Analysen über Cloud-Links

### 📊 Export-Funktionen
- **JSON Export** - Strukturierte Daten für APIs
- **CSV Export** - Für Excel und Datenanalyse
- **Excel Export** - Mehrere Sheets mit verschiedenen Daten
- **HTML Reports** - Schöne, interaktive Berichte
- **Markdown Export** - Für GitHub und Dokumentation

### 🔒 Kali Linux Support
- **Tor Integration** - Anonyme Requests über Tor
- **Proxychains** - Proxy-Unterstützung
- **Verschlüsselung** - Sichere Datenspeicherung
- **Security Tools** - Integration mit Kali-Tools

### ⚡ Automatisierung
- **Scheduler** - Automatische tägliche/stündliche Analysen
- **Cron Jobs** - Linux Cron Integration
- **Systemd Service** - Als System-Service ausführbar
- **Notifications** - Discord, Telegram, Email Benachrichtigungen

## 🛠️ Installation

### Schnellinstallation (Linux/Kali)

```bash
git clone https://github.com/yourusername/kickbase-ultimate-analyzer.git
cd kickbase-ultimate-analyzer
chmod +x install.sh
./install.sh
```

### Manuelle Installation

#### 1. Abhängigkeiten installieren

```bash
# Ubuntu/Debian/Kali Linux
sudo apt update
sudo apt install python3 python3-pip python3-venv git

# Python Virtual Environment
python3 -m venv venv
source venv/bin/activate

# Python Pakete
pip install -r requirements.txt
```

#### 2. Konfiguration

```bash
# Kopiere Template
cp .env.template .env

# Bearbeite mit deinen Daten
nano .env
```

#### 3. Verzeichnisse erstellen

```bash
mkdir -p kickbase_data exports logs cache temp
```

## ⚙️ Konfiguration

### Umgebungsvariablen (.env)

```env
# Kickbase Login
KICKBASE_EMAIL=deine@email.com
KICKBASE_PASSWORD=dein_passwort
KICKBASE_LEAGUE_ID=deine_liga_id

# AI APIs (Optional)
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...

# Cloud Storage (Optional)
GOOGLE_CREDENTIALS_PATH=path/to/service-account.json
AWS_ACCESS_KEY_ID=AKIA...
AWS_SECRET_ACCESS_KEY=...
```

### YAML Konfiguration (config.yaml)

Detaillierte Einstellungen für ML-Parameter, Scheduling, Features etc.

## 🚀 Verwendung

### Kommandozeile

```bash
# Aktiviere Virtual Environment
source venv/bin/activate

# Quick Analyse
python3 kickbase_ultimate_analyzer.py --mode quick

# Vollständige Analyse
python3 kickbase_ultimate_analyzer.py --mode full

# Scheduler starten
python3 kickbase_ultimate_analyzer.py --mode scheduler

# Mit eigener Konfiguration
python3 kickbase_ultimate_analyzer.py --config my_config.yaml --output-dir /path/to/output
```

### Python API

```python
from kickbase_ultimate_analyzer import KickbaseUltimateAnalyzer

# Analyzer erstellen
analyzer = KickbaseUltimateAnalyzer()

# Schnelle Analyse
results = analyzer.run_quick_analysis()

# Vollständige Analyse (async)
import asyncio
results = asyncio.run(analyzer.run_full_analysis())

# Ergebnisse verwenden
print(f"Top Spieler: {results['analysis_data']['top_players'][:5]}")
print(f"AI Analyse: {results['ai_analysis']}")
```

## 📈 Ausgabe-Beispiele

### Top Spieler Empfehlungen

```
🚀 Top Kauf-Empfehlungen:
1. Erling Haaland - Erwartete Steigerung: +2.5M€ (+15.2%)
2. Jamal Musiala - Erwartete Steigerung: +1.8M€ (+12.4%)
3. Florian Wirtz - Erwartete Steigerung: +1.2M€ (+8.9%)
```

### AI-Analyse Beispiel

```
🤖 Basierend auf den aktuellen Daten empfehle ich folgende Transfers:

SOFORTIGE KÄUFE:
- Erling Haaland: Starke Form, günstige Fixtures
- Jamal Musiala: Unterschätzt, hohes Potenzial

VERKÄUFE:
- Manuel Neuer: Überteuert für aktuelle Leistung
- Thomas Müller: Altersschwäche erkennbar

MARKT-TRENDS:
- Stürmer sind aktuell überbewertet
- Mittelfeld bietet beste Value-Picks
```

### Export-Dateien

```
exports/
├── kickbase_analysis_20240115_143022.json    # JSON Daten
├── kickbase_predictions_20240115_143022.csv  # CSV Predictions
├── kickbase_complete_20240115_143022.xlsx    # Excel Report
├── kickbase_report_20240115_143022.html      # HTML Report
└── kickbase_report_20240115_143022.md        # Markdown Report
```

## 🔧 Erweiterte Features

### Machine Learning Modelle

Das Tool trainiert automatisch mehrere ML-Modelle und wählt das beste aus:

- **Random Forest** - Robust, interpretierbar
- **XGBoost** - Hohe Genauigkeit, Feature Importance
- **LightGBM** - Schnell, effizient
- **Gradient Boosting** - Klassischer Ensemble-Ansatz

### Feature Engineering

Automatische Erstellung von über 20 Features:

- Marktwert-Trends (5/10/30 Tage)
- Performance-Ratios (Punkte pro Million)
- Positions-Encodings
- Team-basierte Features
- Saisonale Trends
- Verletzungshistorie

### Cloud-Integration

#### Google Cloud Storage

```python
# Automatischer Upload
cloud_urls = await cloud_integration.upload_files(export_files, "mein-bucket")
print(f"GCS URL: {cloud_urls['gcs_json']}")
```

#### AWS S3

```python
# S3 Configuration
config.aws_access_key = "AKIA..."
config.aws_secret_key = "..."
```

### Kali Linux Features

#### Tor Integration

```bash
# Tor über Proxychains
proxychains4 python3 kickbase_ultimate_analyzer.py --mode quick
```

#### Verschlüsselung

```env
ENCRYPTION_KEY=your-32-char-key-here
USE_ENCRYPTION=true
```

## 📊 Scheduler & Automatisierung

### Systemd Service

```bash
# Service erstellen (während Installation)
sudo systemctl enable kickbase-analyzer.service
sudo systemctl start kickbase-analyzer.service

# Status prüfen
sudo systemctl status kickbase-analyzer.service

# Logs anzeigen
journalctl -u kickbase-analyzer.service -f
```

### Cron Jobs

```bash
# Tägliche Analyse um 8:00
0 8 * * * /path/to/venv/bin/python /path/to/kickbase_ultimate_analyzer.py --mode full

# Stündliche Updates
0 * * * * /path/to/venv/bin/python /path/to/kickbase_ultimate_analyzer.py --mode quick
```

## 🔍 Troubleshooting

### Häufige Probleme

#### Login Fehler

```bash
# Teste Login manuell
python3 -c "
from kickbase_ultimate_analyzer import KickbaseAPIWrapper, Config
config = Config()
api = KickbaseAPIWrapper(config)
print('Login erfolgreich!' if api.login() else 'Login fehlgeschlagen!')
"
```

#### Abhängigkeiten Fehler

```bash
# Reinstalliere Requirements
pip install --force-reinstall -r requirements.txt

# Prüfe Installation
python3 -c "import pandas, numpy, sklearn, xgboost; print('OK')"
```

#### Chrome/Selenium Probleme

```bash
# Installiere Chrome
sudo apt install chromium-browser chromium-chromedriver

# Teste Selenium
python3 -c "
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
options = Options()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)
print('Selenium OK')
driver.quit()
"
```

### Debug-Modus

```bash
# Verbose Output
python3 kickbase_ultimate_analyzer.py --mode quick --verbose

# Debug Logs
export LOG_LEVEL=DEBUG
python3 kickbase_ultimate_analyzer.py --mode quick
```

## 🤝 Contributing

Beiträge sind willkommen! Bitte:

1. Fork das Repository
2. Erstelle einen Feature Branch
3. Committe deine Änderungen
4. Erstelle einen Pull Request

### Development Setup

```bash
# Development Dependencies
pip install -r requirements-dev.txt

# Code Formatting
black kickbase_ultimate_analyzer.py

# Linting
flake8 kickbase_ultimate_analyzer.py

# Tests
pytest tests/
```

## ⚠️ Disclaimer

**WICHTIG**: Dieses Tool ist inoffiziell und nicht mit Kickbase verbunden.

- **Risiko**: Kickbase könnte Accounts bei erkannter Automation sperren
- **Verwendung**: Nur für persönliche Analysen und Bildungszwecke
- **Haftung**: Keine Gewähr für Richtigkeit der Vorhersagen
- **Rate Limits**: Nutze das Tool sparsam um Sperrungen zu vermeiden

## 📄 Lizenz

MIT License - siehe [LICENSE](LICENSE) für Details.

## 🙏 Credits

Inspiriert von und basierend auf:

- [kevinskyba/kickbase-api-python](https://github.com/kevinskyba/kickbase-api-python)
- [elcaiseri/Fantasy-Premier-League-LTX](https://github.com/elcaiseri/Fantasy-Premier-League-LTX)
- [sertalpbilal/FPL-Optimization-Tools](https://github.com/sertalpbilal/FPL-Optimization-Tools)
- [Chillohillo/Kickbase-Insights](https://github.com/Chillohillo/Kickbase-Insights)

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/kickbase-ultimate-analyzer/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/kickbase-ultimate-analyzer/discussions)
- **Wiki**: [GitHub Wiki](https://github.com/yourusername/kickbase-ultimate-analyzer/wiki)

---

**⭐ Wenn dir das Tool gefällt, gib dem Repository einen Star!**
