#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kickbase Advanced Analyzer - Comprehensive Fantasy Football Analysis System
Author: Enhanced with AI Integration and Advanced ML Features
Version: 2.0
"""

import os
import sys
import json
import time
import asyncio
import datetime
import logging
import requests
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# ML Libraries
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import mean_squared_error, r2_score
import xgboost as xgb
from xgboost import XGBRegressor
import joblib

# Visualization
import matplotlib.pyplot as plt
import seaborn as sns
plt.style.use('dark_background')

# Rich Console for beautiful output
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Prompt, Confirm
from rich.text import Text
from rich.layout import Layout
from rich.live import Live

# AI Integration
try:
    import openai
    from openai import OpenAI
    AI_AVAILABLE = True
except ImportError:
    AI_AVAILABLE = False
    print("⚠️  OpenAI not available. AI features disabled.")

# Configuration
console = Console()

@dataclass
class PlayerData:
    """Data structure for player information"""
    id: str
    name: str
    team: str
    position: str
    market_value: float
    points_total: int
    points_avg: float
    games_played: int
    goals: int
    assists: int
    yellow_cards: int
    red_cards: int
    injuries: List[str]
    form_trend: float
    value_history: List[float]
    predicted_value: Optional[float] = None
    confidence_score: Optional[float] = None
    risk_score: Optional[float] = None
    recommendation: Optional[str] = None

class KickbaseAPIClient:
    """Enhanced Kickbase API Client with error handling and rate limiting"""
    
    def __init__(self, email: str, password: str):
        self.email = email
        self.password = password
        self.session = requests.Session()
        self.base_url = "https://api.kickbase.com"
        self.token = None
        self.rate_limit_delay = 1.0  # seconds between requests
        
    def login(self) -> bool:
        """Login to Kickbase API"""
        try:
            login_data = {
                "email": self.email,
                "password": self.password
            }
            
            response = self.session.post(
                f"{self.base_url}/auth/login",
                json=login_data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                self.token = data.get("token")
                self.session.headers.update({"Authorization": f"Bearer {self.token}"})
                console.print("✅ Login successful", style="green")
                return True
            else:
                console.print(f"❌ Login failed: {response.status_code}", style="red")
                return False
                
        except Exception as e:
            console.print(f"❌ Login error: {str(e)}", style="red")
            return False
    
    def get_leagues(self) -> List[Dict]:
        """Get user's leagues"""
        try:
            response = self.session.get(f"{self.base_url}/leagues")
            time.sleep(self.rate_limit_delay)
            return response.json() if response.status_code == 200 else []
        except Exception as e:
            console.print(f"❌ Error fetching leagues: {str(e)}", style="red")
            return []
    
    def get_players(self, league_id: str) -> List[PlayerData]:
        """Get all players in a league with detailed stats"""
        players = []
        
        try:
            # Get league players
            response = self.session.get(f"{self.base_url}/leagues/{league_id}/players")
            time.sleep(self.rate_limit_delay)
            
            if response.status_code != 200:
                console.print(f"❌ Error fetching players: {response.status_code}", style="red")
                return players
            
            players_data = response.json()
            
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console
            ) as progress:
                task = progress.add_task("Fetching player data...", total=len(players_data))
                
                for player in players_data:
                    try:
                        # Get detailed player stats
                        player_id = player.get("id")
                        stats_response = self.session.get(f"{self.base_url}/players/{player_id}/stats")
                        time.sleep(self.rate_limit_delay)
                        
                        if stats_response.status_code == 200:
                            stats = stats_response.json()
                            
                            # Get market value history
                            history_response = self.session.get(f"{self.base_url}/players/{player_id}/market-value-history")
                            time.sleep(self.rate_limit_delay)
                            
                            value_history = []
                            if history_response.status_code == 200:
                                history_data = history_response.json()
                                value_history = [h.get("value", 0) for h in history_data.get("history", [])]
                            
                            player_data = PlayerData(
                                id=player_id,
                                name=f"{player.get('firstName', '')} {player.get('lastName', '')}",
                                team=player.get("team", {}).get("name", "Unknown"),
                                position=player.get("position", "Unknown"),
                                market_value=player.get("marketValue", 0),
                                points_total=stats.get("totalPoints", 0),
                                points_avg=stats.get("averagePoints", 0),
                                games_played=stats.get("matchCount", 0),
                                goals=stats.get("goals", 0),
                                assists=stats.get("assists", 0),
                                yellow_cards=stats.get("yellowCards", 0),
                                red_cards=stats.get("redCards", 0),
                                injuries=stats.get("injuries", []),
                                form_trend=self._calculate_form_trend(stats),
                                value_history=value_history
                            )
                            
                            players.append(player_data)
                        
                        progress.advance(task)
                        
                    except Exception as e:
                        console.print(f"⚠️  Error processing player {player.get('id')}: {str(e)}", style="yellow")
                        continue
            
            console.print(f"✅ Fetched {len(players)} players", style="green")
            return players
            
        except Exception as e:
            console.print(f"❌ Error fetching players: {str(e)}", style="red")
            return players
    
    def _calculate_form_trend(self, stats: Dict) -> float:
        """Calculate player form trend based on recent performance"""
        try:
            recent_points = stats.get("recentPoints", [])
            if len(recent_points) >= 5:
                recent_avg = np.mean(recent_points[-5:])
                overall_avg = stats.get("averagePoints", 0)
                return recent_avg - overall_avg
            return 0.0
        except:
            return 0.0

class MLPredictor:
    """Advanced ML model for player value predictions"""
    
    def __init__(self):
        self.models = {}
        self.scaler = StandardScaler()
        self.label_encoders = {}
        self.feature_columns = [
            'points_total', 'points_avg', 'games_played', 'goals', 'assists',
            'yellow_cards', 'red_cards', 'form_trend', 'value_change_5d',
            'value_change_10d', 'value_change_30d', 'injury_risk'
        ]
        
    def prepare_features(self, players: List[PlayerData]) -> pd.DataFrame:
        """Prepare features for ML model"""
        df = pd.DataFrame([asdict(player) for player in players])
        
        # Calculate additional features
        df['value_change_5d'] = df['value_history'].apply(
            lambda x: np.diff(x[-5:]).sum() if len(x) >= 5 else 0
        )
        df['value_change_10d'] = df['value_history'].apply(
            lambda x: np.diff(x[-10:]).sum() if len(x) >= 10 else 0
        )
        df['value_change_30d'] = df['value_history'].apply(
            lambda x: np.diff(x[-30:]).sum() if len(x) >= 30 else 0
        )
        
        # Injury risk calculation
        df['injury_risk'] = df['injuries'].apply(
            lambda x: len(x) * 0.1 if x else 0
        )
        
        # Position encoding
        if 'position' not in self.label_encoders:
            self.label_encoders['position'] = LabelEncoder()
            df['position_encoded'] = self.label_encoders['position'].fit_transform(df['position'])
        else:
            df['position_encoded'] = self.label_encoders['position'].transform(df['position'])
        
        # Select features
        feature_df = df[self.feature_columns + ['position_encoded']].fillna(0)
        
        return feature_df, df
    
    def train_models(self, players: List[PlayerData]):
        """Train multiple ML models"""
        feature_df, full_df = self.prepare_features(players)
        target = full_df['market_value']
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            feature_df, target, test_size=0.2, random_state=42
        )
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Train multiple models
        models = {
            'xgboost': XGBRegressor(n_estimators=100, learning_rate=0.1, random_state=42),
            'random_forest': RandomForestRegressor(n_estimators=100, random_state=42),
            'gradient_boosting': GradientBoostingRegressor(n_estimators=100, random_state=42)
        }
        
        console.print("🤖 Training ML models...", style="blue")
        
        for name, model in models.items():
            try:
                model.fit(X_train_scaled, y_train)
                y_pred = model.predict(X_test_scaled)
                mse = mean_squared_error(y_test, y_pred)
                r2 = r2_score(y_test, y_pred)
                
                console.print(f"✅ {name}: MSE={mse:.2f}, R²={r2:.3f}", style="green")
                self.models[name] = model
                
            except Exception as e:
                console.print(f"❌ Error training {name}: {str(e)}", style="red")
    
    def predict_values(self, players: List[PlayerData]) -> List[PlayerData]:
        """Predict market values for all players"""
        if not self.models:
            console.print("⚠️  No trained models available", style="yellow")
            return players
        
        feature_df, full_df = self.prepare_features(players)
        X_scaled = self.scaler.transform(feature_df)
        
        # Ensemble prediction
        predictions = {}
        for name, model in self.models.items():
            predictions[name] = model.predict(X_scaled)
        
        # Average predictions
        ensemble_pred = np.mean(list(predictions.values()), axis=0)
        
        # Update players with predictions
        for i, player in enumerate(players):
            player.predicted_value = ensemble_pred[i]
            player.confidence_score = self._calculate_confidence(predictions, i)
            player.risk_score = self._calculate_risk_score(player)
            player.recommendation = self._generate_recommendation(player)
        
        return players
    
    def _calculate_confidence(self, predictions: Dict, index: int) -> float:
        """Calculate confidence score based on model agreement"""
        values = [pred[index] for pred in predictions.values()]
        return 1.0 - (np.std(values) / np.mean(values)) if np.mean(values) > 0 else 0.0
    
    def _calculate_risk_score(self, player: PlayerData) -> float:
        """Calculate risk score for player"""
        risk = 0.0
        
        # Injury risk
        if player.injuries:
            risk += len(player.injuries) * 0.2
        
        # Form risk
        if player.form_trend < -1.0:
            risk += 0.3
        
        # Age/experience risk (simplified)
        if player.games_played < 5:
            risk += 0.2
        
        return min(risk, 1.0)
    
    def _generate_recommendation(self, player: PlayerData) -> str:
        """Generate trading recommendation"""
        if not player.predicted_value:
            return "HOLD"
        
        value_change = player.predicted_value - player.market_value
        change_percent = (value_change / player.market_value) * 100 if player.market_value > 0 else 0
        
        if change_percent > 10 and player.risk_score < 0.5:
            return "STRONG_BUY"
        elif change_percent > 5 and player.risk_score < 0.7:
            return "BUY"
        elif change_percent < -10:
            return "SELL"
        elif change_percent < -5:
            return "WEAK_SELL"
        else:
            return "HOLD"

class AIAnalyzer:
    """AI-powered analysis using OpenAI/GPT"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key
        self.client = None
        
        if api_key and AI_AVAILABLE:
            try:
                self.client = OpenAI(api_key=api_key)
                console.print("🤖 AI Analyzer initialized", style="green")
            except Exception as e:
                console.print(f"❌ AI initialization failed: {str(e)}", style="red")
    
    def analyze_player(self, player: PlayerData) -> str:
        """Generate AI analysis for a player"""
        if not self.client:
            return "AI analysis not available"
        
        try:
            prompt = f"""
            Analyze this football player for fantasy football trading:
            
            Name: {player.name}
            Team: {player.team}
            Position: {player.position}
            Current Market Value: {player.market_value}
            Total Points: {player.points_total}
            Average Points: {player.points_avg}
            Games Played: {player.games_played}
            Goals: {player.goals}
            Assists: {player.assists}
            Form Trend: {player.form_trend}
            Injuries: {player.injuries}
            Predicted Value: {player.predicted_value}
            Risk Score: {player.risk_score}
            
            Provide a brief analysis and trading recommendation.
            """
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=200
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"AI analysis error: {str(e)}"
    
    def generate_market_report(self, players: List[PlayerData]) -> str:
        """Generate comprehensive market report"""
        if not self.client:
            return "AI report not available"
        
        try:
            # Prepare market summary
            total_players = len(players)
            avg_value = np.mean([p.market_value for p in players])
            top_gainers = sorted(players, key=lambda x: x.predicted_value - x.market_value, reverse=True)[:5]
            top_losers = sorted(players, key=lambda x: x.market_value - x.predicted_value, reverse=True)[:5]
            
            prompt = f"""
            Generate a comprehensive fantasy football market report:
            
            Market Overview:
            - Total Players: {total_players}
            - Average Market Value: {avg_value:.2f}
            
            Top 5 Potential Gainers:
            {chr(10).join([f"- {p.name}: {p.market_value} → {p.predicted_value:.2f}" for p in top_gainers])}
            
            Top 5 Potential Losers:
            {chr(10).join([f"- {p.name}: {p.market_value} → {p.predicted_value:.2f}" for p in top_losers])}
            
            Provide insights and trading strategies.
            """
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"AI report error: {str(e)}"

class DataExporter:
    """Handle data export to various formats"""
    
    def __init__(self, output_dir: str = "kickbase_data"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
    
    def export_json(self, players: List[PlayerData], filename: str = None):
        """Export to JSON format"""
        if not filename:
            filename = f"kickbase_data_{datetime.date.today()}.json"
        
        filepath = self.output_dir / filename
        
        data = {
            "export_date": datetime.datetime.now().isoformat(),
            "total_players": len(players),
            "players": [asdict(player) for player in players]
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        console.print(f"✅ Exported JSON: {filepath}", style="green")
        return str(filepath)
    
    def export_csv(self, players: List[PlayerData], filename: str = None):
        """Export to CSV format"""
        if not filename:
            filename = f"kickbase_predictions_{datetime.date.today()}.csv"
        
        filepath = self.output_dir / filename
        
        df = pd.DataFrame([asdict(player) for player in players])
        df.to_csv(filepath, index=False, encoding='utf-8')
        
        console.print(f"✅ Exported CSV: {filepath}", style="green")
        return str(filepath)
    
    def export_report(self, players: List[PlayerData], ai_report: str = "", filename: str = None):
        """Export comprehensive report"""
        if not filename:
            filename = f"kickbase_report_{datetime.date.today()}.md"
        
        filepath = self.output_dir / filename
        
        # Create markdown report
        report = f"""# Kickbase Market Analysis Report
Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Market Overview
- Total Players Analyzed: {len(players)}
- Average Market Value: {np.mean([p.market_value for p in players]):.2f}
- Total Market Value: {sum([p.market_value for p in players]):.2f}

## Top Recommendations

### Strong Buy Candidates
"""
        
        strong_buys = [p for p in players if p.recommendation == "STRONG_BUY"]
        for player in sorted(strong_buys, key=lambda x: x.predicted_value - x.market_value, reverse=True)[:10]:
            report += f"- **{player.name}** ({player.team}): {player.market_value} → {player.predicted_value:.2f} (Risk: {player.risk_score:.2f})\n"
        
        report += "\n### Sell Candidates\n"
        sells = [p for p in players if p.recommendation in ["SELL", "WEAK_SELL"]]
        for player in sorted(sells, key=lambda x: x.market_value - x.predicted_value, reverse=True)[:10]:
            report += f"- **{player.name}** ({player.team}): {player.market_value} → {player.predicted_value:.2f} (Risk: {player.risk_score:.2f})\n"
        
        if ai_report:
            report += f"\n## AI Analysis\n{ai_report}\n"
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(report)
        
        console.print(f"✅ Exported Report: {filepath}", style="green")
        return str(filepath)

class KickbaseAnalyzer:
    """Main analyzer class that orchestrates everything"""
    
    def __init__(self, email: str, password: str, ai_api_key: str = None):
        self.api_client = KickbaseAPIClient(email, password)
        self.ml_predictor = MLPredictor()
        self.ai_analyzer = AIAnalyzer(ai_api_key)
        self.exporter = DataExporter()
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('kickbase_analyzer.log'),
                logging.StreamHandler()
            ]
        )
    
    def run_analysis(self, league_id: str = None) -> List[PlayerData]:
        """Run complete analysis pipeline"""
        console.print(Panel.fit("🚀 Starting Kickbase Analysis", style="blue"))
        
        # Login
        if not self.api_client.login():
            console.print("❌ Failed to login", style="red")
            return []
        
        # Get leagues
        leagues = self.api_client.get_leagues()
        if not leagues:
            console.print("❌ No leagues found", style="red")
            return []
        
        # Select league
        if not league_id:
            league_id = leagues[0].get("id") if leagues else None
        
        if not league_id:
            console.print("❌ No league ID provided", style="red")
            return []
        
        console.print(f"📊 Analyzing league: {league_id}", style="blue")
        
        # Fetch players
        players = self.api_client.get_players(league_id)
        if not players:
            console.print("❌ No players found", style="red")
            return []
        
        # Train ML models
        self.ml_predictor.train_models(players)
        
        # Make predictions
        players_with_predictions = self.ml_predictor.predict_values(players)
        
        # Generate AI analysis
        ai_report = ""
        if self.ai_analyzer.client:
            ai_report = self.ai_analyzer.generate_market_report(players_with_predictions)
        
        # Export data
        self.exporter.export_json(players_with_predictions)
        self.exporter.export_csv(players_with_predictions)
        self.exporter.export_report(players_with_predictions, ai_report)
        
        console.print("✅ Analysis complete!", style="green")
        return players_with_predictions
    
    def display_results(self, players: List[PlayerData]):
        """Display results in beautiful tables"""
        if not players:
            return
        
        # Top recommendations table
        table = Table(title="Top Trading Recommendations")
        table.add_column("Player", style="cyan")
        table.add_column("Team", style="magenta")
        table.add_column("Current Value", style="green")
        table.add_column("Predicted Value", style="yellow")
        table.add_column("Change %", style="blue")
        table.add_column("Recommendation", style="red")
        table.add_column("Risk Score", style="white")
        
        # Sort by potential gain
        sorted_players = sorted(
            players, 
            key=lambda x: (x.predicted_value - x.market_value) / x.market_value if x.market_value > 0 else 0,
            reverse=True
        )
        
        for player in sorted_players[:15]:
            change_percent = ((player.predicted_value - player.market_value) / player.market_value * 100) if player.market_value > 0 else 0
            table.add_row(
                player.name,
                player.team,
                f"{player.market_value:.2f}",
                f"{player.predicted_value:.2f}" if player.predicted_value else "N/A",
                f"{change_percent:+.1f}%",
                player.recommendation or "HOLD",
                f"{player.risk_score:.2f}" if player.risk_score else "N/A"
            )
        
        console.print(table)

def main():
    """Main entry point"""
    console.print(Panel.fit("🎯 Kickbase Advanced Analyzer v2.0", style="bold blue"))
    
    # Get credentials
    email = Prompt.ask("Enter your Kickbase email")
    password = Prompt.ask("Enter your Kickbase password", password=True)
    
    # Optional AI API key
    ai_key = Prompt.ask("Enter OpenAI API key (optional)", default="")
    
    # Initialize analyzer
    analyzer = KickbaseAnalyzer(email, password, ai_key if ai_key else None)
    
    # Run analysis
    players = analyzer.run_analysis()
    
    if players:
        analyzer.display_results(players)
        
        # Ask for additional analysis
        if Confirm.ask("Would you like detailed AI analysis for specific players?"):
            for player in players[:5]:  # Analyze top 5
                analysis = analyzer.ai_analyzer.analyze_player(player)
                console.print(Panel(analysis, title=f"AI Analysis: {player.name}", style="green"))

if __name__ == "__main__":
    main()