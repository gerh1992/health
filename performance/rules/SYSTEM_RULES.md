# Performance Log System Rules (Multi-CSV Architecture)

## Canonical paths
All files are located relative to the repository root `/home/ubuntu/.hermes/data/health/` (or locally `/Users/ghidalgo/projects/ai-systems/health/`):
- Schema definition: `performance/schema/SCHEMA.json`
- Database files:
  - `performance/data/biometrics.csv`
  - `performance/data/sessions.csv`
  - `performance/data/fitness_metrics.csv`
  - `performance/data/match_details.csv`
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
Stores details for competitive team sports. Links to `sessions.csv` via `Session_Id`.
- `Session_Id`: Primary Key & Foreign Key linking to `sessions.csv`.
- `Sport`: Enum: `Padel`, `Soccer`, `Tennis`.
- `Match_Result`: Enum: `Win`, `Loss`, `-` (for practices or recreational matches).
- `Match_Type`: Enum: `Friendly`, `Tournament`, `-`.
- `Tournament_Category`: Level of the tournament (e.g. `7ma`, `6ta`, `1ra` or `-` if friendly/recreational).
- `Score`: String score (e.g. `6-4 6-2`, `5-3` or `-`).
- `Partner`: Name of teammate(s) or `-`.
- `Opponents`: Name of opponent(s) or `-`.

### 5. `supplements.csv` (Daily Supplement Adherence Log)
Logs daily intake of supplements. Exactly one row per date.
- `Date`: String, format `YYYY-MM-DD` (Primary Key).
- `Protein`: Enum: `True`, `False`, `-`.
- `Creatine`: Enum: `True`, `False`, `-`.
- `Magnesium`: Enum: `True`, `False`, `-`.
- `Retinol`: Enum: `True`, `False`, `-`.
- `Ashwagandha`: Enum: `True`, `False`, `-`.

---

## Placeholder Semantics
- `-` always means **unknown / not reported by the user / intentionally left blank because the data point is unavailable**.
- `-` does **not** mean zero.
- `-` does **not** mean a negative result.
- In `match_details.csv`, `Match_Result: -` means the session was non-competitive, a practice, or the result was not explicitly reported.

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
