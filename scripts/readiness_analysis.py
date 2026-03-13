"""
Readiness Analysis
Calculate Recovery Status Index (RSI) and identify players at risk.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict
from sys import path as sys_path
import os

# Add parent directory to path to allow imports from sibling modules
sys_path.insert(0, os.path.dirname(__file__))
from data_processing import DataProcessor


class ReadinessAnalyzer:
    """Calculate recovery and readiness metrics."""
    
    def __init__(self, daily_load: pd.DataFrame, wellness: pd.DataFrame):
        """
        Initialize analyzer.
        
        Args:
            daily_load: DataFrame from DataProcessor.calculate_daily_load()
            wellness: Wellness survey data (sleep, soreness, etc.)
        """
        self.daily_load = daily_load
        self.wellness = wellness
        self.wellness['date'] = pd.to_datetime(self.wellness['date'])
    
    def calculate_acute_chronic_ratio(self, player_id: str, date: pd.Timestamp, 
                                     acute_days: int = 7, chronic_days: int = 28) -> float:
        """
        Calculate Acute:Chronic Workload Ratio (Research-backed injury predictor).
        
        ACR = Average load (past 7 days) / Average load (past 28 days)
        
        Interpretation:
        - <0.8: Underload (detraining risk)
        - 0.8-1.3: Safe zone
        - 1.3-1.5: Moderate risk
        - >1.5: High injury risk
        
        Args:
            player_id: Player identifier
            date: Target date
            acute_days: Days in acute window (default 7)
            chronic_days: Days in chronic window (default 28)
        
        Returns:
            ACR value (float)
        """
        player_load = self.daily_load[self.daily_load['player_id'] == player_id].copy()
        player_load = player_load.set_index('date').sort_index()
        
        acute_start = date - timedelta(days=acute_days)
        chronic_start = date - timedelta(days=chronic_days)
        
        acute = player_load[(player_load.index > acute_start) & (player_load.index <= date)]['daily_load']
        chronic = player_load[(player_load.index > chronic_start) & (player_load.index <= date)]['daily_load']
        
        acute_avg = acute.mean() if len(acute) > 0 else 0
        chronic_avg = chronic.mean() if len(chronic) > 0 else 1  # Avoid division by zero
        
        acr = acute_avg / chronic_avg if chronic_avg > 0 else 0
        return round(acr, 2)
    
    def calculate_recovery_score(self, player_id: str, date: pd.Timestamp, 
                                window_days: int = 7) -> float:
        """
        Calculate Recovery Score from wellness data.
        
        Composite of: sleep quality, sleep duration, muscle soreness, fatigue.
        Score ranges 0-100 (higher = better recovery).
        
        Args:
            player_id: Player identifier
            date: Target date
            window_days: Days to include in average
        
        Returns:
            Recovery score 0-100 (float)
        """
        start_date = date - timedelta(days=window_days)
        player_wellness = self.wellness[
            (self.wellness['player_id'] == player_id) & 
            (self.wellness['date'] > start_date) & 
            (self.wellness['date'] <= date)
        ]
        
        if len(player_wellness) == 0:
            return 50  # Default if no data
        
        # Normalize metrics to 0-100 scale
        sleep_score = (player_wellness['sleep_quality'].mean() / 10) * 100  # 0-10 → 0-100
        sleep_duration = np.clip((player_wellness['sleep_hours'].mean() / 8.5) * 100, 0, 100)  # Target 8.5h
        soreness_score = 100 - (player_wellness['muscle_soreness'].mean() / 10) * 100  # Inverse (lower soreness is better)
        fatigue_score = 100 - (player_wellness['fatigue_level'].mean() / 10) * 100  # Inverse
        
        # Weighted average
        recovery_score = (
            sleep_score * 0.35 +
            sleep_duration * 0.25 +
            soreness_score * 0.25 +
            fatigue_score * 0.15
        )
        
        return round(np.clip(recovery_score, 0, 100), 1)
    
    def calculate_rsi(self, player_id: str, date: pd.Timestamp) -> Dict:
        """
        Calculate Recovery Status Index (RSI).
        
        RSI = 100 - [(ACR/2) + ((100 - Recovery Score)/2)]
        
        Ranges:
        - 🟢 >80: Ready for full training
        - 🟡 60-80: Monitor; consider load management
        - 🔴 <60: High risk; recommend load reduction
        
        Args:
            player_id: Player identifier
            date: Target date
        
        Returns:
            Dictionary with RSI, ACR, recovery score, and risk category
        """
        acr = self.calculate_acute_chronic_ratio(player_id, date)
        recovery_score = self.calculate_recovery_score(player_id, date)
        
        # RSI formula
        rsi = 100 - ((acr / 2) + ((100 - recovery_score) / 2))
        rsi = round(np.clip(rsi, 0, 100), 1)
        
        # Risk category
        if rsi > 80:
            risk_category = "[GREEN] Ready"
        elif rsi >= 60:
            risk_category = "[YELLOW] Monitor"
        else:
            risk_category = "[RED] At Risk"
        
        return {
            'player_id': player_id,
            'date': date,
            'rsi': rsi,
            'acr': acr,
            'recovery_score': recovery_score,
            'risk_category': risk_category,
        }
    
    def generate_daily_readiness_report(self, target_date: pd.Timestamp) -> pd.DataFrame:
        """
        Generate daily readiness report for all players.
        
        Args:
            target_date: Date to analyze
        
        Returns:
            DataFrame with RSI for all players
        """
        players = self.daily_load['player_id'].unique()
        records = []
        
        for player_id in players:
            rsi_data = self.calculate_rsi(player_id, target_date)
            player_name = self.daily_load[self.daily_load['player_id'] == player_id]['player_name'].iloc[0]
            rsi_data['player_name'] = player_name
            records.append(rsi_data)
        
        report = pd.DataFrame(records)
        return report.sort_values('rsi')
    
    def identify_at_risk_players(self, target_date: pd.Timestamp, threshold: float = 60) -> pd.DataFrame:
        """Find players below readiness threshold."""
        report = self.generate_daily_readiness_report(target_date)
        at_risk = report[report['rsi'] < threshold]
        return at_risk


def main():
    """Run readiness analysis."""
    print("Loading data for readiness analysis...\n")
    
    processor = DataProcessor("data")
    data = processor.load_all_data()
    
    daily_load = processor.calculate_daily_load()
    wellness = processor.load_all_data()['wellness']
    
    analyzer = ReadinessAnalyzer(daily_load, wellness)
    
    # Get latest date in data
    latest_date = daily_load['date'].max()
    print(f"Generating readiness report for {latest_date.date()}\n")
    
    report = analyzer.generate_daily_readiness_report(latest_date)
    print("=" * 80)
    print(f"DAILY READINESS REPORT - {latest_date.date()}")
    print("=" * 80)
    print(report.to_string(index=False))
    print()
    
    # Highlight at-risk players
    at_risk = analyzer.identify_at_risk_players(latest_date, threshold=60)
    if len(at_risk) > 0:
        print("\n[WARNING] AT-RISK PLAYERS (RSI < 60):")
        print(at_risk[['player_name', 'rsi', 'acr', 'recovery_score']].to_string(index=False))
    else:
        print("\n[OK] All players within acceptable readiness range")
    
    return report


if __name__ == "__main__":
    main()
