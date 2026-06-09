# Performance Log System Rules

## Canonical paths
- Source of truth CSV: `/home/ubuntu/.hermes/data/health/performance/data/performance_log.csv`
- Schema definition: `/home/ubuntu/.hermes/data/health/performance/schema/SCHEMA.json`
- Backup directory: `/home/ubuntu/.hermes/data/health/performance/backups/`
- Backup script: `/home/ubuntu/.hermes/data/health/performance/ops/backup_performance_log.sh`
- Repo root: `/home/ubuntu/.hermes/data/health`

## Non-canonical paths
Do **not** treat `~/.hermes/cache/documents/` as source of truth for health/performance data.
That area may contain uploads, temporary artifacts, or files that later disappear.

## Row model
One CSV row follows this schema:
- `Date`: string, format `YYYY-MM-DD`
- `Category`: enum string: `Biometrics`, `Strength`, `Padel`, `Recovery`, `Social`, `Work`
- `Activity`: string
- `Entry_Type`: enum string: `biometrics`, `session`, `kpi`, `accessory`
- `Session_Tag`: enum string: `High`, `Low`, `Match`, `Technical`, `Recovery`, `Social`, `Work`, `-`
- `Volume_Detail`: string
- `RPE`: stringified number like `7`, `8`, `8/10`, or `-` when unknown
- `HRV_Morning`: integer-as-string or `-`
- `RHR_Night`: integer-as-string or `-`
- `Comments`: free-text string

## Logging rules
- Add exactly one `biometrics` row when the day has sleep/recovery metrics.
- Add one `session` row per meaningful event category for that day.
- Add `kpi` rows only for lifts/tests that can change decisions.
- Add `accessory` rows only when preserving that movement is actually useful.
- Do not invent missing values. Use `-` when the user did not provide the number.

## Volume_Detail formatting rules
To enable automatic data parsing and analysis, the `Volume_Detail` column must follow strict formats based on the row's `Category` and `Entry_Type`:
- **Biometrics (biometrics)**: Sleep duration must be reported as a decimal number representing hours (e.g., `7.5`, `8.0`, `6.8`). Do not use text like "7h 2m" or "7.5h".
- **Strength (kpi)**: Principal lifts must follow the format `[Carga]kg - [Sets]x[Reps]` or top sets like `[Carga]kg x[Reps] top set; [Carga]kg - [Sets]x[Reps]` (e.g., `90kg - 3x4` or `110kg x3 top set; 100kg - 2x4`).
- **Strength (accessory)**: Accessories must follow the format `[Carga]kg - [Sets]x[Reps]` (e.g., `100kg - 3x10`).
- **Padel (session)**: Padel matches must follow the format `[Result] | [Duration]` where result is `Win`, `Loss`, or `-` (if practice/unknown) and duration is formatted as `Xh` or `Xh Ym` (e.g., `Win | 1h 30m`, `Loss | 1h 30m`, `- | 1h`).

## Late-night attribution rule
When the user reports a completed day between `00:00` and `03:59` local time (GMT-3), assign that training/session to the **previous waking day** unless the user explicitly gives another date.

## Backup rules
- Before every structural edit or append, create a timestamped backup in `backups/`.
- Backup filename format: `performance_log.backup_YYYYMMDDTHHMMSSZ.csv`
- Keep backups append-only on disk for now, but ignore them in git.
- After each write, verify by reading the CSV back from disk.

## Git workflow
- Before any modification, run `git pull --rebase` from the repo root.
- After any modification, verify the affected files, then commit with a contextual message.
- After committing, push to the remote.
- Hermes should use repo-local git author `Hermes Agent <hermes@local>` unless the user asks otherwise.

## Operational rule for Hermes
If Hermes updates the performance log in future sessions, it must write to the canonical path above and then commit the change in the `health` repo.
