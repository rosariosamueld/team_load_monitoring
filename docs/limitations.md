# Limitations & Data Gaps

## Current Project Scope

This project is a **proof-of-concept** for a professional athlete monitoring system. It demonstrates core responsibilities and analytical approaches, but operates with several simplifications and limitations necessary for a standalone portfolio project.

---

## 1. Data Limitations

### Missing Real-World Data Sources
| Data Source | Not Included | Impact |
|-------------|-------------|--------|
| **Actual GPS tracking** | Simplified synthetic data; limited accelerometry detail | Load calculation less precise; position-specific patterns can't be detected |
| **Heart Rate / HRV** | No HR or heart rate variability data | Can't assess autonomic nervous system recovery |
| **Strength testing** | No force plate, jump, or isokinetic data | Missing neuromuscular fatigue indicators |
| **Injury outcomes** | No injuries recorded in dataset | Can't validate RSI's predictive power with actual injury data |
| **Longitudinal history** | Only 15 days of data; no seasonal baseline | Can't establish individual player tolerance thresholds |

### Sample Data Notes
- **3 players, 15 days** of synthetic data created for demonstration
- Reflects realistic load patterns but lacks:
  - Full roster depth (no bench players, no practice squad)
  - Seasonal variation (playoffs, back-to-backs, rest days mid-season)
  - Injury scenarios (can't show how metrics change post-injury)
  - Inter-league comparisons (no benchmarks vs. other teams)

### Recommendations for Real Implementation
1. **Import 12+ months of historical data** before deploying (establish baselines)
2. **Integrate real GPS system** (Catapult, Statsports) with automatic data feeds
3. **Add wearables** (Oura Ring, Whoop, Apple Watch) for HRV and continuous monitoring
4. **Link to medical database** (injury logs) to validate ACR-injury associations

---

## 2. Analytical Limitations

### Fixed Thresholds Are Not Personalized
- **Current approach:** ACR >1.5 injury risk, RSI <60 at-risk for all players
- **Reality:** Elite athletes often tolerate higher loads; players with previous injuries may need lower thresholds
- **Gap:** This system requires ~8 weeks of baseline data per player to build personalized models

### RSI Doesn't Account For...
- **Training quality:** A maximal-effort session ≠ skill drill (same RPE × duration, different stimulus)
- **Game demands:** In-game load differs from practice (fatigue + pressure + opponent variability)
- **Travel/schedule:** Jet lag, back-to-backs, road games aren't coded as load factors
- **Environmental factors:** Temperature, altitude, gym availability not captured
- **Psychological stress:** Team dynamics, pressure, family issues don't appear in data

### No Injury Prediction Yet
- **Current use case:** Descriptive ("who is tired right now?") not predictive ("who will get injured?")
- **Why:** Requires paired injury + load history for machine learning
- **Path forward:** Collect 1–2 seasons + build logistic regression to predict probability of injury within 7 days

### Position-Specific Insights Limited
- Guards naturally accumulate distance; centers accumulate accelerations
- **Current approach:** Squad-level metrics mask position differences
- **Needed:** Separate ACR thresholds for Guards vs. Centers vs. Forwards

---

## 3. Technical Limitations

### Manual Data Entry Points
- **Dependency:** Players must submit wellness surveys daily (compliance issues)
- **Solution:** Integrate with wearable platforms (auto-sync from Oura, Whoop)
- **Current state:** Relies on discipline; missing surveys = missing recovery data

### No Real-Time Alerts
- **Current:** Daily batch reports (end-of-day review)
- **Ideal:** Real-time alerts if ACR spikes or recovery crashes mid-day
- **Barriers:** Requires live GPS feed + automated analysis infrastructure

### Limited Integration With Existing Systems
- **Current:** Standalone CSV-based pipeline
- **Real implementation:** Must integrate with:
  - Official team scheduling systems
  - Medical IT (injury tracking)
  - Strength & conditioning software (Vimeo, TrainHeroic)
  - Roster management (salary cap, contracts, playing time)

### No Advanced Statistical Validation
- No confidence intervals around RSI predictions
- No sensitivity analysis ("what if sleep data is 10% underestimated?")
- No cross-validation testing (train/test split)

---

## 4. Organizational Limitations

### Assumes Buy-In From All Levels
- **Coaches must:** Assign honest session RPE (can be skipped under time pressure)
- **Players must:** Complete daily wellness surveys (compliance ~70–80% typical)
- **Medical staff must:** Act on red flags (conflicts with coaching pressure to play)
- **Issue:** In first season, adoption friction is real

### No Cost/Resource Considerations
- GPS hardware: $15K–50K per team annually (Catapult Elite)
- Wearable subscriptions: $500–5K per player yearly
- Staff time: 0.5–1 FTE analyst minimum
- **Current project:** Ignores licensing, infrastructure, privacy (HIPAA) compliance

### Missing Contextual Workflows
- How does an athlete sit out a game due to high RSI?
- What's the protocol if a player disagrees with readiness rating?
- How are recommendations communicated in real time?
- Who has final say: Coach or medical staff?

---

## 5. Statistical Limitations

### Sample Size Too Small
- **Current:** 3 players, 15 days = 45 player-days
- **Minimum recommended:** 30+ players, 100+ days = 3,000+ player-days
- **Effect:** Can't detect significant differences or outliers reliably

### No Control Group
- Can't compare monitored players vs. unmonitored (injury rates)
- Can't compare RSI-guided load management vs. traditional approach

### Survivorship Bias
- If this system successfully prevents injuries, we won't see injuries to validate it
- Need long-term prospective study to establish true predictive power

---

## 6. External Validity Issues

### This Data Reflects One Team's Context
- League: NBA-like (season, schedule, elite athletes)
- Not generalizable to college, high school, or other sports
- Different sports (soccer, rugby, tennis) have different load profiles
- Position effects vary by sport

### Synthetic Data Limitations
- Relationships in synthetic data are artificially clean
- Real data includes measurement error, missing values, outliers
- Real players show individual quirks (one "sleeps poorly but recovers great"; another inverse)

---

## 7. Recommendations for Improving This Project

### Short-term (Portfolio Review)
- [ ] Add README note explicitly stating this is proof-of-concept
- [ ] Document all assumptions and thresholds clearly
- [ ] Include comparison to published research thresholds
- [ ] Show awareness of limitations (interviewers respect this)

### Medium-term (Real Implementation)
- [ ] Secure 12 months historical data + real roster
- [ ] Integrate GPS data from actual wearables
- [ ] Add HRV or strength testing validation
- [ ] Personalize thresholds after 8-week baseline period

### Long-term (Production)
- [ ] Collect 2+ seasons to build predictive injury model
- [ ] Machine learning: Predict injury probability, not just current risk
- [ ] Integrate performance data (on-court efficiency by RSI level)
- [ ] Real-time dashboards for coaching staff during practice
- [ ] Mobile app for player wellness surveys + instant feedback

---

## 8. Questions This Doesn't (Yet) Answer

1. **"Does high load actually cause injuries?"** → Need injury data + matched controls
2. **"What's the optimal training load for maximum performance?"** → Need game performance + load correlation
3. **"Which player is most likely to get injured this week?"** → Need predictive model + validation
4. **"How much load is too much for this specific player?"** → Need individual baseline + personalization
5. **"Are we overtraining or undertraining as a team?"** → Needs seasonal trend analysis + benchmarking
6. **"What's the relationship between wellness compliance and injury risk?"** → Needs compliance data collection

---

## Contact & Feedback

This project is intentionally scoped for a portfolio demonstration. Feedback on what additional analyses would be most valuable for a professional setting is welcome.

For questions about assumptions, methods, or limitations, refer to [methodology.md](methodology.md).
