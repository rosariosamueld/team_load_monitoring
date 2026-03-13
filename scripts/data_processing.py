"""
Data Processing & Validation
Loads and cleans athlete monitoring data from multiple sources.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, Tuple


class DataProcessor:
    """Load, validate, and clean athlete monitoring data."""
    
    def __init__(self, data_dir: str):
        """
        Initialize processor with data directory path.
        
        Args:
            data_dir: Path to folder containing CSV files
        """
        # Convert to Path and resolve relative to current directory or parent
        path = Path(data_dir)
        if not path.is_absolute():
            # If relative, try from current directory, then from parent directory
            if not (Path.cwd() / path).exists():
                # Try one level up (in case running from scripts directory)
                path = Path.cwd().parent / path
        
        self.data_dir = path
        self.gps_data = None
        self.rpe_data = None
        self.wellness_data = None
        self.game_data = None
        self.roster_data = None
    
    def load_all_data(self) -> Dict:
        """Load all data sources from CSV files."""
        print("Loading data files...")
        
        self.roster_data = pd.read_csv(self.data_dir / "player_roster.csv")
        self.gps_data = pd.read_csv(self.data_dir / "gps_tracking.csv")
        self.rpe_data = pd.read_csv(self.data_dir / "rpe_sessions.csv")
        self.wellness_data = pd.read_csv(self.data_dir / "wellness_daily.csv")
        self.game_data = pd.read_csv(self.data_dir / "game_performance.csv")
        
        print("[OK] Loaded {} players".format(len(self.roster_data)))
        print("[OK] Loaded {} GPS tracking records".format(len(self.gps_data)))
        print("[OK] Loaded {} RPE records".format(len(self.rpe_data)))
        print("[OK] Loaded {} wellness records".format(len(self.wellness_data)))
        print("[OK] Loaded {} game performance records".format(len(self.game_data)))
        
        return {
            "roster": self.roster_data,
            "gps": self.gps_data,
            "rpe": self.rpe_data,
            "wellness": self.wellness_data,
            "game": self.game_data,
        }
    
    def validate_data(self) -> Dict[str, list]:
        """Validate data integrity and return validation report."""
        issues = {}
        
        # Check for missing values
        print("\n[VALIDATION] Validating data integrity...")
        
        for df_name, df in [("GPS", self.gps_data), ("RPE", self.rpe_data), 
                             ("Wellness", self.wellness_data), ("Game", self.game_data)]:
            missing = df.isnull().sum().sum()
            if missing > 0:
                issues[f"{df_name}_missing"] = missing
                print(f"  [WARN] {df_name}: {missing} missing values")
        
        # Check for duplicates
        gps_dups = self.gps_data[self.gps_data.duplicated(subset=['player_id', 'date'])].shape[0]
        if gps_dups > 0:
            issues["gps_duplicates"] = gps_dups
            print(f"  [WARN] GPS: {gps_dups} duplicate records")
        
        # Check date consistency
        self.gps_data['date'] = pd.to_datetime(self.gps_data['date'])
        self.rpe_data['date'] = pd.to_datetime(self.rpe_data['date'])
        self.wellness_data['date'] = pd.to_datetime(self.wellness_data['date'])
        self.game_data['date'] = pd.to_datetime(self.game_data['date'])
        
        date_range = (self.gps_data['date'].min(), self.gps_data['date'].max())
        print(f"  [OK] Date range: {date_range[0].date()} to {date_range[1].date()}")
        
        # Check for outliers in key metrics
        gps_outliers = self._check_outliers(self.gps_data, 'distance_m', lower=3000, upper=12000)
        if len(gps_outliers) > 0:
            issues["gps_outliers"] = len(gps_outliers)
            print(f"  [WARN] GPS distance outliers: {len(gps_outliers)} records")
        
        if len(issues) == 0:
            print("  [OK] All validation checks passed!")
        
        return issues
    
    def _check_outliers(self, df: pd.DataFrame, column: str, lower: float, upper: float) -> pd.DataFrame:
        """Find values outside expected range."""
        return df[(df[column] < lower) | (df[column] > upper)]
    
    def calculate_daily_load(self) -> pd.DataFrame:
        """
        Calculate daily training load for each player.
        Uses session RPE × duration as primary load metric.
        
        Returns:
            DataFrame with date, player_id, player_name, daily_load
        """
        daily_load = self.rpe_data.groupby(['date', 'player_id', 'player_name']).agg({
            'session_rpe': 'max',
            'duration_min': 'max',
            'player_rpe': 'mean'
        }).reset_index()
        
        # Load = Session RPE × Duration / 10 (standard methodology)
        daily_load['daily_load'] = (daily_load['session_rpe'] * daily_load['duration_min']) / 10
        daily_load['date'] = pd.to_datetime(daily_load['date'])
        
        return daily_load[['date', 'player_id', 'player_name', 'daily_load', 'player_rpe']].sort_values(['player_id', 'date'])
    
    def create_training_block_summary(self, daily_load: pd.DataFrame, window_days: int = 7) -> pd.DataFrame:
        """
        Create rolling training load summary (e.g., weekly totals).
        
        Args:
            daily_load: DataFrame from calculate_daily_load()
            window_days: Rolling window size (default 7 for weekly)
        
        Returns:
            DataFrame with rolling load metrics
        """
        summary = daily_load.set_index('date').groupby('player_id').apply(
            lambda x: pd.DataFrame({
                'rolling_load': x['daily_load'].rolling(window=window_days, min_periods=1).sum(),
                'rolling_rpe': x['player_rpe'].rolling(window=window_days, min_periods=1).mean(),
            })
        ).reset_index()
        
        return summary


def main():
    """Run data processing pipeline."""
    processor = DataProcessor("data")
    
    # Load data
    data = processor.load_all_data()
    
    # Validate
    validation_issues = processor.validate_data()
    
    # Calculate metrics
    daily_load = processor.calculate_daily_load()
    print(f"\n[OK] Calculated daily load for {daily_load['player_id'].nunique()} players")
    print(daily_load.head(10))
    
    return daily_load


if __name__ == "__main__":
    main()
