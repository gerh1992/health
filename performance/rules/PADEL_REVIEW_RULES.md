# Padel review storage rules

## Purpose
This file documents the canonical storage model for tactical and reflective padel reviews.

The goal is not only post-match catharsis, but durable pattern detection across:
- role (`Drive` / `Reves`),
- partner level asymmetry,
- tournament vs friendly context,
- recurring tactical frustrations,
- perceived influence on the match,
- and whether the next experiment actually changes outcomes.

## Canonical path
- Structured review log: `performance/data/padel_match_reviews.csv`

Optional future layer for long-form narrative notes:
- `performance/notes/padel/YYYY-MM-DD-<slug>.md`

The CSV is the canonical source of truth for cross-match pattern analysis.
Long-form notes are optional supporting context.

## Ingestion model
Preferred user input is free text.
Hermes should translate that free text into structured review fields.

Workflow:
1. user describes the match in natural language,
2. Hermes infers all fields that can be inferred safely,
3. Hermes asks direct follow-up questions only for fields that materially improve later pattern analysis,
4. Hermes writes the structured row(s) to `padel_match_reviews.csv`,
5. Hermes keeps unknown values explicit with `-` rather than inventing them.

## Row granularity
Default granularity is **one review row per match that produced tactical learning**.

That means:
- a multi-match tournament day can have multiple review rows,
- several review rows may point to the same `Session_Id`,
- if the user only gives a session-level reflection rather than match-specific detail, Hermes may still create multiple rows when distinct matches clearly carried different learning value.

## Foreign-key linkage
Each review row should link back to the objective match log whenever possible:
- `Session_Id` → parent row in `sessions.csv`
- `Match_Id` → individual match row in `match_details.csv`

If a review is session-level and cannot yet be tied to a specific match, `Match_Id` may be `-` until clarified.

## Field semantics
- `Review_Id`: Primary key. Format: `r-YYYY-MM-DD-<session or match suffix>`.
- `Date`: Date of the reviewed match.
- `Session_Id`: Parent performance session.
- `Match_Id`: Specific match row in `match_details.csv` or `-`.
- `Sport`: currently `Padel`.
- `Role`: `Drive`, `Reves`, or `-`.
- `Partner_Name`: teammate name or `-`.
- `Partner_Level_Relative`: `Lower`, `Similar`, `Higher`, or `-`.
- `Opponent_Level_Notes`: short free text if relevant, else `-`.
- `Match_Context`: `Tournament`, `Friendly`, `Practice`, or `-`.
- `Result`: `Win`, `Loss`, or `-`.
- `Emotional_Tone`: short label such as `Frustrated`, `Calm`, `Confident`, `Tilted`, `Satisfied`, or `-`.
- `Main_Frustration`: the key emotional or competitive complaint.
- `Main_Tactical_Problem`: the main tactical pattern that limited performance.
- `What_I_Did_Well`: short summary of strengths shown.
- `What_I_Did_Poorly`: short summary of weaknesses shown.
- `Adjustment_I_Needed`: the tactical correction that was needed.
- `Adjustment_I_Tried`: what was actually attempted during the match, or `-`.
- `Next_Experiment`: the next thing to test in future matches.
- `Drive_Intervention_Score`: integer `1-5` or `-`.
- `Net_Presence_Score`: integer `1-5` or `-`.
- `Volley_Damage_Score`: integer `1-5` or `-`.
- `Tactical_Influence_Score`: integer `1-5` or `-`.
- `Mental_Composure_Score`: integer `1-5` or `-`.
- `Key_Pattern_Tags`: pipe-delimited pattern tags.
- `Free_Notes`: short context that does not fit elsewhere.

## Scale rules for scores
Use `1-5`:
- `1` = clearly poor / absent
- `2` = below desired standard
- `3` = mixed / functional but limited
- `4` = good and useful
- `5` = clear strength / high impact

Do not pretend precision that the user did not express.
If score confidence is too low, use `-` and ask later if needed.

## Tag rules
Use compact, reusable tags separated by `|`.
Prefer stable vocabulary over novel tags every time.

Examples:
- `drive`
- `reves`
- `partner-lower`
- `partner-similar`
- `partner-higher`
- `tournament`
- `friendly`
- `good-defense`
- `low-influence`
- `late-adjustment`
- `net-passive`
- `good-backhand-volley`
- `frustration-partner-targeted`
- `did-not-press-enough`

## Retrieval intent
This dataset should make future questions easy, such as:
- when do I most often feel low influence as drive?
- what patterns repeat with lower-level revés partners?
- what experiments have I tried before in similar situations?
- do my tournament frustrations differ from friendlies?
- when I report strong defense, do I also report low tactical influence?

## Operational rule for Hermes
When the user gives a padel reflection:
1. check whether an objective match already exists in `sessions.csv` / `match_details.csv`,
2. create or update the review row(s),
3. avoid duplicating review rows for the same match unless updating materially,
4. preserve unknowns with `-`,
5. validate and commit if the canonical repo is being changed.
