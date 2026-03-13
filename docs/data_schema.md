# Data Schema & Dictionary

## Overview

This document describes all data sources, fields, and expected formats for the athlete monitoring system.

## Core Data Files

### 1. player_roster.csv
**Purpose:** Master player registry and metadata

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| player_id | String | Unique player identifier | P001 |
| player_name | String | Full player name | Marcus Johnson |
| position | String | Basketball position | SG, PG, C, etc. |
| jersey_number | Integer | Jersey number | 7 |
| height_cm | Integer | Height in centimeters | 198 |
| weight_kg | Integer | Body weight in kilograms | 95 |
| injury_history | String | Previous injuries (informational) | None, ACL (2023), etc. |
| season | String | Season identifier | 2025-26 |

### 2. gps_tracking.csv
**Purpose:** GPS/LPS tracking data from wearables during training/games

**Collection:** Typically from GPS units on chest harness or integrated wearables (Catapult, Statsports, etc.)

| Field | Type | Description | Unit | Expected Range |
|-------|------|-------------|------|-----------------|
| player_id | String | Player identifier | — | P001-P999 |
| player_name | String | Player name | — | — |
| date | Date | Session date | YYYY-MM-DD | — |
| distance_m | Float | Total distance covered | meters | 3,000-12,000 |
| max_speed_kmh | Float | Maximum speed achieved | km/h | 15-35 |
| acceleration_count | Integer | Number of accelerations (>2 m/s²) | count | 50-250 |
| high_speed_runs | Integer | Runs >24 km/h | count | 5-60 |

**Data Quality Notes:**
- Missing sessions indicate rest days, absences, or equipment failure
- Speed metrics vary by position (guards run faster than centers; guards cover more distance)
- Accelerations correlate with high-intensity efforts

### 3. rpe_sessions.csv
**Purpose:** Rate of Perceived Exertion (RPE) ratings for training sessions and individual players

**Collection:** Coach assigns Session RPE; players rate perceived effort immediately post-session

| Field | Type | Description | Scale |
|-------|------|-------------|-------|
| date | Date | Session date | YYYY-MM-DD |
| session_type | String | Practice, Game, Recovery | — |
| session_rpe | Integer | Coach's RPE for that day's training | 1-10 |
| duration_min | Integer | Training session duration | minutes |
| player_id | String | Player identifier | — |
| player_name | String | Player name | — |
| player_rpe | Integer | Player's perceived effort | 1-10 |
| notes | String | Context/focus (optional) | Free text |

**Load Calculation:**
- **Daily Load = (Session RPE × Duration) / 10**
- This standardized formula comes from research (Foster et al.)
- Example: RPE 7 × 100 min = 700 / 10 = 70 units

### 4. wellness_daily.csv
**Purpose:** Daily wellness and recovery surveys taken each morning

**Collection:** Players complete via app/sheet each morning (ideally before training)

| Field | Type | Description | Scale |
|-------|------|-------------|-------|
| date | Date | Survey date | YYYY-MM-DD |
| player_id | String | Player identifier | — |
| player_name | String | Player name | — |
| sleep_hours | Float | Total sleep previous night | 0-12 hours |
| sleep_quality | Integer | Subjective sleep quality | 1-10 |
| muscle_soreness | Integer | Overall muscle soreness | 1-10 (1=none, 10=severe) |
| fatigue_level | Integer | General fatigue/energy | 1-10 (1=fresh, 10=exhausted) |
| stress_level | Integer | Emotional/mental stress | 1-10 |
| mood_notes | String | Optional context | Free text |

**Interpretation:**
- Sleep <7 hrs or quality <5 indicates poor recovery
- Soreness + Fatigue >12 combined may indicate CAR recovery lag
- Stress impacts all recovery markers

### 5. game_performance.csv
**Purpose:** On-court game statistics

**Collection:** Official game stat sheets + advanced metrics (via stats partner)

| Field | Type | Description | Scale |
|-------|------|-------------|-------|
| date | Date | Game date | YYYY-MM-DD |
| player_id | String | Player identifier | — |
| player_name | String | Player name | — |
| points | Integer | Points scored | count |
| assists | Integer | Assists | count |
| rebounds | Integer | Rebounds | count |
| true_shooting_pct | Float | TS% (shooting efficiency) | 0.0-1.0 |
| usage_rate | Float | Usage rate (% of possessions) | 0.0-100.0 |
| minutes_played | Float | Minutes on court | minutes |

**Context:** Used to correlate load with on-court performance (load ↔ efficiency trade-offs)

---

## Data Validation Rules

### Required Fields
- GPS: date, player_id, distance_m
- RPE: date, player_id, session_rpe, duration_min
- Wellness: date, player_id, sleep_hours, muscle_soreness
- Game: date, player_id, minutes_played

### Acceptable Ranges
| Field | Min | Max | Flag if… |
|-------|-----|-----|----------|
| distance_m | 2,500 | 12,500 | Outside range (may indicate missing data or position error) |
| session_rpe | 1 | 10 | Out of bounds |
| sleep_hours | 3 | 12 | <5 or >9 indicates potential issue |
| player_rpe | 1 | 10 | Out of bounds |

### Missing Data Handling
- **GPS missing on a given day** → Likely rest day or injury; flagged in analysis
- **RPE missing** → Cannot calculate daily load; assume player absent
- **Wellness missing** → Use imputation from rolling average or adjacent days
- **Game stats missing** → Expected; only games have game data

---

## Data Collection Responsibilities

| Role | Collects | Frequency |
|------|----------|-----------|
| Strength & Conditioning Coach | GPS tracking upload | Daily (practices/games) |
| Head Coach | Session RPE assignment | Each practice day |
| Players | Wellness survey | Daily (morning) |
| Stats/Analytics | Game performance | Post-game |
| Medical Staff | Injury status, clearances | As-needed notes in roster |

---

## Future Enhancements

- Heart rate variability (HRV) for autonomic recovery status
- Force plate data from strength testing
- Musculoskeletal screening scores
- Real-time wearable integration (Oura, Whoop, Apple Watch)
