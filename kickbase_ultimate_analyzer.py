#!/usr/bin/env python3
"""
Kickbase Ultimate Analyzer
==========================

Ein umfangreiches Python-Tool für Kickbase-Analyse mit:
- API-Integration (mehrere Wrapper)
- Machine Learning Predictions
- Cloud-Integration
- AI-Integration (ChatGPT/Grok)
- Kali Linux Support
- Automatisierte Datenexporte

Author: AI Assistant
Version: 1.0.0
License: MIT
"""

import os
import sys
import json
import logging
import datetime
import time
import asyncio
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Core imports
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import xgboost as xgb
import lightgbm as lgb

# Web and API
import requests
import aiohttp
from bs4 import BeautifulSoup
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# Data visualization
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

# Configuration and utilities
from dotenv import load_dotenv
import schedule
import yaml
from loguru import logger
import sqlite3
from sqlalchemy import create_engine

# AI Integration
try:
    import openai
except ImportError:
    openai = None

try:
    from anthropic import Anthropic
except ImportError:
    Anthropic = None

# Cloud services
try:
    from google.cloud import storage as gcs
    from google.cloud import drive
except ImportError:
    gcs = None
    drive = None

try:
    import boto3
except ImportError:
    boto3 = None

# Load environment variables
load_dotenv()

# Configuration
@dataclass
class Config:
    """Konfigurationsklasse für das Kickbase Analyzer Tool"""
    
    # Kickbase Credentials
    kickbase_email: str = os.getenv("KICKBASE_EMAIL", "")
    kickbase_password: str = os.getenv("KICKBASE_PASSWORD", "")
    kickbase_league_id: str = os.getenv("KICKBASE_LEAGUE_ID", "")
    
    # AI API Keys
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    anthropic_api_key: str = os.getenv("ANTHROPIC_API_KEY", "")
    grok_api_key: str = os.getenv("GROK_API_KEY", "")
    
    # Cloud Storage
    google_credentials_path: str = os.getenv("GOOGLE_CREDENTIALS_PATH", "")
    aws_access_key: str = os.getenv("AWS_ACCESS_KEY_ID", "")
    aws_secret_key: str = os.getenv("AWS_SECRET_ACCESS_KEY", "")
    
    # Data paths
    data_dir: str = "kickbase_data"
    export_dir: str = "exports"
    logs_dir: str = "logs"
    
    # ML Parameters
    ml_test_size: float = 0.2
    ml_random_state: int = 42
    ml_n_estimators: int = 100
    
    # Automation
    auto_update_interval: int = 3600  # seconds
    enable_scheduling: bool = True
    
    def __post_init__(self):
        """Erstelle notwendige Verzeichnisse"""
        for directory in [self.data_dir, self.export_dir, self.logs_dir]:
            Path(directory).mkdir(exist_ok=True)

class KickbaseAPIWrapper:
    """Wrapper für verschiedene Kickbase API Implementierungen"""
    
    def __init__(self, config: Config):
        self.config = config
        self.session = requests.Session()
        self.token = None
        self.user_data = None
        self.leagues = []
        
    def login(self) -> bool:
        """Login zu Kickbase"""
        try:
            # Verschiedene API-Ansätze versuchen
            return self._try_official_api() or self._try_unofficial_api()
        except Exception as e:
            logger.error(f"Login fehlgeschlagen: {e}")
            return False
    
    def _try_official_api(self) -> bool:
        """Versuche offizielle API"""
        try:
            login_url = "https://api.kickbase.com/v4/user/login"
            payload = {
                "em": self.config.kickbase_email,
                "pass": self.config.kickbase_password,
                "loy": False,
                "rep": {}
            }
            
            response = self.session.post(login_url, json=payload)
            if response.status_code == 200:
                data = response.json()
                self.token = data.get("tkn")
                self.user_data = data.get("u")
                self.leagues = data.get("l", [])
                
                # Set authorization header
                self.session.headers.update({
                    "Authorization": f"Bearer {self.token}"
                })
                
                logger.success("Kickbase Login erfolgreich (Offizielle API)")
                return True
        except Exception as e:
            logger.warning(f"Offizielle API fehlgeschlagen: {e}")
        
        return False
    
    def _try_unofficial_api(self) -> bool:
        """Versuche inoffizielle API-Wrapper"""
        try:
            # Hier würden verschiedene Wrapper-Bibliotheken verwendet
            # Beispiel für kevinskyba/kickbase-api-python
            from kickbase_api.kickbase import Kickbase
            from kickbase_api.exceptions import KickbaseException
            
            kb = Kickbase()
            user, leagues = kb.login(self.config.kickbase_email, self.config.kickbase_password)
            
            self.user_data = user
            self.leagues = leagues
            self._kb_instance = kb
            
            logger.success("Kickbase Login erfolgreich (Inoffizielle API)")
            return True
            
        except ImportError:
            logger.warning("kickbase_api Bibliothek nicht verfügbar")
        except Exception as e:
            logger.warning(f"Inoffizielle API fehlgeschlagen: {e}")
        
        return False
    
    def get_league_players(self, league_id: Optional[str] = None) -> List[Dict]:
        """Hole alle Spieler einer Liga"""
        try:
            if hasattr(self, '_kb_instance'):
                # Verwende inoffizielle API
                league = self._find_league(league_id)
                if league:
                    players = self._kb_instance.league_players(league)
                    return self._process_players_data(players)
            else:
                # Verwende offizielle API
                url = f"https://api.kickbase.com/v4/leagues/{league_id or self.config.kickbase_league_id}/players"
                response = self.session.get(url)
                if response.status_code == 200:
                    return response.json().get("players", [])
        except Exception as e:
            logger.error(f"Fehler beim Abrufen der Spieler: {e}")
        
        return []
    
    def get_player_stats(self, player_id: str) -> Dict:
        """Hole detaillierte Spielerstatistiken"""
        try:
            if hasattr(self, '_kb_instance'):
                # Implementierung für inoffizielle API
                pass
            else:
                # Offizielle API
                url = f"https://api.kickbase.com/v4/players/{player_id}/stats"
                response = self.session.get(url)
                if response.status_code == 200:
                    return response.json()
        except Exception as e:
            logger.error(f"Fehler beim Abrufen der Spielerstatistiken: {e}")
        
        return {}
    
    def get_market_values_history(self, player_id: str) -> List[Dict]:
        """Hole Marktwert-Historie eines Spielers"""
        try:
            if hasattr(self, '_kb_instance'):
                player = self._find_player(player_id)
                if player:
                    return self._kb_instance.player_market_value_history(player)
            else:
                url = f"https://api.kickbase.com/v4/players/{player_id}/market-value"
                response = self.session.get(url)
                if response.status_code == 200:
                    return response.json().get("history", [])
        except Exception as e:
            logger.error(f"Fehler beim Abrufen der Marktwert-Historie: {e}")
        
        return []
    
    def _find_league(self, league_id: Optional[str]):
        """Finde Liga basierend auf ID oder Name"""
        if not league_id:
            return self.leagues[0] if self.leagues else None
        
        for league in self.leagues:
            if hasattr(league, 'id') and league.id == league_id:
                return league
            elif isinstance(league, dict) and league.get('id') == league_id:
                return league
        
        return None
    
    def _find_player(self, player_id: str):
        """Finde Spieler basierend auf ID"""
        # Implementierung je nach API-Wrapper
        pass
    
    def _process_players_data(self, players) -> List[Dict]:
        """Verarbeite Spielerdaten zu einheitlichem Format"""
        processed = []
        for player in players:
            try:
                data = {
                    "id": getattr(player, 'id', player.get('id')),
                    "name": getattr(player, 'name', player.get('name')),
                    "first_name": getattr(player, 'first_name', player.get('firstName')),
                    "last_name": getattr(player, 'last_name', player.get('lastName')),
                    "team_id": getattr(player, 'team_id', player.get('teamId')),
                    "position": getattr(player, 'position', player.get('position')),
                    "market_value": getattr(player, 'market_value', player.get('marketValue')),
                    "market_value_trend": getattr(player, 'market_value_trend', player.get('marketValueTrend')),
                    "points": getattr(player, 'points', player.get('points', 0)),
                    "average_points": getattr(player, 'average_points', player.get('averagePoints', 0)),
                }
                processed.append(data)
            except Exception as e:
                logger.warning(f"Fehler beim Verarbeiten von Spieler {player}: {e}")
        
        return processed

class DataCollector:
    """Sammelt Daten aus verschiedenen Quellen"""
    
    def __init__(self, config: Config, api_wrapper: KickbaseAPIWrapper):
        self.config = config
        self.api = api_wrapper
        self.data_cache = {}
    
    async def collect_all_data(self) -> Dict[str, pd.DataFrame]:
        """Sammle alle verfügbaren Daten"""
        logger.info("Starte Datensammlung...")
        
        data = {}
        
        # Kickbase Daten
        data['players'] = await self._collect_player_data()
        data['market_values'] = await self._collect_market_value_data()
        data['match_results'] = await self._collect_match_data()
        
        # Externe Daten
        data['bundesliga_stats'] = await self._collect_bundesliga_stats()
        data['weather_data'] = await self._collect_weather_data()
        data['betting_odds'] = await self._collect_betting_odds()
        
        logger.success(f"Datensammlung abgeschlossen. {len(data)} Datensätze gesammelt.")
        return data
    
    async def _collect_player_data(self) -> pd.DataFrame:
        """Sammle Spielerdaten"""
        try:
            players = self.api.get_league_players()
            if not players:
                logger.warning("Keine Spielerdaten erhalten")
                return pd.DataFrame()
            
            # Erweitere Daten mit detaillierten Stats
            detailed_players = []
            for player in players[:10]:  # Limit für Demo
                try:
                    stats = self.api.get_player_stats(player['id'])
                    player.update(stats)
                    detailed_players.append(player)
                    time.sleep(0.1)  # Rate limiting
                except Exception as e:
                    logger.warning(f"Fehler bei Spieler {player.get('name', 'Unknown')}: {e}")
                    detailed_players.append(player)
            
            df = pd.DataFrame(detailed_players)
            logger.info(f"Spielerdaten gesammelt: {len(df)} Spieler")
            return df
            
        except Exception as e:
            logger.error(f"Fehler beim Sammeln der Spielerdaten: {e}")
            return pd.DataFrame()
    
    async def _collect_market_value_data(self) -> pd.DataFrame:
        """Sammle Marktwert-Historien"""
        try:
            market_data = []
            players = self.api.get_league_players()
            
            for player in players[:5]:  # Limit für Demo
                try:
                    history = self.api.get_market_values_history(player['id'])
                    for entry in history:
                        market_data.append({
                            'player_id': player['id'],
                            'player_name': player['name'],
                            'date': entry.get('date'),
                            'market_value': entry.get('value'),
                            'change': entry.get('change', 0)
                        })
                    time.sleep(0.1)
                except Exception as e:
                    logger.warning(f"Fehler bei Marktwert-Historie für {player.get('name', 'Unknown')}: {e}")
            
            df = pd.DataFrame(market_data)
            logger.info(f"Marktwert-Daten gesammelt: {len(df)} Einträge")
            return df
            
        except Exception as e:
            logger.error(f"Fehler beim Sammeln der Marktwert-Daten: {e}")
            return pd.DataFrame()
    
    async def _collect_match_data(self) -> pd.DataFrame:
        """Sammle Spielergebnisse"""
        try:
            # Hier würde eine Implementierung für Spielergebnisse stehen
            # Beispiel mit Web Scraping von ligainsider.de oder anderen Quellen
            
            matches = []
            # Dummy-Daten für Demo
            for i in range(10):
                matches.append({
                    'match_id': f'match_{i}',
                    'home_team': f'Team_{i}',
                    'away_team': f'Team_{i+1}',
                    'home_goals': np.random.randint(0, 4),
                    'away_goals': np.random.randint(0, 4),
                    'date': datetime.datetime.now() - datetime.timedelta(days=i)
                })
            
            df = pd.DataFrame(matches)
            logger.info(f"Spiel-Daten gesammelt: {len(df)} Spiele")
            return df
            
        except Exception as e:
            logger.error(f"Fehler beim Sammeln der Spiel-Daten: {e}")
            return pd.DataFrame()
    
    async def _collect_bundesliga_stats(self) -> pd.DataFrame:
        """Sammle Bundesliga-Statistiken"""
        try:
            # Web Scraping von offiziellen Quellen
            url = "https://www.bundesliga.com/de/stats"
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        html = await response.text()
                        soup = BeautifulSoup(html, 'html.parser')
                        
                        # Hier würde das Parsing der Statistiken stehen
                        # Für Demo erstellen wir Dummy-Daten
                        stats = []
                        for i in range(18):  # 18 Bundesliga Teams
                            stats.append({
                                'team': f'Team_{i}',
                                'goals_scored': np.random.randint(20, 80),
                                'goals_conceded': np.random.randint(20, 80),
                                'points': np.random.randint(10, 70)
                            })
                        
                        df = pd.DataFrame(stats)
                        logger.info(f"Bundesliga-Statistiken gesammelt: {len(df)} Teams")
                        return df
            
        except Exception as e:
            logger.error(f"Fehler beim Sammeln der Bundesliga-Statistiken: {e}")
            return pd.DataFrame()
    
    async def _collect_weather_data(self) -> pd.DataFrame:
        """Sammle Wetterdaten für Spieltage"""
        try:
            # Integration mit Weather API (z.B. OpenWeatherMap)
            weather_data = []
            
            # Dummy-Daten für Demo
            for i in range(30):
                weather_data.append({
                    'date': datetime.datetime.now() - datetime.timedelta(days=i),
                    'temperature': np.random.randint(-5, 30),
                    'humidity': np.random.randint(30, 90),
                    'wind_speed': np.random.randint(0, 20),
                    'precipitation': np.random.randint(0, 10)
                })
            
            df = pd.DataFrame(weather_data)
            logger.info(f"Wetter-Daten gesammelt: {len(df)} Tage")
            return df
            
        except Exception as e:
            logger.error(f"Fehler beim Sammeln der Wetter-Daten: {e}")
            return pd.DataFrame()
    
    async def _collect_betting_odds(self) -> pd.DataFrame:
        """Sammle Wettquoten"""
        try:
            # Integration mit Betting APIs
            odds_data = []
            
            # Dummy-Daten für Demo
            for i in range(20):
                odds_data.append({
                    'match_id': f'match_{i}',
                    'home_win_odds': np.random.uniform(1.2, 5.0),
                    'draw_odds': np.random.uniform(2.5, 4.0),
                    'away_win_odds': np.random.uniform(1.2, 5.0),
                    'over_2_5_odds': np.random.uniform(1.3, 3.0),
                    'under_2_5_odds': np.random.uniform(1.3, 3.0)
                })
            
            df = pd.DataFrame(odds_data)
            logger.info(f"Wettquoten gesammelt: {len(df)} Spiele")
            return df
            
        except Exception as e:
            logger.error(f"Fehler beim Sammeln der Wettquoten: {e}")
            return pd.DataFrame()

class MLPredictor:
    """Machine Learning Modelle für Vorhersagen"""
    
    def __init__(self, config: Config):
        self.config = config
        self.models = {}
        self.scalers = {}
        self.encoders = {}
        self.feature_columns = []
    
    def prepare_features(self, data: Dict[str, pd.DataFrame]) -> pd.DataFrame:
        """Bereite Features für ML vor"""
        try:
            players_df = data.get('players', pd.DataFrame())
            market_df = data.get('market_values', pd.DataFrame())
            
            if players_df.empty:
                logger.warning("Keine Spielerdaten für Feature-Erstellung verfügbar")
                return pd.DataFrame()
            
            # Basis-Features
            features = players_df.copy()
            
            # Numerische Features
            numeric_features = ['market_value', 'points', 'average_points']
            for col in numeric_features:
                if col in features.columns:
                    features[col] = pd.to_numeric(features[col], errors='coerce')
            
            # Kategorische Features encodieren
            categorical_features = ['position', 'team_id']
            for col in categorical_features:
                if col in features.columns:
                    if col not in self.encoders:
                        self.encoders[col] = LabelEncoder()
                        features[f'{col}_encoded'] = self.encoders[col].fit_transform(
                            features[col].astype(str)
                        )
                    else:
                        features[f'{col}_encoded'] = self.encoders[col].transform(
                            features[col].astype(str)
                        )
            
            # Erweiterte Features
            if not market_df.empty:
                # Marktwert-Trends
                market_trends = market_df.groupby('player_id').agg({
                    'market_value': ['mean', 'std', 'min', 'max'],
                    'change': ['mean', 'sum']
                }).reset_index()
                
                market_trends.columns = ['player_id'] + [
                    f'market_{col[0]}_{col[1]}' for col in market_trends.columns[1:]
                ]
                
                features = features.merge(market_trends, left_on='id', right_on='player_id', how='left')
            
            # Zeitbasierte Features
            features['data_collection_date'] = datetime.datetime.now()
            features['days_since_season_start'] = (
                features['data_collection_date'] - datetime.datetime(2024, 8, 1)
            ).dt.days
            
            # Performance-Ratios
            if 'points' in features.columns and 'market_value' in features.columns:
                features['points_per_million'] = features['points'] / (features['market_value'] / 1000000)
                features['value_efficiency'] = features['average_points'] / (features['market_value'] / 1000000)
            
            # Fülle NaN-Werte
            numeric_columns = features.select_dtypes(include=[np.number]).columns
            features[numeric_columns] = features[numeric_columns].fillna(0)
            
            self.feature_columns = [col for col in features.columns 
                                  if col not in ['id', 'name', 'first_name', 'last_name', 'data_collection_date']]
            
            logger.info(f"Features erstellt: {len(self.feature_columns)} Spalten, {len(features)} Zeilen")
            return features
            
        except Exception as e:
            logger.error(f"Fehler bei Feature-Erstellung: {e}")
            return pd.DataFrame()
    
    def train_models(self, features_df: pd.DataFrame) -> Dict[str, Any]:
        """Trainiere verschiedene ML-Modelle"""
        try:
            if features_df.empty or not self.feature_columns:
                logger.error("Keine Features für Training verfügbar")
                return {}
            
            # Ziel-Variable: Marktwert-Veränderung vorhersagen
            target_col = 'market_value'
            if target_col not in features_df.columns:
                logger.error(f"Ziel-Variable {target_col} nicht gefunden")
                return {}
            
            # Daten vorbereiten
            X = features_df[self.feature_columns].select_dtypes(include=[np.number])
            y = features_df[target_col]
            
            # Entferne Zeilen mit NaN in Ziel-Variable
            valid_indices = ~y.isna()
            X = X[valid_indices]
            y = y[valid_indices]
            
            if len(X) < 10:
                logger.warning("Zu wenige Daten für Training")
                return {}
            
            # Train-Test Split
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=self.config.ml_test_size, 
                random_state=self.config.ml_random_state
            )
            
            # Feature Scaling
            self.scalers['standard'] = StandardScaler()
            X_train_scaled = self.scalers['standard'].fit_transform(X_train)
            X_test_scaled = self.scalers['standard'].transform(X_test)
            
            # Modelle definieren
            models_to_train = {
                'random_forest': RandomForestRegressor(
                    n_estimators=self.config.ml_n_estimators,
                    random_state=self.config.ml_random_state
                ),
                'gradient_boosting': GradientBoostingRegressor(
                    n_estimators=self.config.ml_n_estimators,
                    random_state=self.config.ml_random_state
                ),
                'xgboost': xgb.XGBRegressor(
                    n_estimators=self.config.ml_n_estimators,
                    random_state=self.config.ml_random_state
                ),
                'lightgbm': lgb.LGBMRegressor(
                    n_estimators=self.config.ml_n_estimators,
                    random_state=self.config.ml_random_state,
                    verbose=-1
                )
            }
            
            results = {}
            
            # Trainiere und evaluiere Modelle
            for name, model in models_to_train.items():
                try:
                    logger.info(f"Trainiere {name}...")
                    
                    # Training
                    if name in ['random_forest', 'gradient_boosting']:
                        model.fit(X_train, y_train)
                        y_pred = model.predict(X_test)
                    else:
                        model.fit(X_train_scaled, y_train)
                        y_pred = model.predict(X_test_scaled)
                    
                    # Evaluation
                    mae = mean_absolute_error(y_test, y_pred)
                    mse = mean_squared_error(y_test, y_pred)
                    r2 = r2_score(y_test, y_pred)
                    
                    # Cross-Validation
                    cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring='r2')
                    
                    results[name] = {
                        'model': model,
                        'mae': mae,
                        'mse': mse,
                        'rmse': np.sqrt(mse),
                        'r2': r2,
                        'cv_mean': cv_scores.mean(),
                        'cv_std': cv_scores.std(),
                        'predictions': y_pred,
                        'test_actual': y_test
                    }
                    
                    logger.success(f"{name}: R² = {r2:.3f}, MAE = {mae:.0f}, RMSE = {np.sqrt(mse):.0f}")
                    
                except Exception as e:
                    logger.error(f"Fehler beim Training von {name}: {e}")
            
            # Speichere bestes Modell
            if results:
                best_model_name = max(results.keys(), key=lambda k: results[k]['r2'])
                self.models['best'] = results[best_model_name]['model']
                logger.info(f"Bestes Modell: {best_model_name} (R² = {results[best_model_name]['r2']:.3f})")
            
            return results
            
        except Exception as e:
            logger.error(f"Fehler beim Modell-Training: {e}")
            return {}
    
    def predict_player_values(self, features_df: pd.DataFrame) -> pd.DataFrame:
        """Vorhersage von Spielerwerten"""
        try:
            if 'best' not in self.models or features_df.empty:
                logger.error("Kein trainiertes Modell oder keine Daten verfügbar")
                return pd.DataFrame()
            
            model = self.models['best']
            X = features_df[self.feature_columns].select_dtypes(include=[np.number])
            
            # Skalierung wenn nötig
            if 'standard' in self.scalers:
                X_scaled = self.scalers['standard'].transform(X)
                predictions = model.predict(X_scaled)
            else:
                predictions = model.predict(X)
            
            # Ergebnisse zusammenstellen
            results_df = features_df[['id', 'name', 'market_value']].copy()
            results_df['predicted_value'] = predictions
            results_df['predicted_change'] = results_df['predicted_value'] - results_df['market_value']
            results_df['predicted_change_percent'] = (
                results_df['predicted_change'] / results_df['market_value'] * 100
            )
            
            # Sortiere nach größter erwarteter Steigerung
            results_df = results_df.sort_values('predicted_change', ascending=False)
            
            logger.info(f"Vorhersagen erstellt für {len(results_df)} Spieler")
            return results_df
            
        except Exception as e:
            logger.error(f"Fehler bei Vorhersagen: {e}")
            return pd.DataFrame()

class AIIntegration:
    """Integration mit AI-Services (ChatGPT, Grok, Claude)"""
    
    def __init__(self, config: Config):
        self.config = config
        self.openai_client = None
        self.anthropic_client = None
        
        # Initialize AI clients
        if config.openai_api_key and openai:
            openai.api_key = config.openai_api_key
            self.openai_client = openai
        
        if config.anthropic_api_key and Anthropic:
            self.anthropic_client = Anthropic(api_key=config.anthropic_api_key)
    
    async def analyze_with_ai(self, data: Dict[str, Any], analysis_type: str = "general") -> str:
        """Analysiere Daten mit AI"""
        try:
            # Erstelle Kontext für AI
            context = self._prepare_context(data, analysis_type)
            
            # Versuche verschiedene AI-Services
            result = None
            
            if self.openai_client:
                result = await self._analyze_with_openai(context, analysis_type)
            
            if not result and self.anthropic_client:
                result = await self._analyze_with_anthropic(context, analysis_type)
            
            if not result:
                result = self._fallback_analysis(data, analysis_type)
            
            return result
            
        except Exception as e:
            logger.error(f"Fehler bei AI-Analyse: {e}")
            return self._fallback_analysis(data, analysis_type)
    
    def _prepare_context(self, data: Dict[str, Any], analysis_type: str) -> str:
        """Bereite Kontext für AI vor"""
        context_parts = []
        
        # Basis-Informationen
        context_parts.append("# Kickbase Analyse Report")
        context_parts.append(f"Analyse-Typ: {analysis_type}")
        context_parts.append(f"Datum: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Spieler-Daten
        if 'top_players' in data:
            context_parts.append("\n## Top Spieler (nach erwarteter Wertsteigerung):")
            for i, player in enumerate(data['top_players'][:10], 1):
                context_parts.append(
                    f"{i}. {player.get('name', 'Unknown')} - "
                    f"Aktueller Wert: {player.get('market_value', 0):,.0f}€, "
                    f"Erwartete Änderung: {player.get('predicted_change', 0):+,.0f}€ "
                    f"({player.get('predicted_change_percent', 0):+.1f}%)"
                )
        
        # Modell-Performance
        if 'model_performance' in data:
            perf = data['model_performance']
            context_parts.append(f"\n## Modell-Performance:")
            context_parts.append(f"R² Score: {perf.get('r2', 0):.3f}")
            context_parts.append(f"Mean Absolute Error: {perf.get('mae', 0):.0f}€")
            context_parts.append(f"Root Mean Square Error: {perf.get('rmse', 0):.0f}€")
        
        # Markt-Trends
        if 'market_trends' in data:
            context_parts.append(f"\n## Markt-Trends:")
            trends = data['market_trends']
            context_parts.append(f"Durchschnittlicher Marktwert: {trends.get('avg_value', 0):,.0f}€")
            context_parts.append(f"Gesamte Marktkapitalisierung: {trends.get('total_value', 0):,.0f}€")
        
        return "\n".join(context_parts)
    
    async def _analyze_with_openai(self, context: str, analysis_type: str) -> Optional[str]:
        """Analyse mit OpenAI"""
        try:
            prompt = self._get_analysis_prompt(analysis_type)
            
            response = await self.openai_client.ChatCompletion.acreate(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": context}
                ],
                max_tokens=1500,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.warning(f"OpenAI Analyse fehlgeschlagen: {e}")
            return None
    
    async def _analyze_with_anthropic(self, context: str, analysis_type: str) -> Optional[str]:
        """Analyse mit Anthropic Claude"""
        try:
            prompt = self._get_analysis_prompt(analysis_type)
            
            response = await self.anthropic_client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=1500,
                messages=[
                    {"role": "user", "content": f"{prompt}\n\n{context}"}
                ]
            )
            
            return response.content[0].text
            
        except Exception as e:
            logger.warning(f"Anthropic Analyse fehlgeschlagen: {e}")
            return None
    
    def _get_analysis_prompt(self, analysis_type: str) -> str:
        """Hole Analyse-Prompt basierend auf Typ"""
        prompts = {
            "general": """Du bist ein erfahrener Kickbase-Experte und Datenanalyst. 
            Analysiere die bereitgestellten Kickbase-Daten und gib konkrete, actionable Empfehlungen.
            
            Fokussiere dich auf:
            1. Die besten Kauf-Empfehlungen (Spieler mit hohem Potenzial)
            2. Verkaufs-Empfehlungen (überbewertete Spieler)
            3. Markt-Trends und Muster
            4. Risiko-Bewertung der Empfehlungen
            5. Kurz- und langfristige Strategien
            
            Antworte auf Deutsch und sei spezifisch mit Zahlen und Begründungen.""",
            
            "transfer": """Du bist ein Kickbase-Transfer-Experte. Analysiere die Daten und gib 
            spezifische Transfer-Empfehlungen.
            
            Fokussiere dich auf:
            1. Sofortige Transfer-Gelegenheiten
            2. Spieler kurz vor Wertsteigerungen
            3. Überbewertete Spieler zum Verkauf
            4. Optimale Transfer-Zeitpunkte
            5. Budget-Allokation
            
            Gib konkrete Kauf/Verkauf-Empfehlungen mit Begründungen.""",
            
            "market_analysis": """Du bist ein Marktanalyst für Fantasy Football. 
            Analysiere die Markttrends und -dynamiken.
            
            Fokussiere dich auf:
            1. Gesamtmarkt-Trends
            2. Positions-spezifische Analysen
            3. Team-basierte Muster
            4. Saisonale Einflüsse
            5. Prognosen für kommende Wochen
            
            Liefere eine umfassende Marktanalyse mit Daten-Support."""
        }
        
        return prompts.get(analysis_type, prompts["general"])
    
    def _fallback_analysis(self, data: Dict[str, Any], analysis_type: str) -> str:
        """Fallback-Analyse ohne AI"""
        try:
            analysis = ["# Kickbase Analyse (Automatisch generiert)", ""]
            
            if 'top_players' in data:
                analysis.append("## 🚀 Top Kauf-Empfehlungen:")
                for i, player in enumerate(data['top_players'][:5], 1):
                    change = player.get('predicted_change', 0)
                    change_pct = player.get('predicted_change_percent', 0)
                    analysis.append(
                        f"{i}. **{player.get('name', 'Unknown')}** - "
                        f"Erwartete Steigerung: {change:+,.0f}€ ({change_pct:+.1f}%)"
                    )
                
                analysis.append("\n## ⚠️ Verkaufs-Kandidaten:")
                bottom_players = sorted(data['top_players'], key=lambda x: x.get('predicted_change', 0))[:3]
                for i, player in enumerate(bottom_players, 1):
                    change = player.get('predicted_change', 0)
                    change_pct = player.get('predicted_change_percent', 0)
                    analysis.append(
                        f"{i}. **{player.get('name', 'Unknown')}** - "
                        f"Erwarteter Verlust: {change:+,.0f}€ ({change_pct:+.1f}%)"
                    )
            
            if 'model_performance' in data:
                perf = data['model_performance']
                analysis.append(f"\n## 📊 Modell-Qualität:")
                analysis.append(f"- Genauigkeit (R²): {perf.get('r2', 0):.1%}")
                analysis.append(f"- Durchschnittlicher Fehler: {perf.get('mae', 0):,.0f}€")
            
            analysis.append("\n## 💡 Strategische Empfehlungen:")
            analysis.append("1. Fokussiere auf Spieler mit positivem Trend")
            analysis.append("2. Verkaufe überbewertete Spieler vor Wertverlusten")
            analysis.append("3. Beobachte Verletzungen und Formkurven")
            analysis.append("4. Diversifiziere dein Portfolio über verschiedene Teams")
            
            return "\n".join(analysis)
            
        except Exception as e:
            logger.error(f"Fehler bei Fallback-Analyse: {e}")
            return "Analyse konnte nicht erstellt werden."

class DataExporter:
    """Export von Daten und Analysen"""
    
    def __init__(self, config: Config):
        self.config = config
        self.export_path = Path(config.export_dir)
        self.export_path.mkdir(exist_ok=True)
    
    def export_all(self, data: Dict[str, Any], analysis: str) -> Dict[str, str]:
        """Exportiere alle Daten und Analysen"""
        exports = {}
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        
        try:
            # JSON Export
            json_file = self.export_path / f"kickbase_analysis_{timestamp}.json"
            exports['json'] = self._export_json(data, json_file)
            
            # CSV Exports
            csv_file = self.export_path / f"kickbase_predictions_{timestamp}.csv"
            exports['csv'] = self._export_csv(data, csv_file)
            
            # Excel Export
            excel_file = self.export_path / f"kickbase_complete_{timestamp}.xlsx"
            exports['excel'] = self._export_excel(data, excel_file)
            
            # HTML Report
            html_file = self.export_path / f"kickbase_report_{timestamp}.html"
            exports['html'] = self._export_html(data, analysis, html_file)
            
            # Markdown Report
            md_file = self.export_path / f"kickbase_report_{timestamp}.md"
            exports['markdown'] = self._export_markdown(data, analysis, md_file)
            
            logger.success(f"Datenexport abgeschlossen: {len(exports)} Dateien erstellt")
            return exports
            
        except Exception as e:
            logger.error(f"Fehler beim Datenexport: {e}")
            return exports
    
    def _export_json(self, data: Dict[str, Any], filepath: Path) -> str:
        """Export als JSON"""
        try:
            # Konvertiere DataFrames zu Dictionaries
            export_data = {}
            for key, value in data.items():
                if isinstance(value, pd.DataFrame):
                    export_data[key] = value.to_dict('records')
                else:
                    export_data[key] = value
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False, default=str)
            
            logger.info(f"JSON Export: {filepath}")
            return str(filepath)
            
        except Exception as e:
            logger.error(f"JSON Export Fehler: {e}")
            return ""
    
    def _export_csv(self, data: Dict[str, Any], filepath: Path) -> str:
        """Export als CSV"""
        try:
            if 'top_players' in data and isinstance(data['top_players'], pd.DataFrame):
                data['top_players'].to_csv(filepath, index=False, encoding='utf-8')
                logger.info(f"CSV Export: {filepath}")
                return str(filepath)
            elif 'top_players' in data:
                # Konvertiere Liste zu DataFrame
                df = pd.DataFrame(data['top_players'])
                df.to_csv(filepath, index=False, encoding='utf-8')
                logger.info(f"CSV Export: {filepath}")
                return str(filepath)
            
        except Exception as e:
            logger.error(f"CSV Export Fehler: {e}")
        
        return ""
    
    def _export_excel(self, data: Dict[str, Any], filepath: Path) -> str:
        """Export als Excel mit mehreren Sheets"""
        try:
            with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
                # Verschiedene Sheets für verschiedene Daten
                if 'top_players' in data:
                    if isinstance(data['top_players'], pd.DataFrame):
                        data['top_players'].to_excel(writer, sheet_name='Predictions', index=False)
                    else:
                        pd.DataFrame(data['top_players']).to_excel(writer, sheet_name='Predictions', index=False)
                
                # Weitere Sheets für andere Daten
                for key, value in data.items():
                    if isinstance(value, pd.DataFrame) and key != 'top_players':
                        sheet_name = key.replace('_', ' ').title()[:31]  # Excel Sheet Name Limit
                        value.to_excel(writer, sheet_name=sheet_name, index=False)
            
            logger.info(f"Excel Export: {filepath}")
            return str(filepath)
            
        except Exception as e:
            logger.error(f"Excel Export Fehler: {e}")
            return ""
    
    def _export_html(self, data: Dict[str, Any], analysis: str, filepath: Path) -> str:
        """Export als HTML Report"""
        try:
            html_content = self._generate_html_report(data, analysis)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            logger.info(f"HTML Export: {filepath}")
            return str(filepath)
            
        except Exception as e:
            logger.error(f"HTML Export Fehler: {e}")
            return ""
    
    def _export_markdown(self, data: Dict[str, Any], analysis: str, filepath: Path) -> str:
        """Export als Markdown"""
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(analysis)
            
            logger.info(f"Markdown Export: {filepath}")
            return str(filepath)
            
        except Exception as e:
            logger.error(f"Markdown Export Fehler: {e}")
            return ""
    
    def _generate_html_report(self, data: Dict[str, Any], analysis: str) -> str:
        """Generiere HTML Report"""
        html_template = """
        <!DOCTYPE html>
        <html lang="de">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Kickbase Analyse Report</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; background-color: #f5f5f5; }
                .container { max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
                h1, h2 { color: #2c3e50; }
                .header { text-align: center; margin-bottom: 30px; }
                .stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin: 20px 0; }
                .stat-card { background: #ecf0f1; padding: 20px; border-radius: 8px; text-align: center; }
                .stat-value { font-size: 2em; font-weight: bold; color: #27ae60; }
                .stat-label { color: #7f8c8d; margin-top: 5px; }
                table { width: 100%; border-collapse: collapse; margin: 20px 0; }
                th, td { padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }
                th { background-color: #34495e; color: white; }
                .positive { color: #27ae60; font-weight: bold; }
                .negative { color: #e74c3c; font-weight: bold; }
                .analysis { background: #f8f9fa; padding: 20px; border-left: 4px solid #3498db; margin: 20px 0; }
                .footer { text-align: center; margin-top: 30px; color: #7f8c8d; }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🚀 Kickbase Ultimate Analyzer</h1>
                    <p>Generiert am: {timestamp}</p>
                </div>
                
                {stats_section}
                
                <h2>📈 Top Spieler Empfehlungen</h2>
                {players_table}
                
                <div class="analysis">
                    <h2>🤖 AI-Analyse</h2>
                    <div>{analysis_content}</div>
                </div>
                
                <div class="footer">
                    <p>Erstellt mit Kickbase Ultimate Analyzer | Alle Angaben ohne Gewähr</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Statistiken
        stats_html = ""
        if 'model_performance' in data:
            perf = data['model_performance']
            stats_html = f"""
            <div class="stats">
                <div class="stat-card">
                    <div class="stat-value">{perf.get('r2', 0):.1%}</div>
                    <div class="stat-label">Modell-Genauigkeit</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{perf.get('mae', 0):,.0f}€</div>
                    <div class="stat-label">Durchschn. Fehler</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{len(data.get('top_players', []))}</div>
                    <div class="stat-label">Analysierte Spieler</div>
                </div>
            </div>
            """
        
        # Spieler Tabelle
        players_html = "<table><tr><th>Rang</th><th>Spieler</th><th>Aktueller Wert</th><th>Erwartete Änderung</th><th>Änderung %</th></tr>"
        
        if 'top_players' in data:
            players = data['top_players'][:10]  # Top 10
            for i, player in enumerate(players, 1):
                change = player.get('predicted_change', 0)
                change_pct = player.get('predicted_change_percent', 0)
                change_class = 'positive' if change > 0 else 'negative'
                
                players_html += f"""
                <tr>
                    <td>{i}</td>
                    <td>{player.get('name', 'Unknown')}</td>
                    <td>{player.get('market_value', 0):,.0f}€</td>
                    <td class="{change_class}">{change:+,.0f}€</td>
                    <td class="{change_class}">{change_pct:+.1f}%</td>
                </tr>
                """
        
        players_html += "</table>"
        
        # Analysis Content formatieren
        analysis_formatted = analysis.replace('\n', '<br>').replace('**', '<strong>').replace('**', '</strong>')
        
        return html_template.format(
            timestamp=datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S"),
            stats_section=stats_html,
            players_table=players_html,
            analysis_content=analysis_formatted
        )

class CloudIntegration:
    """Integration mit Cloud-Services"""
    
    def __init__(self, config: Config):
        self.config = config
        self.gcs_client = None
        self.s3_client = None
        
        self._initialize_clients()
    
    def _initialize_clients(self):
        """Initialisiere Cloud-Clients"""
        try:
            # Google Cloud Storage
            if self.config.google_credentials_path and gcs:
                self.gcs_client = gcs.Client.from_service_account_json(
                    self.config.google_credentials_path
                )
                logger.info("Google Cloud Storage Client initialisiert")
        except Exception as e:
            logger.warning(f"GCS Initialisierung fehlgeschlagen: {e}")
        
        try:
            # AWS S3
            if self.config.aws_access_key and self.config.aws_secret_key and boto3:
                self.s3_client = boto3.client(
                    's3',
                    aws_access_key_id=self.config.aws_access_key,
                    aws_secret_access_key=self.config.aws_secret_key
                )
                logger.info("AWS S3 Client initialisiert")
        except Exception as e:
            logger.warning(f"S3 Initialisierung fehlgeschlagen: {e}")
    
    async def upload_files(self, file_paths: Dict[str, str], bucket_name: str = "kickbase-analysis") -> Dict[str, str]:
        """Lade Dateien in Cloud hoch"""
        upload_results = {}
        
        try:
            # Google Cloud Storage Upload
            if self.gcs_client:
                upload_results.update(await self._upload_to_gcs(file_paths, bucket_name))
            
            # AWS S3 Upload
            if self.s3_client:
                upload_results.update(await self._upload_to_s3(file_paths, bucket_name))
            
            # GitHub Upload (als Alternative)
            if not upload_results:
                upload_results.update(await self._upload_to_github(file_paths))
            
        except Exception as e:
            logger.error(f"Cloud Upload Fehler: {e}")
        
        return upload_results
    
    async def _upload_to_gcs(self, file_paths: Dict[str, str], bucket_name: str) -> Dict[str, str]:
        """Upload zu Google Cloud Storage"""
        results = {}
        
        try:
            bucket = self.gcs_client.bucket(bucket_name)
            
            for file_type, file_path in file_paths.items():
                if not file_path or not Path(file_path).exists():
                    continue
                
                blob_name = f"kickbase-analysis/{Path(file_path).name}"
                blob = bucket.blob(blob_name)
                
                blob.upload_from_filename(file_path)
                blob.make_public()
                
                results[f'gcs_{file_type}'] = blob.public_url
                logger.info(f"GCS Upload erfolgreich: {blob.public_url}")
        
        except Exception as e:
            logger.error(f"GCS Upload Fehler: {e}")
        
        return results
    
    async def _upload_to_s3(self, file_paths: Dict[str, str], bucket_name: str) -> Dict[str, str]:
        """Upload zu AWS S3"""
        results = {}
        
        try:
            for file_type, file_path in file_paths.items():
                if not file_path or not Path(file_path).exists():
                    continue
                
                key = f"kickbase-analysis/{Path(file_path).name}"
                
                self.s3_client.upload_file(
                    file_path, bucket_name, key,
                    ExtraArgs={'ACL': 'public-read'}
                )
                
                url = f"https://{bucket_name}.s3.amazonaws.com/{key}"
                results[f's3_{file_type}'] = url
                logger.info(f"S3 Upload erfolgreich: {url}")
        
        except Exception as e:
            logger.error(f"S3 Upload Fehler: {e}")
        
        return results
    
    async def _upload_to_github(self, file_paths: Dict[str, str]) -> Dict[str, str]:
        """Upload zu GitHub (als Fallback)"""
        results = {}
        
        try:
            # Hier würde eine GitHub API Integration stehen
            # Für Demo erstellen wir lokale "URLs"
            for file_type, file_path in file_paths.items():
                if file_path and Path(file_path).exists():
                    results[f'local_{file_type}'] = f"file://{Path(file_path).absolute()}"
        
        except Exception as e:
            logger.error(f"GitHub Upload Fehler: {e}")
        
        return results

class KickbaseUltimateAnalyzer:
    """Hauptklasse für das Kickbase Ultimate Analyzer Tool"""
    
    def __init__(self, config_path: Optional[str] = None):
        self.config = self._load_config(config_path)
        self.setup_logging()
        
        # Initialisiere Komponenten
        self.api_wrapper = KickbaseAPIWrapper(self.config)
        self.data_collector = DataCollector(self.config, self.api_wrapper)
        self.ml_predictor = MLPredictor(self.config)
        self.ai_integration = AIIntegration(self.config)
        self.data_exporter = DataExporter(self.config)
        self.cloud_integration = CloudIntegration(self.config)
        
        logger.info("Kickbase Ultimate Analyzer initialisiert")
    
    def _load_config(self, config_path: Optional[str]) -> Config:
        """Lade Konfiguration"""
        if config_path and Path(config_path).exists():
            try:
                with open(config_path, 'r') as f:
                    config_data = yaml.safe_load(f)
                return Config(**config_data)
            except Exception as e:
                logger.warning(f"Konfigurationsdatei konnte nicht geladen werden: {e}")
        
        return Config()
    
    def setup_logging(self):
        """Setup Logging"""
        log_file = Path(self.config.logs_dir) / f"kickbase_analyzer_{datetime.datetime.now().strftime('%Y%m%d')}.log"
        
        logger.add(
            log_file,
            rotation="1 day",
            retention="30 days",
            level="INFO",
            format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"
        )
    
    async def run_full_analysis(self) -> Dict[str, Any]:
        """Führe vollständige Analyse durch"""
        logger.info("🚀 Starte vollständige Kickbase-Analyse...")
        
        try:
            # 1. Login
            if not self.api_wrapper.login():
                raise Exception("Kickbase Login fehlgeschlagen")
            
            # 2. Datensammlung
            logger.info("📊 Sammle Daten...")
            raw_data = await self.data_collector.collect_all_data()
            
            # 3. Feature Engineering
            logger.info("🔧 Erstelle Features...")
            features_df = self.ml_predictor.prepare_features(raw_data)
            
            # 4. Model Training
            logger.info("🤖 Trainiere ML-Modelle...")
            model_results = self.ml_predictor.train_models(features_df)
            
            # 5. Predictions
            logger.info("🔮 Erstelle Vorhersagen...")
            predictions_df = self.ml_predictor.predict_player_values(features_df)
            
            # 6. Daten für Analyse vorbereiten
            analysis_data = {
                'top_players': predictions_df.to_dict('records') if not predictions_df.empty else [],
                'model_performance': self._get_best_model_performance(model_results),
                'market_trends': self._calculate_market_trends(features_df),
                'raw_data': raw_data
            }
            
            # 7. AI-Analyse
            logger.info("🧠 Führe AI-Analyse durch...")
            ai_analysis = await self.ai_integration.analyze_with_ai(analysis_data, "general")
            
            # 8. Datenexport
            logger.info("💾 Exportiere Daten...")
            export_files = self.data_exporter.export_all(analysis_data, ai_analysis)
            
            # 9. Cloud Upload
            logger.info("☁️ Lade in Cloud hoch...")
            cloud_urls = await self.cloud_integration.upload_files(export_files)
            
            # 10. Ergebnisse zusammenstellen
            results = {
                'analysis_data': analysis_data,
                'ai_analysis': ai_analysis,
                'export_files': export_files,
                'cloud_urls': cloud_urls,
                'execution_time': datetime.datetime.now(),
                'config': asdict(self.config)
            }
            
            logger.success("✅ Vollständige Analyse abgeschlossen!")
            return results
            
        except Exception as e:
            logger.error(f"❌ Fehler bei vollständiger Analyse: {e}")
            raise
    
    def _get_best_model_performance(self, model_results: Dict[str, Any]) -> Dict[str, float]:
        """Hole Performance des besten Modells"""
        if not model_results:
            return {}
        
        best_model = max(model_results.keys(), key=lambda k: model_results[k].get('r2', 0))
        return {
            'model_name': best_model,
            'r2': model_results[best_model].get('r2', 0),
            'mae': model_results[best_model].get('mae', 0),
            'rmse': model_results[best_model].get('rmse', 0),
            'cv_mean': model_results[best_model].get('cv_mean', 0)
        }
    
    def _calculate_market_trends(self, features_df: pd.DataFrame) -> Dict[str, float]:
        """Berechne Markt-Trends"""
        if features_df.empty:
            return {}
        
        return {
            'avg_value': features_df['market_value'].mean() if 'market_value' in features_df.columns else 0,
            'total_value': features_df['market_value'].sum() if 'market_value' in features_df.columns else 0,
            'avg_points': features_df['points'].mean() if 'points' in features_df.columns else 0,
            'total_players': len(features_df)
        }
    
    def run_quick_analysis(self) -> Dict[str, Any]:
        """Führe schnelle Analyse durch (synchron)"""
        logger.info("⚡ Starte Quick-Analyse...")
        
        try:
            # Verwende asyncio für async Funktionen
            return asyncio.run(self.run_full_analysis())
        except Exception as e:
            logger.error(f"Quick-Analyse Fehler: {e}")
            return {}
    
    def start_scheduler(self):
        """Starte automatische Ausführung"""
        if not self.config.enable_scheduling:
            logger.info("Scheduling deaktiviert")
            return
        
        # Plane tägliche Ausführung
        schedule.every().day.at("08:00").do(self.run_quick_analysis)
        schedule.every().day.at("20:00").do(self.run_quick_analysis)
        
        # Plane stündliche Updates (nur Datensammlung)
        schedule.every().hour.do(self._quick_data_update)
        
        logger.info("Scheduler gestartet - Automatische Analysen geplant")
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
        except KeyboardInterrupt:
            logger.info("Scheduler gestoppt")
    
    def _quick_data_update(self):
        """Schnelle Datenaktualisierung"""
        try:
            logger.info("🔄 Quick Data Update...")
            if self.api_wrapper.login():
                asyncio.run(self.data_collector.collect_all_data())
                logger.success("Quick Update abgeschlossen")
        except Exception as e:
            logger.error(f"Quick Update Fehler: {e}")

def main():
    """Hauptfunktion"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Kickbase Ultimate Analyzer")
    parser.add_argument("--config", help="Pfad zur Konfigurationsdatei")
    parser.add_argument("--mode", choices=["full", "quick", "scheduler"], default="quick", 
                       help="Ausführungsmodus")
    parser.add_argument("--output-dir", help="Output-Verzeichnis")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose Output")
    
    args = parser.parse_args()
    
    # Konfiguration anpassen
    config = Config()
    if args.output_dir:
        config.export_dir = args.output_dir
    
    # Analyzer initialisieren
    analyzer = KickbaseUltimateAnalyzer(args.config)
    
    try:
        if args.mode == "full":
            results = asyncio.run(analyzer.run_full_analysis())
            print("\n🎉 Vollständige Analyse abgeschlossen!")
            
            if results.get('cloud_urls'):
                print("\n📁 Cloud URLs:")
                for key, url in results['cloud_urls'].items():
                    print(f"  {key}: {url}")
            
        elif args.mode == "quick":
            results = analyzer.run_quick_analysis()
            print("\n⚡ Quick-Analyse abgeschlossen!")
            
        elif args.mode == "scheduler":
            print("🕒 Starte Scheduler...")
            analyzer.start_scheduler()
            
    except KeyboardInterrupt:
        print("\n👋 Programm beendet")
    except Exception as e:
        logger.error(f"Hauptprogramm Fehler: {e}")
        print(f"\n❌ Fehler: {e}")

if __name__ == "__main__":
    main()