# Basketball Team Load Monitoring & Performance Analytics

A practical framework for tracking athlete workload, recovery, and readiness to inform performance and injury prevention decisions across coaching and medical staff.

## Project Overview

This project demonstrates managment and analysis of team performance:

1. **Athlete Monitoring & Data Collection** — Aggregate multiple data sources (GPS, RPE, wellness, performance)
2. **Data Analysis & Performance Insights** — Identify workload patterns, recovery trends, injury risks
3. **Reporting & Communication** — Translate data into actionable insights for different stakeholders
4. **Analytics Infrastructure** — Build clean pipelines and scalable data systems

## Key Outputs

### Coaching Staff Dashboard
- Weekly workload summary by player
- Readiness status (green/yellow/red)
- Training load vs. recovery trends

### Medical Team Brief
- High-risk players (load spikes, recovery delays)
- Longitudinal workload patterns for injured/recovering athletes
- Anomalies in individual load tolerance

### Executive Summary
- Squad-level trends and benchmarks
- Key performance drivers and risks

## Key Takeaways

- **Position-Specific Load Patterns:** Guards accumulate higher distance and speed metrics, while centers show greater acceleration demands, highlighting the need for position-tailored monitoring thresholds.
- **ACR-RSI Relationship:** Acute:Chronic Workload Ratio (ACR) spikes correlate with declining Recovery Status Index (RSI), providing early warning of potential injury risk before performance drops.
- **Recovery Variability:** Individual players show distinct recovery profiles—some maintain readiness despite high load, while others require extended recovery, indicating personalized load tolerance.
- **Multi-Source Integration:** Combining GPS, RPE, and wellness data reveals load-recovery mismatches not visible in single metrics, enabling proactive intervention design.
- **Stakeholder-Relevant Insights:** Tailored reports translate complex data into actionable recommendations, supporting coaching decisions, medical monitoring, and organizational resource planning.

## Data Structure

```
data/
├── gps_tracking/          # GPS/LPS player movement data
├── rpe_surveys/           # Session and player RPE ratings
├── wellness/              # Daily wellness, sleep, muscle soreness
├── game_performance/      # Game stats and on-court metrics
└── player_roster.csv      # Player metadata and season info
```

## Core Metric: Recovery Status Index (RSI)

**Definition:** A composite readiness score derived from workload burden and recovery indicators.

$$\text{RSI} = 100 - \left( \frac{\text{Acute:Chronic Ratio}}{2} + \frac{(100 - \text{Recovery Score})}{2} \right)$$

Where:
- **Acute:Chronic Ratio (ACR)** = Average load past 7 days / Average load past 28 days *(Gabbett et al., 2016)*
- **Recovery Score** = Normalized composite of sleep, muscle soreness, and heart rate variability

**Interpretation:**
- 🟢 **RSI > 80**: Ready for full training / competition
- 🟡 **RSI 60-80**: Monitor closely; consider load management
- 🔴 **RSI < 60**: High fatigue/injury risk; recommend load reduction

## Repository Structure

```
Load_Monitoring/
├── data/                          # Sample and real data
│   ├── gps_tracking.csv
│   ├── rpe_sessions.csv
│   ├── wellness_daily.csv
│   ├── game_performance.csv
│   └── player_roster.csv
├── scripts/
│   ├── data_processing.py         # Clean and validate data
│   ├── readiness_analysis.py      # Calculate RSI and patterns
│   ├── reporting.py               # Generate reports for different audiences
│   └── visualization.py           # Charts and dashboards
├── outputs/
│   ├── coaching_dashboard.html    # Weekly insights for coaching staff
│   ├── medical_brief.pdf          # Risk flags for medical team
│   └── executive_summary.txt      # High-level trends
├── docs/
│   ├── data_schema.md             # Data dictionary and assumptions
│   ├── methodology.md             # Details on RSI calculation and metrics
│   └── limitations.md             # Known limitations and gaps
└── README.md
```

## How to Use

1. **Data Pipeline:**
   ```
   python scripts/data_processing.py --input data/ --output data_clean/
   ```

2. **Calculate Readiness Metrics:**
   ```
   python scripts/readiness_analysis.py --data data_clean/ --date 2025-12-15
   ```

3. **Generate Reports:**
   ```
   python scripts/reporting.py --data data_clean/ --output outputs/
   ```

## Key Design Decisions

- **Simple, defensible metric:** RSI combines acute:chronic workload ratio (proven injury predictor) with recovery indicators
- **Multiple output formats:** Coaching staff, medical team, and executive leadership all get tailored summaries
- **Transparent assumptions:** All calculations are documented; data gaps are acknowledged
- **Scalable infrastructure:** Data pipeline can integrate real-time systems (Catapult, Oura Ring, etc.)

## Next Steps / Future Enhancements

- [ ] Integrate game performance data with workload (efficiency vs. load trade-offs)
- [ ] Build machine learning model to predict injury risk
- [ ] Real-time alerts for load anomalies
- [ ] Player-specific load tolerance thresholds
- [ ] Integration with official team databases

## References

- Gabbett, T. J., et al. (2016). The athlete monitoring cycle: a systematic approach to injury prevention. *British Journal of Sports Medicine*, 50(13), 805-806.

## Author
Samuel Rosario, PhD

Biomechanics | Sport Performance | Applied Data Analysis