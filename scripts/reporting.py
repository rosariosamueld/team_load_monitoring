"""
Reporting Module
Generate tailored reports for different stakeholder groups.
"""

import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path
from sys import path as sys_path
import os

# Add parent directory to path to allow imports from sibling modules
sys_path.insert(0, os.path.dirname(__file__))
from data_processing import DataProcessor
from readiness_analysis import ReadinessAnalyzer


class ReportGenerator:
    """Generate stakeholder-specific reports."""
    
    def __init__(self, daily_load: pd.DataFrame, wellness: pd.DataFrame, 
                 gps: pd.DataFrame, game: pd.DataFrame, roster: pd.DataFrame):
        """Initialize report generator."""
        self.daily_load = daily_load
        self.wellness = wellness
        self.gps = gps
        self.game = game
        self.roster = roster
        self.analyzer = ReadinessAnalyzer(daily_load, wellness)
    
    def coaching_staff_dashboard(self, target_date: pd.Timestamp) -> str:
        """
        Generate weekly dashboard for coaching staff.
        Focused on: readiness, training load, and actionable recommendations.
        """
        report = self.analyzer.generate_daily_readiness_report(target_date)
        
        # Weekly load aggregation
        week_start = target_date - timedelta(days=target_date.weekday())
        week_load = self.daily_load[
            (self.daily_load['date'] >= week_start) & 
            (self.daily_load['date'] <= target_date)
        ].groupby('player_id').agg({
            'daily_load': 'sum',
            'player_rpe': 'mean',
            'player_name': 'first'
        }).reset_index()
        week_load = week_load.rename(columns={
            'daily_load': 'weekly_load',
            'player_rpe': 'avg_rpe'
        })
        
        merged = report.merge(week_load, on=['player_id', 'player_name'])
        
        output = []
        output.append("=" * 90)
        output.append(f"COACHING STAFF DASHBOARD - Week of {week_start.date()}")
        output.append("=" * 90)
        output.append("")
        output.append("PLAYER READINESS SUMMARY")
        output.append("-" * 90)
        output.append(merged[['player_name', 'rsi', 'risk_category', 'weekly_load', 'avg_rpe']].to_string(index=False))
        output.append("")
        
        # Recommendations
        output.append("COACHING RECOMMENDATIONS")
        output.append("-" * 90)
        for _, row in merged.iterrows():
            if row['rsi'] > 80:
                rec = f"[OK] {row['player_name']}: Full training availability. Load increasing appropriately."
            elif row['rsi'] >= 60:
                rec = f"[MONITOR] {row['player_name']}: Monitor closely. Consider reducing intensity if fatigue increases."
            else:
                rec = f"[AT-RISK] {row['player_name']}: Recommend reduced load. Prioritize recovery (consider DNP-rest or limited minutes)."
            output.append(rec)
        
        output.append("")
        output.append("SQUAD-LEVEL INSIGHTS")
        output.append("-" * 90)
        avg_rsi = merged['rsi'].mean()
        at_risk_count = len(merged[merged['rsi'] < 60])
        output.append(f"- Average Squad RSI: {avg_rsi:.1f}")
        output.append(f"- Players at Risk (RSI < 60): {at_risk_count}")
        output.append(f"- Average Weekly Load: {merged['weekly_load'].mean():.1f}")
        
        return "\n".join(output)
    
    def medical_team_brief(self, target_date: pd.Timestamp) -> str:
        """
        Generate brief for sports medicine/athletic training staff.
        Focused on: recovery indicators, injury risk patterns, and monitoring flags.
        """
        report = self.analyzer.generate_daily_readiness_report(target_date)
        
        # Recent load trends (last 14 days)
        recent_start = target_date - timedelta(days=14)
        player_ids = self.daily_load['player_id'].unique()
        
        output = []
        output.append("=" * 90)
        output.append(f"MEDICAL TEAM BRIEF - {target_date.date()}")
        output.append("=" * 90)
        output.append("")
        output.append("RECOVERY STATUS BY PLAYER")
        output.append("-" * 90)
        output.append(report[['player_name', 'rsi', 'recovery_score', 'acr', 'risk_category']].to_string(index=False))
        output.append("")
        
        # Detailed player insights
        output.append("INDIVIDUAL PLAYER NOTES")
        output.append("-" * 90)
        for player_id in player_ids:
            player_name = self.daily_load[self.daily_load['player_id'] == player_id]['player_name'].iloc[0]
            player_report = report[report['player_id'] == player_id].iloc[0]
            
            # Get recent wellness data
            player_wellness = self.wellness[
                (self.wellness['player_id'] == player_id) & 
                (self.wellness['date'] >= recent_start)
            ].sort_values('date', ascending=False)
            
            output.append(f"\n{player_name}:")
            output.append(f"  - RSI: {player_report['rsi']:.1f} ({player_report['risk_category']})")
            output.append(f"  - ACR: {player_report['acr']:.2f} ({'Underload' if player_report['acr'] < 0.8 else 'Normal' if player_report['acr'] <= 1.3 else 'Elevated'})")
            
            if len(player_wellness) > 0:
                recent_sleep = player_wellness['sleep_hours'].mean()
                recent_soreness = player_wellness['muscle_soreness'].mean()
                output.append(f"  - Recent sleep: {recent_sleep:.1f} hrs/night")
                output.append(f"  - Muscle soreness (avg): {recent_soreness:.1f}/10")
            
            # Flag if history is concerning
            roster_info = self.roster[self.roster['player_id'] == player_id]
            if len(roster_info) > 0 and roster_info['injury_history'].iloc[0] != 'None':
                output.append(f"  [HISTORY] {roster_info['injury_history'].iloc[0]}")
        
        output.append("")
        output.append("MONITORING PRIORITIES")
        output.append("-" * 90)
        at_risk = report[report['rsi'] < 60].sort_values('rsi')
        if len(at_risk) > 0:
            output.append("High Priority (RSI < 60):")
            for _, player in at_risk.iterrows():
                output.append(f"  - {player['player_name']}: RSI {player['rsi']:.1f} | Recommend daily check-ins")
        
        return "\n".join(output)
    
    def executive_summary(self, target_date: pd.Timestamp) -> str:
        """
        Generate executive summary for leadership/coaching staff.
        Focused on: squad-level trends, key metrics, season context.
        """
        report = self.analyzer.generate_daily_readiness_report(target_date)
        
        week_start = target_date - timedelta(days=target_date.weekday())
        month_start = target_date.replace(day=1)
        
        week_load = self.daily_load[
            (self.daily_load['date'] >= week_start) & 
            (self.daily_load['date'] <= target_date)
        ]['daily_load'].sum()
        
        month_load = self.daily_load[
            (self.daily_load['date'] >= month_start) & 
            (self.daily_load['date'] <= target_date)
        ]['daily_load'].sum()
        
        output = []
        output.append("=" * 90)
        output.append(f"EXECUTIVE SUMMARY - {target_date.date()}")
        output.append("=" * 90)
        output.append("")
        output.append("SQUAD STATUS")
        output.append("-" * 90)
        output.append(f"- Average Readiness (RSI): {report['rsi'].mean():.1f}/100")
        output.append(f"- Players Ready (RSI > 80): {len(report[report['rsi'] > 80])}/{len(report)}")
        output.append(f"- Players at Risk (RSI < 60): {len(report[report['rsi'] < 60])}/{len(report)}")
        output.append("")
        
        output.append("LOAD TRENDS")
        output.append("-" * 90)
        output.append(f"- This week's load: {week_load:.0f} units")
        output.append(f"- This month's load: {month_load:.0f} units")
        output.append(f"- Average daily load: {self.daily_load[self.daily_load['date'] <= target_date]['daily_load'].mean():.1f} units")
        output.append("")
        
        output.append("KEY ALERTS")
        output.append("-" * 90)
        at_risk = report[report['rsi'] < 60]
        if len(at_risk) > 0:
            output.append(f"[AT-RISK] {len(at_risk)} player(s) below readiness threshold:")
            for _, row in at_risk.iterrows():
                output.append(f"   - {row['player_name']} (RSI: {row['rsi']:.1f})")
        else:
            output.append("[OK] All players within acceptable readiness range")
        
        return "\n".join(output)


def main():
    """Generate all reports."""
    print("Initializing report generation...\n")
    
    processor = DataProcessor("data")
    data = processor.load_all_data()
    
    daily_load = processor.calculate_daily_load()
    gen = ReportGenerator(
        daily_load=daily_load,
        wellness=data['wellness'],
        gps=data['gps'],
        game=data['game'],
        roster=data['roster']
    )
    
    target_date = daily_load['date'].max()
    
    # Generate all reports
    print("\n" + gen.coaching_staff_dashboard(target_date))
    print("\n\n" + gen.medical_team_brief(target_date))
    print("\n\n" + gen.executive_summary(target_date))
    
    # Determine output directory
    output_dir = Path("outputs")
    if not output_dir.is_absolute():
        # Try from current directory first, then from parent
        if not (Path.cwd() / output_dir).exists():
            output_dir = Path.cwd().parent / output_dir
    
    # Create output directory if it doesn't exist
    output_dir.mkdir(exist_ok=True)
    
    # Save to files
    with open(output_dir / "coaching_dashboard.txt", "w") as f:
        f.write(gen.coaching_staff_dashboard(target_date))
    
    with open(output_dir / "medical_brief.txt", "w") as f:
        f.write(gen.medical_team_brief(target_date))
    
    with open(output_dir / "executive_summary.txt", "w") as f:
        f.write(gen.executive_summary(target_date))
    
    print("\n[OK] Reports saved to outputs/")


if __name__ == "__main__":
    main()
