import os
import json
import datetime
import argparse
from typing import List, Dict, Any, Optional

import numpy as np
import pandas as pd
from tqdm import tqdm

# ML imports
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor

# Kickbase wrapper (unofficial)
try:
    from kickbase_api.kickbase import Kickbase
    from kickbase_api.exceptions import KickbaseException
except ImportError:  # Graceful fallback if wrapper missing
    Kickbase = None  # type: ignore
    KickbaseException = Exception  # type: ignore

# Optional: use OpenAI / ChatGPT summarisation if API key provided
try:
    import openai
except ImportError:
    openai = None  # type: ignore

###############################################################################
# Utility helpers
###############################################################################

def ensure_dir(path: str) -> None:
    """Ensure a directory exists."""
    os.makedirs(path, exist_ok=True)


def ts() -> str:
    """Return current date as YYYY-MM-DD string."""
    return datetime.date.today().isoformat()


def debug(msg: str) -> None:
    print(f"[KickbaseAnalytics] {msg}")

###############################################################################
# Core class
###############################################################################

class KickbaseAnalytics:
    """Wrapper class bundling all functionality."""

    DEFAULT_EXPORT_DIR = "kickbase_data"

    def __init__(
        self,
        email: str,
        password: str,
        league_id: Optional[str] = None,
        export_dir: str = DEFAULT_EXPORT_DIR,
        model_type: str = "xgboost",
        openai_api_key: Optional[str] = None,
    ) -> None:
        self.email = email
        self.password = password
        self.league_id = league_id
        self.export_dir = export_dir
        self.model_type = model_type.lower()
        self.kb = None  # Will hold Kickbase instance

        ensure_dir(self.export_dir)

        # Configure OpenAI if requested
        if openai_api_key and openai:
            openai.api_key = openai_api_key
            debug("OpenAI integration enabled.")

    # ---------------------------------------------------------------------
    # Login
    # ---------------------------------------------------------------------
    def login(self) -> None:
        if Kickbase is None:
            raise RuntimeError(
                "kickbase_api library not found. Please install with `pip install kickbase_api`."
            )
        try:
            self.kb = Kickbase()
            user, leagues = self.kb.login(self.email, self.password)
            debug(f"Logged in as {user.name} (User ID: {user.id})")
            # Determine league
            if self.league_id:
                league = next((l for l in leagues if l.id == self.league_id), None)
            else:
                league = leagues[0] if leagues else None
            if league is None:
                raise RuntimeError("Unable to find specified league.")
            self.league_id = league.id
            self.league = league
            debug(f"Using league '{league.name}' (ID: {league.id})")
        except KickbaseException as e:
            raise RuntimeError(f"Kickbase login failed: {e}")

    # ---------------------------------------------------------------------
    # Data collection
    # ---------------------------------------------------------------------
    def fetch_player_data(self) -> List[Dict[str, Any]]:
        if self.kb is None:
            raise RuntimeError("Not logged in. Call login() first.")

        debug("Fetching player list...")
        players = self.kb.league_players(self.league)
        result: List[Dict[str, Any]] = []
        for player in tqdm(players, desc="Players"):
            try:
                stats = self.kb.player_stats(player)
                market_value = player.market_value
                trend = player.market_value_trend
                history = self.kb.player_market_value_history(player) or []

                result.append(
                    {
                        "id": player.id,
                        "name": f"{player.first_name} {player.last_name}",
                        "team": player.team_id,
                        "position": player.position,
                        "market_value": market_value,
                        "trend": trend,
                        "points_total": getattr(stats, "total_points", 0),
                        "points_avg": getattr(stats, "average_points", 0),
                        "games_played": getattr(stats, "match_count", 0),
                        "goals": getattr(stats, "goals", 0),
                        "assists": getattr(stats, "assists", 0),
                        "value_history": [h["v"] for h in history],
                    }
                )
            except KickbaseException as e:
                debug(f"Skipping player {player.id} due to API error: {e}")
        debug(f"Collected data for {len(result)} players.")
        return result

    # ---------------------------------------------------------------------
    # Analysis and prediction
    # ---------------------------------------------------------------------
    def analyze_and_predict(self, players: List[Dict[str, Any]]) -> pd.DataFrame:
        debug("Running analysis & prediction...")
        df = pd.DataFrame(players)

        # Feature engineering
        df["value_change_last_5"] = df["value_history"].apply(
            lambda x: np.diff(x[-5:]).sum() if len(x) >= 5 else 0
        )
        df["predicted_trend"] = (
            df["points_avg"] * 0.5
            + df["goals"] * 2
            + df["assists"] * 1.5
            - df["games_played"] * 0.1
        )

        feature_cols = [
            "points_total",
            "points_avg",
            "games_played",
            "goals",
            "assists",
            "value_change_last_5",
        ]
        target_col = "market_value"

        X = df[feature_cols].fillna(0)
        y = df[target_col].fillna(0)

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        # Select model
        if self.model_type == "randomforest":
            model = RandomForestRegressor(n_estimators=200, random_state=42)
        else:  # default to XGBoost
            model = XGBRegressor(n_estimators=300, learning_rate=0.05, random_state=42)

        model.fit(X_train, y_train)
        df["predicted_value"] = model.predict(X)
        df["predicted_change"] = df["predicted_value"] - df["market_value"]

        # Ranking
        df_sorted = df.sort_values(by="predicted_change", ascending=False)

        debug("Analysis complete.")
        return df_sorted

    # ---------------------------------------------------------------------
    # Export
    # ---------------------------------------------------------------------
    def export(self, raw_data: List[Dict[str, Any]], predictions: pd.DataFrame) -> None:
        json_path = os.path.join(self.export_dir, f"kickbase_data_{ts()}.json")
        csv_path = os.path.join(self.export_dir, f"kickbase_predictions_{ts()}.csv")

        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(raw_data, f, indent=4, ensure_ascii=False)
        predictions.to_csv(csv_path, index=False)

        debug(f"Exported data to \n - {json_path}\n - {csv_path}")

    # ---------------------------------------------------------------------
    # Optional: AI summary
    # ---------------------------------------------------------------------
    def summarise_top_picks(self, df: pd.DataFrame, top_n: int = 10) -> Optional[str]:
        if openai is None or not openai.api_key:
            debug("OpenAI not configured; skipping summary generation.")
            return None

        top_players = df.head(top_n)[
            ["name", "market_value", "predicted_value", "predicted_change"]
        ].to_dict(orient="records")

        prompt = (
            "You are a fantasy football assistant. Based on the following player predictions, "
            "suggest which players are the best bargains and why.\n\n" + json.dumps(top_players, indent=2)
        )
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
            )
            summary = response.choices[0].message["content"].strip()
            return summary
        except Exception as e:
            debug(f"OpenAI request failed: {e}")
            return None

###############################################################################
# CLI entrypoint
###############################################################################

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Kickbase Analytics & Prediction Toolkit",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--email", required=False, help="Kickbase account email")
    parser.add_argument("--password", required=False, help="Kickbase account password")
    parser.add_argument("--league-id", help="League ID (optional; default selects first league)")
    parser.add_argument("--export-dir", default=KickbaseAnalytics.DEFAULT_EXPORT_DIR)
    parser.add_argument(
        "--model", choices=["xgboost", "randomforest"], default="xgboost", help="ML model"
    )
    parser.add_argument(
        "--openai-key",
        dest="openai_api_key",
        default=os.getenv("OPENAI_API_KEY"),
        help="OpenAI API key for summary generation",
    )
    parser.add_argument(
        "--top", type=int, default=10, help="Number of top players to include in summary"
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    # Fallback to env vars for credentials
    email = args.email or os.getenv("KICKBASE_EMAIL")
    password = args.password or os.getenv("KICKBASE_PASSWORD")

    if not email or not password:
        print("Error: Provide Kickbase credentials via CLI or environment variables.")
        exit(1)

    analytics = KickbaseAnalytics(
        email=email,
        password=password,
        league_id=args.league_id,
        export_dir=args.export_dir,
        model_type=args.model,
        openai_api_key=args.openai_api_key,
    )

    analytics.login()
    players = analytics.fetch_player_data()
    predictions = analytics.analyze_and_predict(players)
    analytics.export(players, predictions)

    summary = analytics.summarise_top_picks(predictions, top_n=args.top)
    if summary:
        print("\n===== AI SUMMARY =====\n")
        print(summary)

    print("\nAll done. Happy team managing!")


if __name__ == "__main__":
    main()