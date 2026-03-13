# Setup & Quick Start

## Prerequisites

- Python 3.8+
- pip or conda for package management

## Installation

### 1. Clone or Download Repository
```bash
cd Load_Monitoring
```

### 2. Create Virtual Environment (Recommended)
```bash
# Using venv
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Using conda
conda create -n load_monitor python=3.9
conda activate load_monitor
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

## Running the Analysis

### Option 1: Run Individual Modules

#### Load & Validate Data
```bash
cd scripts
python data_processing.py
```
**Output:** Displays data summary, validation report, and daily load calculations

#### Calculate Readiness Metrics
```bash
python readiness_analysis.py
```
**Output:** Recovery Status Index (RSI) report for all players

#### Generate Reports
```bash
python reporting.py
```
**Output:** Three text-based reports to `outputs/`:
- `coaching_dashboard.txt` - Coaching staff focus
- `medical_brief.txt` - Athletic training focus
- `executive_summary.txt` - Leadership summary

#### Create Visualizations
```bash
python visualization.py
```
**Output:** PNG charts saved to `outputs/`:
- `weekly_load.png` - Bar chart of weekly load by player
- `load_trend_*.png` - Individual player load trends
- `rsi_dashboard.png` - Comprehensive readiness dashboard

### Option 2: Run Full Pipeline (One Command)
```bash
# From Load_Monitoring directory
python -c "
from scripts.data_processing import DataProcessor
from scripts.readiness_analysis import ReadinessAnalyzer
from scripts.reporting import ReportGenerator
from scripts.visualization import DataVisualizer
import os

processor = DataProcessor('data')
data = processor.load_all_data()
processor.validate_data()

daily_load = processor.calculate_daily_load()
gen = ReportGenerator(daily_load, data['wellness'], data['gps'], data['game'], data['roster'])
target_date = daily_load['date'].max()

print(gen.coaching_staff_dashboard(target_date))
print('\n' + gen.medical_team_brief(target_date))
print('\n' + gen.executive_summary(target_date))

viz = DataVisualizer(daily_load, data['wellness'], data['roster'])
viz.plot_weekly_load_by_player()
for player_id in daily_load['player_id'].unique():
    viz.plot_load_trend_by_player(player_id)
viz.plot_rsi_dashboard(target_date)

print('\n✓ Pipeline complete!')
"
```

## File Structure After Running

```
Load_Monitoring/
├── data/
│   ├── gps_tracking.csv
│   ├── rpe_sessions.csv
│   ├── wellness_daily.csv
│   ├── game_performance.csv
│   └── player_roster.csv
├── scripts/
│   ├── data_processing.py
│   ├── readiness_analysis.py
│   ├── reporting.py
│   └── visualization.py
├── outputs/  ← Generated files appear here
│   ├── coaching_dashboard.txt
│   ├── medical_brief.txt
│   ├── executive_summary.txt
│   ├── weekly_load.png
│   ├── load_trend_P001.png
│   ├── load_trend_P002.png
│   ├── load_trend_P003.png
│   └── rsi_dashboard.png
├── docs/
│   ├── data_schema.md
│   ├── methodology.md
│   └── limitations.md
├── requirements.txt
└── README.md
```

## Current Data

**Players:** 3 (Marcus Johnson, Sarah Chen, DeAndre Williams)  
**Date Range:** December 1-15, 2025 (15 days)  
**Data Types:** GPS tracking, RPE sessions, wellness surveys, game performance

## Key Metrics

- **Daily Load:** Session RPE × Duration / 10
- **ACR (Acute:Chronic Ratio):** 7-day avg load / 28-day avg load
- **Recovery Score:** Composite of sleep, soreness, fatigue (0-100)
- **RSI (Recovery Status Index):** Readiness score combining load & recovery (0-100)

### Risk Thresholds
- 🟢 **RSI > 80:** Ready for full training
- 🟡 **RSI 60-80:** Monitor; consider load management
- 🔴 **RSI < 60:** At risk; recommend load reduction

## Documentation

- **[README.md](../README.md)** - Project overview
- **[data_schema.md](../docs/data_schema.md)** - Data dictionary & collection guide
- **[methodology.md](../docs/methodology.md)** - Detailed metrics & formulas
- **[limitations.md](../docs/limitations.md)** - Known gaps & future work

## Troubleshooting

### Import Errors
```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

### "ModuleNotFoundError: No module named 'scripts'"
```bash
# Run from Load_Monitoring directory
# Make sure scripts/ folder exists with all .py files
ls scripts/  # Check files are there
```

### No output files generated
```bash
# Create outputs directory if missing
mkdir outputs

# Try data_processing.py first to ensure data loads
python scripts/data_processing.py
```

## Next Steps

1. **Review sample outputs:** Check `outputs/*.txt` and visualizations
2. **Customize for your team:** Replace sample data with real data
3. **Add integration:** Connect to your team's existing systems
4. **Refine thresholds:** Personalize ACR & RSI cutoffs based on team history
5. **Expand metrics:** Add HRV, force plate, or performance correlation analysis

## Questions?

See **[methodology.md](../docs/methodology.md)** for detailed explanations of formulas and interpretations.

See **[limitations.md](../docs/limitations.md)** for known gaps and future enhancements.
