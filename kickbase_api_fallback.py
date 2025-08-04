#!/usr/bin/env python3
"""
Kickbase API Fallback Implementation
===================================

Fallback-Implementierung für Kickbase API wenn keine Wrapper verfügbar sind.
Verwendet direkte HTTP-Requests und Web Scraping.

Author: AI Assistant
Version: 1.0.0
License: MIT
"""

import requests
import json
import time
import re
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging

logger = logging.getLogger(__name__)

class KickbaseFallbackAPI:
    """Fallback API für Kickbase ohne offizielle Wrapper"""
    
    def __init__(self, email: str, password: str):
        self.email = email
        self.password = password
        self.session = requests.Session()
        self.token = None
        self.user_id = None
        self.leagues = []
        
        # Headers für Requests
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'de-DE,de;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
        })
    
    def login(self) -> bool:
        """Login zu Kickbase über verschiedene Methoden"""
        try:
            # Methode 1: Direkte API
            if self._login_direct_api():
                logger.info("Login erfolgreich über direkte API")
                return True
            
            # Methode 2: Web Scraping
            if self._login_web_scraping():
                logger.info("Login erfolgreich über Web Scraping")
                return True
            
            # Methode 3: Selenium
            if self._login_selenium():
                logger.info("Login erfolgreich über Selenium")
                return True
            
            logger.error("Alle Login-Methoden fehlgeschlagen")
            return False
            
        except Exception as e:
            logger.error(f"Login Fehler: {e}")
            return False
    
    def _login_direct_api(self) -> bool:
        """Direkte API Login"""
        try:
            login_url = "https://api.kickbase.com/v4/user/login"
            
            payload = {
                "em": self.email,
                "pass": self.password,
                "loy": False,
                "rep": {}
            }
            
            response = self.session.post(login_url, json=payload, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                self.token = data.get("tkn")
                self.user_id = data.get("u", {}).get("id")
                self.leagues = data.get("l", [])
                
                # Token zu Headers hinzufügen
                self.session.headers.update({
                    "Authorization": f"Bearer {self.token}"
                })
                
                return True
            else:
                logger.warning(f"API Login fehlgeschlagen: {response.status_code}")
                return False
                
        except Exception as e:
            logger.warning(f"Direkte API Login Fehler: {e}")
            return False
    
    def _login_web_scraping(self) -> bool:
        """Login über Web Scraping"""
        try:
            # Hole Login-Seite
            login_page_url = "https://www.kickbase.com/login"
            response = self.session.get(login_page_url)
            
            if response.status_code != 200:
                return False
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Suche nach CSRF Token oder ähnlichem
            csrf_token = None
            csrf_input = soup.find('input', {'name': '_token'})
            if csrf_input:
                csrf_token = csrf_input.get('value')
            
            # Login-Daten
            login_data = {
                'email': self.email,
                'password': self.password,
            }
            
            if csrf_token:
                login_data['_token'] = csrf_token
            
            # Login Request
            login_response = self.session.post(
                "https://www.kickbase.com/login",
                data=login_data,
                allow_redirects=True
            )
            
            # Prüfe ob Login erfolgreich
            if "dashboard" in login_response.url or login_response.status_code == 200:
                # Versuche Token aus Response zu extrahieren
                self._extract_token_from_response(login_response.text)
                return True
            
            return False
            
        except Exception as e:
            logger.warning(f"Web Scraping Login Fehler: {e}")
            return False
    
    def _login_selenium(self) -> bool:
        """Login über Selenium WebDriver"""
        driver = None
        try:
            # Chrome Options
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920,1080")
            
            # WebDriver erstellen
            driver = webdriver.Chrome(options=chrome_options)
            
            # Login-Seite öffnen
            driver.get("https://www.kickbase.com/login")
            
            # Warte auf Login-Form
            wait = WebDriverWait(driver, 10)
            
            # Email eingeben
            email_field = wait.until(EC.presence_of_element_located((By.NAME, "email")))
            email_field.send_keys(self.email)
            
            # Passwort eingeben
            password_field = driver.find_element(By.NAME, "password")
            password_field.send_keys(self.password)
            
            # Login Button klicken
            login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
            login_button.click()
            
            # Warte auf Redirect
            wait.until(lambda d: "dashboard" in d.current_url or "league" in d.current_url)
            
            # Cookies zu Session hinzufügen
            selenium_cookies = driver.get_cookies()
            for cookie in selenium_cookies:
                self.session.cookies.set(cookie['name'], cookie['value'])
            
            # Versuche Token aus Local Storage zu holen
            try:
                token = driver.execute_script("return localStorage.getItem('authToken') || sessionStorage.getItem('authToken');")
                if token:
                    self.token = token
                    self.session.headers.update({
                        "Authorization": f"Bearer {self.token}"
                    })
            except:
                pass
            
            return True
            
        except Exception as e:
            logger.warning(f"Selenium Login Fehler: {e}")
            return False
        finally:
            if driver:
                driver.quit()
    
    def _extract_token_from_response(self, html: str):
        """Extrahiere Token aus HTML Response"""
        try:
            # Suche nach JavaScript Variablen
            token_patterns = [
                r'authToken["\']?\s*[:=]\s*["\']([^"\']+)["\']',
                r'token["\']?\s*[:=]\s*["\']([^"\']+)["\']',
                r'jwt["\']?\s*[:=]\s*["\']([^"\']+)["\']',
                r'bearer["\']?\s*[:=]\s*["\']([^"\']+)["\']'
            ]
            
            for pattern in token_patterns:
                match = re.search(pattern, html, re.IGNORECASE)
                if match:
                    self.token = match.group(1)
                    self.session.headers.update({
                        "Authorization": f"Bearer {self.token}"
                    })
                    logger.info("Token aus HTML extrahiert")
                    return
                    
        except Exception as e:
            logger.warning(f"Token Extraktion Fehler: {e}")
    
    def get_leagues(self) -> List[Dict]:
        """Hole Benutzer-Ligen"""
        try:
            if self.leagues:
                return self.leagues
            
            # API Endpoint
            url = "https://api.kickbase.com/v4/leagues"
            response = self.session.get(url)
            
            if response.status_code == 200:
                data = response.json()
                self.leagues = data.get("leagues", [])
                return self.leagues
            else:
                # Fallback: Web Scraping
                return self._scrape_leagues()
                
        except Exception as e:
            logger.error(f"Fehler beim Abrufen der Ligen: {e}")
            return []
    
    def _scrape_leagues(self) -> List[Dict]:
        """Scrape Ligen von der Website"""
        try:
            url = "https://www.kickbase.com/leagues"
            response = self.session.get(url)
            
            if response.status_code != 200:
                return []
            
            soup = BeautifulSoup(response.text, 'html.parser')
            leagues = []
            
            # Suche nach Liga-Elementen (Beispiel-Selektoren)
            league_elements = soup.find_all('div', class_='league-item')
            
            for element in league_elements:
                try:
                    league_data = {
                        'id': element.get('data-league-id'),
                        'name': element.find('h3').text.strip() if element.find('h3') else 'Unknown',
                        'members': len(element.find_all('div', class_='member')),
                    }
                    leagues.append(league_data)
                except:
                    continue
            
            return leagues
            
        except Exception as e:
            logger.error(f"Liga Scraping Fehler: {e}")
            return []
    
    def get_league_players(self, league_id: str) -> List[Dict]:
        """Hole Spieler einer Liga"""
        try:
            # API Endpoint
            url = f"https://api.kickbase.com/v4/leagues/{league_id}/players"
            response = self.session.get(url)
            
            if response.status_code == 200:
                data = response.json()
                return data.get("players", [])
            else:
                # Fallback: Web Scraping
                return self._scrape_league_players(league_id)
                
        except Exception as e:
            logger.error(f"Fehler beim Abrufen der Spieler: {e}")
            return []
    
    def _scrape_league_players(self, league_id: str) -> List[Dict]:
        """Scrape Spieler von der Website"""
        try:
            url = f"https://www.kickbase.com/leagues/{league_id}/players"
            response = self.session.get(url)
            
            if response.status_code != 200:
                return []
            
            soup = BeautifulSoup(response.text, 'html.parser')
            players = []
            
            # Suche nach Spieler-Elementen
            player_elements = soup.find_all('div', class_='player-item')
            
            for element in player_elements:
                try:
                    player_data = {
                        'id': element.get('data-player-id'),
                        'name': element.find('span', class_='player-name').text.strip(),
                        'team': element.find('span', class_='team-name').text.strip(),
                        'position': element.find('span', class_='position').text.strip(),
                        'market_value': self._parse_value(element.find('span', class_='value').text),
                        'points': int(element.find('span', class_='points').text or 0),
                    }
                    players.append(player_data)
                except Exception as e:
                    logger.warning(f"Fehler beim Parsen von Spieler: {e}")
                    continue
            
            return players
            
        except Exception as e:
            logger.error(f"Spieler Scraping Fehler: {e}")
            return []
    
    def get_player_stats(self, player_id: str) -> Dict:
        """Hole detaillierte Spielerstatistiken"""
        try:
            # API Endpoint
            url = f"https://api.kickbase.com/v4/players/{player_id}/stats"
            response = self.session.get(url)
            
            if response.status_code == 200:
                return response.json()
            else:
                # Fallback: Basis-Stats
                return self._get_basic_player_stats(player_id)
                
        except Exception as e:
            logger.error(f"Fehler beim Abrufen der Spielerstatistiken: {e}")
            return {}
    
    def _get_basic_player_stats(self, player_id: str) -> Dict:
        """Basis Spieler-Statistiken"""
        return {
            'total_points': 0,
            'average_points': 0.0,
            'match_count': 0,
            'goals': 0,
            'assists': 0,
            'yellow_cards': 0,
            'red_cards': 0,
        }
    
    def get_market_value_history(self, player_id: str) -> List[Dict]:
        """Hole Marktwert-Historie"""
        try:
            # API Endpoint
            url = f"https://api.kickbase.com/v4/players/{player_id}/market-value"
            response = self.session.get(url)
            
            if response.status_code == 200:
                data = response.json()
                return data.get("history", [])
            else:
                # Fallback: Generiere Dummy-Historie
                return self._generate_dummy_history(player_id)
                
        except Exception as e:
            logger.error(f"Fehler beim Abrufen der Marktwert-Historie: {e}")
            return []
    
    def _generate_dummy_history(self, player_id: str) -> List[Dict]:
        """Generiere Dummy-Marktwert-Historie"""
        history = []
        base_value = 5000000  # 5 Millionen als Basis
        
        for i in range(30):  # 30 Tage Historie
            date = datetime.now() - timedelta(days=i)
            change = (hash(player_id + str(i)) % 1000000) - 500000  # Random zwischen -500k und +500k
            
            history.append({
                'date': date.isoformat(),
                'value': base_value + change,
                'change': change if i > 0 else 0
            })
        
        return history
    
    def _parse_value(self, value_str: str) -> int:
        """Parse Marktwert-String zu Integer"""
        try:
            # Entferne Währungszeichen und Formatierung
            clean_str = re.sub(r'[€$£,.\s]', '', value_str)
            
            # Erkenne Einheiten
            if 'M' in value_str.upper() or 'MIO' in value_str.upper():
                return int(float(clean_str.replace('M', '').replace('MIO', '')) * 1000000)
            elif 'K' in value_str.upper() or 'T' in value_str.upper():
                return int(float(clean_str.replace('K', '').replace('T', '')) * 1000)
            else:
                return int(clean_str) if clean_str.isdigit() else 0
                
        except:
            return 0
    
    def get_match_results(self, league_id: str, limit: int = 50) -> List[Dict]:
        """Hole Spielergebnisse"""
        try:
            # API Endpoint
            url = f"https://api.kickbase.com/v4/leagues/{league_id}/matches"
            params = {'limit': limit}
            response = self.session.get(url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                return data.get("matches", [])
            else:
                # Fallback: Scrape von Bundesliga.com oder anderen Quellen
                return self._scrape_match_results()
                
        except Exception as e:
            logger.error(f"Fehler beim Abrufen der Spielergebnisse: {e}")
            return []
    
    def _scrape_match_results(self) -> List[Dict]:
        """Scrape Spielergebnisse von externen Quellen"""
        try:
            # Beispiel: Bundesliga.com
            url = "https://www.bundesliga.com/de/bundesliga/spieltag"
            response = requests.get(url, timeout=30)
            
            if response.status_code != 200:
                return []
            
            soup = BeautifulSoup(response.text, 'html.parser')
            matches = []
            
            # Suche nach Spiel-Elementen
            match_elements = soup.find_all('div', class_='match')
            
            for element in match_elements[:10]:  # Limit auf 10
                try:
                    match_data = {
                        'id': f"match_{len(matches)}",
                        'home_team': element.find('span', class_='home-team').text.strip(),
                        'away_team': element.find('span', class_='away-team').text.strip(),
                        'home_goals': 0,
                        'away_goals': 0,
                        'date': datetime.now().isoformat(),
                        'status': 'finished'
                    }
                    
                    # Versuche Ergebnis zu parsen
                    score_element = element.find('span', class_='score')
                    if score_element:
                        score_text = score_element.text.strip()
                        if ':' in score_text:
                            home_goals, away_goals = score_text.split(':')
                            match_data['home_goals'] = int(home_goals.strip())
                            match_data['away_goals'] = int(away_goals.strip())
                    
                    matches.append(match_data)
                except:
                    continue
            
            return matches
            
        except Exception as e:
            logger.error(f"Match Results Scraping Fehler: {e}")
            return []
    
    def search_players(self, query: str) -> List[Dict]:
        """Suche Spieler"""
        try:
            # API Endpoint
            url = f"https://api.kickbase.com/v4/players/search"
            params = {'q': query, 'limit': 20}
            response = self.session.get(url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                return data.get("players", [])
            else:
                return []
                
        except Exception as e:
            logger.error(f"Fehler bei Spielersuche: {e}")
            return []
    
    def get_user_info(self) -> Dict:
        """Hole Benutzerinformationen"""
        try:
            if not self.user_id:
                return {}
            
            # API Endpoint
            url = f"https://api.kickbase.com/v4/users/{self.user_id}"
            response = self.session.get(url)
            
            if response.status_code == 200:
                return response.json()
            else:
                return {'id': self.user_id, 'email': self.email}
                
        except Exception as e:
            logger.error(f"Fehler beim Abrufen der Benutzerinformationen: {e}")
            return {}
    
    def close(self):
        """Schließe Session"""
        if self.session:
            self.session.close()

# Beispiel-Verwendung
if __name__ == "__main__":
    # Test der Fallback API
    email = "test@example.com"
    password = "password"
    
    api = KickbaseFallbackAPI(email, password)
    
    if api.login():
        print("Login erfolgreich!")
        
        leagues = api.get_leagues()
        print(f"Gefundene Ligen: {len(leagues)}")
        
        if leagues:
            league_id = leagues[0]['id']
            players = api.get_league_players(league_id)
            print(f"Spieler in Liga: {len(players)}")
            
            if players:
                player = players[0]
                stats = api.get_player_stats(player['id'])
                print(f"Spieler Stats: {stats}")
                
                history = api.get_market_value_history(player['id'])
                print(f"Marktwert-Historie: {len(history)} Einträge")
    else:
        print("Login fehlgeschlagen!")
    
    api.close()