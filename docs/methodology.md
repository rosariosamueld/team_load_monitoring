# Methodology & Core Metrics

## Overview

This document explains the analytical foundations behind the load monitoring system, particularly the **Recovery Status Index (RSI)** and **Acute:Chronic Workload Ratio (ACR)**.

---

## 1. Training Load Calculation

### Formula
$$\text{Daily Load} = \frac{\text{Session RPE} \times \text{Duration (min)}}{10}$$

### Rationale
- **Evidence-based:** Standardized metric from Foster et al. (Sports Medicine)
- **Simple:** Coaching staff can verify calculations
- **Practical:** Requires minimal additional instrumentation beyond existing data

### Interpretation
- **Load = 30–50:** Light session (technical work, recovery) 
- **Load = 50–80:** Moderate session (conditioning, drills)
- **Load = 80–120+:** High-intensity session (scrimmage, competition)

### Example Calculation
- Scrimmage: Session RPE = 8, Duration = 120 min
- Daily Load = (8 × 120) / 10 = **96 units**

### Alternative Load Metrics (Not Used Here; For Reference)
- **GPS-based:** Edwards' Load = √[(acceleration² + deceleration² + speed²) × time]
- **Heart rate:** TRIMP = Duration × Intensity × HR Zone weighting
- **Combination:** Multi-modal score combining RPE + GPS + HR

**Trade-off:** We chose RPE-based for simplicity and team staff familiarity. GPS would add granularity but require additional equipment/processing.

---

## 2. Acute:Chronic Workload Ratio (ACR)

### Formula
$$\text{ACR} = \frac{\text{Avg Load (past 7 days)}}{\text{Avg Load (past 28 days)}}$$

### Interpretation

| ACR Range | Status | Injury Risk | Recommendation |
|-----------|--------|-------------|-----------------|
| < 0.8 | Underloaded | Detraining | Increase training stimulus |
| 0.8–1.3 | Optimal | Low | Maintain current load |
| 1.3–1.5 | Elevated | Moderate | Monitor closely; consider slight reduction |
| > 1.5 | Overloaded | **High** | **Recommend immediate load reduction** |

### Scientific Basis
- **Key Research:** Gabbett et al. (2016); Drew & Finch (2016)
- ACR >1.5 is associated with elevated injury risk in team sports
- Accounts for **training tolerance:** A player conditioned to high load may safely tolerate higher ACR than a deconditioned player
- Rolling window prevents single-session spikes from dominating signal

### Limitations
- **Assumes fitness is stable:** Doesn't account for conditioning changes over months
- **Group-level threshold:** Individual players may have different safe thresholds (need personalization over time)
- **Doesn't capture training quality:** 120 units of skill drills ≠ 120 units of max-effort conditioning

---

## 3. Recovery Status Index (RSI)

### Formula
$$\text{RSI} = 100 - \left( \frac{\text{ACR}}{2} + \frac{(100 - \text{Recovery Score})}{2} \right)$$

### Components

#### 3a. Acute:Chronic Ratio (ACR)
- See section above
- Normalized to 0–100 scale by ACR/2 in the formula

#### 3b. Recovery Score (0–100)
Weighted composite of daily wellness metrics:

$$\text{Recovery Score} = (S_{quality} \times 0.35) + (S_{duration} \times 0.25) + (S_{soreness} \times 0.25) + (S_{fatigue} \times 0.15)$$

Where:
- **S_quality** = (Sleep Quality / 10) × 100
  - 10/10 quality = 100 points
  - 5/10 quality = 50 points

- **S_duration** = (Sleep Hours / 8.5) × 100, clamped 0–100
  - Target: 8.5 hours
  - 7 hours = 82 points
  - 6 hours = 71 points

- **S_soreness** = 100 − (Soreness / 10) × 100
  - Inverse: lower soreness = higher score
  - 2/10 soreness = 80 points
  - 6/10 soreness = 40 points

- **S_fatigue** = 100 − (Fatigue / 10) × 100
  - Inverse: lower fatigue = higher score
  - 3/10 fatigue = 70 points

**Example:**
- Sleep: 7.5 hrs, quality 7/10 → avg ~75 points
- Soreness: 3/10 → 70 points
- Fatigue: 4/10 → 60 points
- **Recovery Score ≈ 72 / 100**

### RSI Thresholds & Action

| RSI | Risk Status | Traffic Light | Recommendation |
|-----|------------|----------------|-----------------|
| > 80 | Ready | 🟢 Green | Full training; normal availability |
| 60–80 | Monitor | 🟡 Yellow | Monitor closely; reduce load if trends worsen |
| < 60 | At Risk | 🔴 Red | High risk; recommend DNP-rest, limited minutes, or load reduction |

### Example Scenarios

**Scenario 1: Optimal Player**
- ACR = 1.0 (balanced loading)
- Recovery Score = 85 (good sleep + low soreness)
- **RSI = 100 − (1.0/2 + 15/2) = 100 − 8 = 92** 🟢 Ready

**Scenario 2: Accumulated Fatigue**
- ACR = 1.4 (elevated load)
- Recovery Score = 55 (poor sleep, high soreness)
- **RSI = 100 − (1.4/2 + 45/2) = 100 − 23.7 = 76** 🟡 Monitor

**Scenario 3: At Risk**
- ACR = 1.6 (high load spike)
- Recovery Score = 40 (very poor recovery)
- **RSI = 100 − (1.6/2 + 60/2) = 100 − 30.8 = 69** 🟡 Monitor → 🔴 if persistent

---

## 4. Additional Metrics

### Game Performance Correlation (Future)
- **Hypothesis:** High RSI + game load = maintained on-court efficiency
- **Counterexample:** High load + low RSI = decreased efficiency (true shooting % drops)
- *Note: Currently in sample data; full analysis pending more games*

### Workload Tolerance (Emerging)
- Individual baseline: Does Player X consistently show ACR >1.4 without issue?
- Personalized thresholds: Adjust risk categories by player history
- *Requires 2–3 months of paired injury/performance data*

---

## 5. Interpretation Guide for Coaches & Medical Staff

### For Coaching Staff
- **Daily use:** Check RSI before training
- **Green (>80):** Plan normal/high-intensity session; player ready for competition
- **Yellow (60–80):** Reduce intensity slightly; skip collision-heavy drills; monitor energy
- **Red (<60):** Consider DNP-rest, off-field conditioning, or reduced minutes in games

### For Medical/Athletic Training
- **ACR spike + low recovery score:** Likely musculoskeletal fatigue or systemic fatigue
- **ACR normal but low recovery score:** Possible overtraining response, illness, sleep deprivation
- **High ACR but high recovery score:** Player is coping well; may sustain higher load
- **Persistent red flags:** Recommend medical assessment (infection, illness, overtraining syndrome)

---

## 6. Known Limitations & Caveats

### 1. **RPE-Based Load is Subjective**
- Coach's session RPE and player's individual RPE may not perfectly align
- Conditioning state affects perceived effort (same workout feels harder when fatigued)
- **Mitigation:** Cross-check with GPS distance/intensity metrics when available

### 2. **Recovery Score Relies on Self-Report**
- Players may underestimate soreness/fatigue to avoid sitting out
- Sleep data from wearables (Oura, Apple Watch) preferred but not always available
- **Mitigation:** Combine with objective HRV, resting HR, or force plate testing if possible

### 3. **Fixed Thresholds Are Population-Level**
- ACR >1.5 is average injury risk threshold based on team-sport research
- Individual players tolerate different loads (e.g., elite athletes often higher ACR)
- **Mitigation:** Personalize thresholds after 12+ weeks of baseline data

### 4. **No Strength/Power Testing Integration**
- Currently doesn't include force plate (jump height, rate of force development)
- HRV, grip strength, or repeated sprint capacity would strengthen assessment
- **Future:** Add quarterly neuromuscular testing

### 5. **Position-Specific Thresholds Not Yet Applied**
- Guards accumulate higher distance; centers accumulate higher accelerations
- Same ACR value may mean different things by position
- **Current approach:** Squad-level thresholds; recommend tracking by position once data established

### 6. **Injury Outcome Data Not Available**
- Ideal validation: "Did player with RSI < 60 subsequently get injured?"
- Currently, RSI must be validated against external benchmarks or historical data
- **Plan:** Collect 1+ year of injury data to refine models

---

## 7. Implementation Best Practices

### Daily Workflow
1. **08:00–09:00:** Players complete wellness survey (before training)
2. **16:00:** Coach assigns session RPE post-practice
3. **17:00:** Analyst calculates load & RSI; alerts coaching staff if red flags
4. **Next morning:** Readiness report reviewed before training session planning

### Weekly Review
- Thursday: End-of-week load summary + readiness trends
- Friday: Plan weekend recovery and following week's intensity

### Monthly Review
- Assess cumulative load trends
- Personalize thresholds if player-specific patterns emerge
- Communicate with medical staff on chronic responders

---

## 8. References & Further Reading

### Seminal Research
- **Foster et al. (1995).** "Monitoring training in athletes with reference to overtraining syndrome." *Med Sci Sports Exerc*
- **Gabbett et al. (2016).** "The athlete monitoring cycle: a systematic approach to injury prevention." *Br J Sports Med*
- **Hulin et al. (2016).** "Sport injury risk during acute periods of match congestion: A new player metric." *Scand J Med Sci Sports*

### Recommended Tools
- **Catapult Sports:** GPS + load integration
- **Tableau / Power BI:** Dashboard creation
- **HRV tools:** Oura, Whoop for additional recovery data

---

## Contact & Questions

For methodology questions or suggested modifications, reach out to the Performance Analytics team.
