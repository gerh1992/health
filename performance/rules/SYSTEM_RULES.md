# Performance Log System Rules (Multi-CSV Architecture)

## Canonical paths
All files are located relative to the repository root `/home/ubuntu/.hermes/data/health/` (or locally `/Users/ghidalgo/projects/ai-systems/health/`):
- Schema definition: `performance/schema/SCHEMA.json`
- Database files:
  - `performance/data/biometrics.csv`
  - `performance/data/sessions.csv`
  - `performance/data/fitness_metrics.csv`
  - `performance/data/match_details.csv`
  - `performance/data/padel_match_reviews.csv`
  - `performance/data/supplements.csv`
- Validation script: `performance/ops/validate_log.py`

---

## Data Models and Schema Rules

### 1. `biometrics.csv` (Daily Sleep & Recovery Log)
Logs recovery metrics. Exactly one row per date if sleep or recovery data is reported.
- `Date`: String, format `YYYY-MM-DD` (Primary Key).
- `Sleep_Hours`: Decimal representing duration (e.g. `7.25`, `8.5`, `6.0`).
- `HRV_Morning`: Integer representing morning HRV or `-`.
- `RHR_Night`: Integer representing night RHR or `-`.
- `Sleep_Quality`: Integer (1-10) representing subjective quality or `-`.
- `Energy_Level`: Integer (1-10) representing morning energy or `-`.
- `Comments`: Free-text string.

### 2. `sessions.csv` (Main Activity Log)
Logs all main daily events (trainings, padel matches, work, recovery walk, etc.).
- `Session_Id`: Unique string identifier (e.g., `YYYY-MM-DD-strength`, `YYYY-MM-DD-padel`).
- `Date`: String, format `YYYY-MM-DD`.
- `Category`: Enum: `Strength`, `Cardio`, `Padel`, `Soccer`, `Recovery`, `Social`, `Work`.
- `Activity`: Name of the session (e.g. `Gym Session`, `Partido Padel`, `Fútbol 5`).
- `Duration_Minutes`: Integer representing session duration.
- `RPE`: Integer (1-10) or `-`.
- `Session_Tag`: Enum: `High`, `Low`, `Match`, `Technical`, `Recovery`, `Social`, `Work`, `-`.
- `Comments`: Free-text string.

### 3. `fitness_metrics.csv` (Heterogeneous Performance Metrics)
Stores granular performance values (lifts, jumps, speed/sprints). Every row links to a session in `sessions.csv` via `Session_Id`.
- `Metric_Id`: Unique string identifier (e.g., `m-YYYY-MM-DD-N`).
- `Session_Id`: Foreign Key linking to `sessions.csv`.
- `Metric_Name`: Name of the metric (e.g. `Back Squat`, `Vertical Jump`, `Sprint 30m`).
- `Metric_Type`: Enum: `Strength`, `Jump`, `Speed`, `Endurance`.
- `Performance_Value`: Decimal value (e.g. `110.0`, `45.0`, `4.15` or `-` if unknown).
- `Performance_Unit`: Enum: `kg`, `cm`, `sec`, `m`.
- `Volume_Sets`: Integer or `-`.
- `Volume_Reps`: Integer or `-`.
- `Is_KPI`: Enum: `True` or `False`.
- `RPE`: Integer (1-10) or `-`.

### 4. `match_details.csv` (Team Sports & Competitive Matches)
Stores details for competitive team sports at the individual-match level. Multiple rows may link to the same session in `sessions.csv` when a tournament or multi-match day happens.
- `Match_Id`: Primary Key (e.g. `YYYY-MM-DD-padel-m1`).
- `Session_Id`: Foreign Key linking to `sessions.csv`.
- `Sport`: Enum: `Padel`, `Soccer`, `Tennis`.
- `Match_Number`: Integer sequence within the parent session (`1`, `2`, `3`, ...).
- `Match_Result`: Enum: `Win`, `Loss`, `-` (for practices or recreational matches).
- `Match_Type`: Enum: `Friendly`, `Tournament`, `-`.
- `Tournament_Category`: Level of the tournament (e.g. `7ma`, `6ta`, `1ra` or `-` if friendly/recreational).
- `Match_Stage`: Stage label (e.g. `group stage`, `quarterfinal`, `semifinal` or `-`).
- `Score`: String score (e.g. `6-4 6-2`, `5-3` or `-`).
- `Partner`: Name of teammate(s) or `-`.
- `Opponents`: Name of opponent(s) or `-`.

### 5. `supplements.csv` (Daily Supplement Adherence Log)
Logs daily intake of supplements. Exactly one row per date.
- `Date`: String, format `YYYY-MM-DD` (Primary Key).
- `Protein`: Enum: `True`, `False`, `-`.
- `Creatine`: Enum: `True`, `False`, `-`.
- `Collagen`: Enum: `True`, `False`, `-`.
- `Magnesium`: Enum: `True`, `False`, `-`.
- `Retinol`: Enum: `True`, `False`, `-`.
- `Ashwagandha`: Enum: `True`, `False`, `-`.

### 6. `padel_match_reviews.csv` (Tactical & Reflective Match Reviews)
Stores subjective tactical reviews for pattern detection and future experimentation.
- `Review_Id`: Primary Key (e.g. `r-2026-06-20-padel-m1`).
- `Date`: String, format `YYYY-MM-DD`.
- `Session_Id`: Foreign Key linking to `sessions.csv`.
- `Match_Id`: Foreign Key linking to `match_details.csv` or `-` if not yet attributed.
- `Sport`: Enum: `Padel`.
- `Role`: Enum: `Drive`, `Reves`, `-`.
- `Partner_Name`: String or `-`.
- `Partner_Level_Relative`: Enum: `Lower`, `Similar`, `Higher`, `-`.
- `Opponent_Level_Notes`: String or `-`.
- `Match_Context`: Enum: `Tournament`, `Friendly`, `Practice`, `-`.
- `Result`: Enum: `Win`, `Loss`, `-`.
- `Emotional_Tone`: String or `-`.
- `Main_Frustration`: String or `-`.
- `Main_Tactical_Problem`: String or `-`.
- `What_I_Did_Well`: String or `-`.
- `What_I_Did_Poorly`: String or `-`.
- `Adjustment_I_Needed`: String or `-`.
- `Adjustment_I_Tried`: String or `-`.
- `Next_Experiment`: String or `-`.
- `Drive_Intervention_Score`: Integer `1-5` or `-`.
- `Net_Presence_Score`: Integer `1-5` or `-`.
- `Volley_Damage_Score`: Integer `1-5` or `-`.
- `Tactical_Influence_Score`: Integer `1-5` or `-`.
- `Mental_Composure_Score`: Integer `1-5` or `-`.
- `Key_Pattern_Tags`: Pipe-delimited tags or `-`.
- `Free_Notes`: String or `-`.

---

## Placeholder Semantics
- `-` always means **unknown / not reported by the user / intentionally left blank because the data point is unavailable**.
- `-` does **not** mean zero.
- `-` does **not** mean a negative result.
- In `match_details.csv`, `Match_Result: -` means the individual match row was non-competitive, a practice, or the result was not explicitly reported.

## Multi-match session rule
- `sessions.csv` stays at the session/day level.
- `match_details.csv` stores one row per individual match.
- A tournament day can therefore have one `Session_Id` in `sessions.csv` and multiple `Match_Id` rows in `match_details.csv`.
- Preserve reported stage/context (`group stage`, `copa de plata`, etc.) in structured fields when available instead of compressing everything into one score string.

## Padel review ingestion rule
- Free-text user reflection is a valid input format for tactical reviews.
- Hermes should infer structured fields where confidence is high.
- Hermes should ask direct follow-up questions only for materially useful missing fields.
- Reviews belong in `padel_match_reviews.csv`, not in `sessions.csv` or `match_details.csv` comments.
- Subjective reflection must stay linkable to objective match rows through `Session_Id` and `Match_Id` whenever possible.

---

## Late-night attribution rule
When the user reports a completed day between `00:00` and `03:59` local time (GMT-3), assign that training/session to the **previous waking day** unless the user explicitly gives another date.

---

## Git workflow
- Before any modification, run `git pull --rebase` from the repo root.
- After any modification, verify all affected files, then commit with a contextual message.
- After committing, push to the remote.
- Hermes should use repo-local git author `Hermes Agent <hermes@local>` unless the user asks otherwise.

## Operational rule for Hermes
If Hermes updates the performance log in future sessions, it must write to the canonical path above and then commit the change in the `health` repo.
