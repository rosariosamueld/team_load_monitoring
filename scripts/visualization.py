"""
Visualization Module
Create charts and visual reports for monitoring data.
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
from sys import path as sys_path
import os

# Add parent directory to path to allow imports from sibling modules
sys_path.insert(0, os.path.dirname(__file__))
from data_processing import DataProcessor
from readiness_analysis import ReadinessAnalyzer


class DataVisualizer:
    """Create visualizations for load and readiness monitoring."""
    
    def __init__(self, daily_load: pd.DataFrame, wellness: pd.DataFrame, roster: pd.DataFrame):
        self.daily_load = daily_load
        self.wellness = wellness
        self.roster = roster
        self.analyzer = ReadinessAnalyzer(daily_load, wellness)
    
    def plot_weekly_load_by_player(self, output_file: str = "outputs/weekly_load.png"):
        """Create bar chart of weekly load by player."""
        latest_date = self.daily_load['date'].max()
        week_start = latest_date - timedelta(days=latest_date.weekday())
        
        week_data = self.daily_load[
            (self.daily_load['date'] >= week_start) & 
            (self.daily_load['date'] <= latest_date)
        ].groupby('player_name')['daily_load'].sum().sort_values(ascending=False)
        
        fig, ax = plt.subplots(figsize=(10, 6))
        week_data.plot(kind='bar', ax=ax, color=['#1f77b4', '#ff7f0e', '#2ca02c'])
        
        ax.set_title(f'Weekly Training Load by Player - Week of {week_start.date()}', fontsize=14, fontweight='bold')
        ax.set_xlabel('Player', fontsize=12)
        ax.set_ylabel('Weekly Load (Units)', fontsize=12)
        ax.grid(axis='y', alpha=0.3)
        plt.tight_layout()
        plt.savefig(output_file, dpi=150)
        print(f"✓ Saved: {output_file}")
    
    def plot_load_trend_by_player(self, player_id: str, output_file: str = None):
        """Create line chart of load trend for a specific player."""
        player_data = self.daily_load[self.daily_load['player_id'] == player_id].sort_values('date')
        player_name = player_data['player_name'].iloc[0]
        
        if output_file is None:
            output_file = f"outputs/load_trend_{player_id}.png"
        
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(player_data['date'], player_data['daily_load'], marker='o', linewidth=2, label='Daily Load')
        
        # Add 7-day rolling average
        rolling_avg = player_data.set_index('date')['daily_load'].rolling(window=7).mean()
        ax.plot(rolling_avg.index, rolling_avg.values, linewidth=2.5, label='7-Day Average', linestyle='--')
        
        ax.set_title(f'Training Load Trend - {player_name}', fontsize=14, fontweight='bold')
        ax.set_xlabel('Date', fontsize=12)
        ax.set_ylabel('Daily Load (Units)', fontsize=12)
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        ax.xaxis.set_major_locator(mdates.AutoDateLocator())
        plt.xticks(rotation=45)
        ax.legend()
        ax.grid(alpha=0.3)
        plt.tight_layout()
        plt.savefig(output_file, dpi=150)
        print(f"✓ Saved: {output_file}")
    
    def plot_rsi_dashboard(self, target_date: pd.Timestamp, output_file: str = "outputs/rsi_dashboard.png"):
        """Create comprehensive RSI visualization."""
        report = self.analyzer.generate_daily_readiness_report(target_date)
        
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle(f'Recovery Status Index (RSI) Dashboard - {target_date.date()}', 
                    fontsize=16, fontweight='bold')
        
        # 1. RSI by player (horizontal bar)
        ax = axes[0, 0]
        sorted_report = report.sort_values('rsi', ascending=True)
        colors = ['#d62728' if x < 60 else '#ff7f0e' if x < 80 else '#2ca02c' 
                 for x in sorted_report['rsi']]
        ax.barh(sorted_report['player_name'], sorted_report['rsi'], color=colors)
        ax.axvline(x=60, color='red', linestyle='--', linewidth=2, alpha=0.5, label='Risk Threshold')
        ax.axvline(x=80, color='orange', linestyle='--', linewidth=2, alpha=0.5, label='Caution Threshold')
        ax.set_xlabel('RSI Score')
        ax.set_title('Recovery Status Index (RSI)')
        ax.set_xlim(0, 100)
        ax.legend(fontsize=9)
        ax.grid(axis='x', alpha=0.3)
        
        # 2. ACR by player
        ax = axes[0, 1]
        sorted_acr = report.sort_values('acr', ascending=True)
        ax.barh(sorted_acr['player_name'], sorted_acr['acr'], color='steelblue')
        ax.axvline(x=0.8, color='green', linestyle='--', linewidth=2, alpha=0.5, label='Underload')
        ax.axvline(x=1.3, color='orange', linestyle='--', linewidth=2, alpha=0.5, label='Caution')
        ax.axvline(x=1.5, color='red', linestyle='--', linewidth=2, alpha=0.5, label='High Risk')
        ax.set_xlabel('Acute:Chronic Ratio')
        ax.set_title('Training Load Balance (ACR)')
        ax.legend(fontsize=8)
        ax.grid(axis='x', alpha=0.3)
        
        # 3. Recovery Score by player
        ax = axes[1, 0]
        sorted_recovery = report.sort_values('recovery_score', ascending=True)
        ax.barh(sorted_recovery['player_name'], sorted_recovery['recovery_score'], color='mediumseagreen')
        ax.set_xlabel('Recovery Score (0-100)')
        ax.set_title('Recovery Indicators (Sleep, Soreness, Fatigue)')
        ax.set_xlim(0, 100)
        ax.grid(axis='x', alpha=0.3)
        
        # 4. Risk distribution
        ax = axes[1, 1]
        risk_counts = report['risk_category'].value_counts()
        colors_pie = {'🟢 Ready': '#2ca02c', '🟡 Monitor': '#ff7f0e', '🔴 At Risk': '#d62728'}
        pie_colors = [colors_pie.get(label, 'gray') for label in risk_counts.index]
        ax.pie(risk_counts.values, labels=risk_counts.index, autopct='%1.0f%%', 
               colors=pie_colors, startangle=90)
        ax.set_title('Squad Risk Distribution')
        
        plt.tight_layout()
        plt.savefig(output_file, dpi=150)
        print(f"✓ Saved: {output_file}")


def main():
    """Generate all visualizations."""
    print("Creating visualizations...\n")
    
    processor = DataProcessor("data")
    data = processor.load_all_data()
    
    daily_load = processor.calculate_daily_load()
    viz = DataVisualizer(
        daily_load=daily_load,
        wellness=data['wellness'],
        roster=data['roster']
    )
    
    # Create visualizations
    viz.plot_weekly_load_by_player()
    
    for player_id in daily_load['player_id'].unique():
        viz.plot_load_trend_by_player(player_id)
    
    target_date = daily_load['date'].max()
    viz.plot_rsi_dashboard(target_date)
    
    print("\n[OK] All visualizations created!")


if __name__ == "__main__":
    main()
