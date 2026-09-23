#!/usr/bin/env python3
import os
import sys
import csv
import json
import re
from datetime import datetime

# Sanity ranges for biometric plausible values (catch typos, not medical truth)
HRV_MIN, HRV_MAX = 15, 150
RHR_MIN, RHR_MAX = 35, 120
SLEEP_MIN, SLEEP_MAX = 0.0, 24.0


def main():
    # Resolve relative paths to keep the script portable
    script_dir = os.path.dirname(os.path.abspath(__file__))
    schema_path = os.path.normpath(os.path.join(script_dir, "..", "schema", "SCHEMA.json"))
    data_dir = os.path.normpath(os.path.join(script_dir, "..", "data"))

    print(f"🔍 Starting performance log validation...")
    print(f"📂 Schema file: {schema_path}")
    print(f"📂 Data directory: {data_dir}")
    print("-" * 60)

    # 1. Load the schema
    if not os.path.exists(schema_path):
        print(f"❌ ERROR: SCHEMA.json file not found at: {schema_path}")
        sys.exit(1)

    try:
        with open(schema_path, "r", encoding="utf-8") as f:
            schema = json.load(f)
    except Exception as e:
        print(f"❌ ERROR: Could not parse SCHEMA.json: {e}")
        sys.exit(1)

    files_schema = schema.get("files", {})
    errors = []
    session_ids = set()
    referenced_session_ids_in_metrics = set()
    referenced_session_ids_in_matches = set()
    referenced_session_ids_in_reviews = set()
    referenced_match_ids_in_reviews = set()
    match_ids = set()
    player_ids = set()
    referenced_player_ids_in_matches = []
    referenced_player_ids_in_reviews = []
    primary_key_columns = {
        "biometrics.csv": "Date",
        "sessions.csv": "Session_Id",
        "fitness_metrics.csv": "Metric_Id",
        "match_details.csv": "Match_Id",
        "padel_match_reviews.csv": "Review_Id",
        "supplements.csv": "Date",
        "players.csv": "Player_Id",
    }
    seen_primary_keys = {file_name: set() for file_name in files_schema.keys()}

    # 2. Validate columns, formats, and collect Session_Ids
    for file_name, file_spec in files_schema.items():
        csv_path = os.path.join(data_dir, file_name)
        print(f"📄 Validating {file_name}...")

        if not os.path.exists(csv_path):
            errors.append({
                "file": file_name,
                "line": "N/A",
                "col": "Existence",
                "msg": f"File {file_name} is missing from data directory."
            })
            continue

        columns_spec = file_spec.get("columns", [])
        expected_headers = [col["name"] for col in columns_spec]

        with open(csv_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            headers = reader.fieldnames

            if not headers:
                errors.append({
                    "file": file_name,
                    "line": 1,
                    "col": "Headers",
                    "msg": "File is empty or missing headers."
                })
                continue

            if headers != expected_headers:
                errors.append({
                    "file": file_name,
                    "line": 1,
                    "col": "Headers",
                    "msg": f"Headers do not match schema. Expected: {expected_headers}, Found: {headers}"
                })
                continue

            # Check rows
            for line_num, row in enumerate(reader, start=2):
                if None in row:
                    errors.append({
                        "file": file_name,
                        "line": line_num,
                        "col": "Columns",
                        "msg": f"Row has extra columns/fields: {row[None]}"
                    })

                # Validate Date column if present
                if "Date" in row:
                    date_val = row["Date"]
                    if not re.match(r"^\d{4}-\d{2}-\d{2}$", date_val):
                        errors.append({
                            "file": file_name,
                            "line": line_num,
                            "col": "Date",
                            "msg": f"Invalid date format '{date_val}'. Must be YYYY-MM-DD"
                        })
                    else:
                        try:
                            datetime.strptime(date_val, "%Y-%m-%d")
                        except ValueError:
                            errors.append({
                                "file": file_name,
                                "line": line_num,
                                "col": "Date",
                                "msg": f"Non-existent or invalid date '{date_val}'"
                            })

                pk_col = primary_key_columns.get(file_name)
                if pk_col:
                    pk_val = row.get(pk_col)
                    if pk_val in seen_primary_keys[file_name]:
                        errors.append({
                            "file": file_name,
                            "line": line_num,
                            "col": pk_col,
                            "msg": f"Duplicate primary key '{pk_val}'"
                        })
                    else:
                        seen_primary_keys[file_name].add(pk_val)

                # Validate specific columns
                for col in columns_spec:
                    col_name = col["name"]
                    col_type = col["type"]
                    required = col.get("required", False)
                    allowed = col.get("allowed", [])

                    val = row.get(col_name)
                    if required and (val is None or val == ""):
                        errors.append({
                            "file": file_name,
                            "line": line_num,
                            "col": col_name,
                            "msg": "Field is required but missing or empty."
                        })
                        continue

                    # Validate enums
                    if col_type == "enum" and val not in allowed:
                        errors.append({
                            "file": file_name,
                            "line": line_num,
                            "col": col_name,
                            "msg": f"Value '{val}' not allowed. Allowed values: {allowed}"
                        })

                    # Validate integers (or '-')
                    if col_type == "integer" and val != "-":
                        try:
                            int_val = int(val)
                            if int_val < 0:
                                errors.append({
                                    "file": file_name,
                                    "line": line_num,
                                    "col": col_name,
                                    "msg": f"Value '{val}' must be non-negative or '-'"
                                })
                            # Custom range checks
                            if col_name in ["RPE", "Sleep_Quality", "Energy_Level"]:
                                if int_val < 1 or int_val > 10:
                                    errors.append({
                                        "file": file_name,
                                        "line": line_num,
                                        "col": col_name,
                                        "msg": f"Value '{val}' must be between 1 and 10 or '-'"
                                    })
                        except ValueError:
                            errors.append({
                                "file": file_name,
                                "line": line_num,
                                "col": col_name,
                                "msg": f"Value '{val}' must be an integer or '-'"
                            })

                    # Validate decimals (or '-')
                    if col_type == "decimal" and val != "-":
                        try:
                            dec_val = float(val)
                            if dec_val < 0.0:
                                errors.append({
                                    "file": file_name,
                                    "line": line_num,
                                    "col": col_name,
                                    "msg": f"Value '{val}' must be non-negative or '-'"
                                })
                            # Sanity range for sleep hours
                            if col_name == "Sleep_Hours":
                                if not (SLEEP_MIN <= dec_val <= SLEEP_MAX):
                                    errors.append({
                                        "file": file_name,
                                        "line": line_num,
                                        "col": col_name,
                                        "msg": f"Value '{val}' outside plausible range ({SLEEP_MIN}-{SLEEP_MAX}). Possible typo?"
                                    })
                        except ValueError:
                            errors.append({
                                "file": file_name,
                                "line": line_num,
                                "col": col_name,
                                "msg": f"Value '{val}' must be a decimal/float or '-'"
                            })

                    # Sanity ranges for HRV/RHR (after integer type validated above)
                    if col_type == "integer" and val != "-":
                        try:
                            ival = int(val)
                            if col_name == "HRV_Morning" and not (HRV_MIN <= ival <= HRV_MAX):
                                errors.append({
                                    "file": file_name,
                                    "line": line_num,
                                    "col": col_name,
                                    "msg": f"HRV '{val}' outside plausible range ({HRV_MIN}-{HRV_MAX}). Possible typo?"
                                })
                            if col_name == "RHR_Night" and not (RHR_MIN <= ival <= RHR_MAX):
                                errors.append({
                                    "file": file_name,
                                    "line": line_num,
                                    "col": col_name,
                                    "msg": f"RHR '{val}' outside plausible range ({RHR_MIN}-{RHR_MAX}). Possible typo?"
                                })
                        except ValueError:
                            pass  # already reported above

                # Collect and track relationships
                if file_name == "players.csv":
                    pid = row.get("Player_Id")
                    if pid:
                        player_ids.add(pid)
                elif file_name == "sessions.csv":
                    session_ids.add(row.get("Session_Id"))
                elif file_name == "fitness_metrics.csv":
                    referenced_session_ids_in_metrics.add(row.get("Session_Id"))
                elif file_name == "match_details.csv":
                    referenced_session_ids_in_matches.add(row.get("Session_Id"))
                    match_ids.add(row.get("Match_Id"))

                    for col in ["Partner_Id", "Opponent_1_Id", "Opponent_2_Id"]:
                        val = row.get(col)
                        if val and val != "-":
                            referenced_player_ids_in_matches.append((val, line_num, col))

                    match_number = row.get("Match_Number")
                    if match_number != "-":
                        try:
                            if int(match_number) < 1:
                                errors.append({
                                    "file": file_name,
                                    "line": line_num,
                                    "col": "Match_Number",
                                    "msg": f"Match_Number '{match_number}' must be >= 1"
                                })
                        except ValueError:
                            # integer validation is already handled above
                            pass
                elif file_name == "padel_match_reviews.csv":
                    referenced_session_ids_in_reviews.add(row.get("Session_Id"))
                    review_match_id = row.get("Match_Id")
                    if review_match_id != "-":
                        referenced_match_ids_in_reviews.add(review_match_id)
                    p_id = row.get("Partner_Id")
                    if p_id and p_id != "-":
                        referenced_player_ids_in_reviews.append((p_id, line_num, "Partner_Id"))

                    for score_col in [
                        "Drive_Intervention_Score",
                        "Net_Presence_Score",
                        "Volley_Damage_Score",
                        "Tactical_Influence_Score",
                        "Mental_Composure_Score",
                    ]:
                        score_val = row.get(score_col)
                        if score_val != "-":
                            try:
                                score_num = int(score_val)
                                if score_num < 1 or score_num > 5:
                                    errors.append({
                                        "file": file_name,
                                        "line": line_num,
                                        "col": score_col,
                                        "msg": f"Value '{score_val}' must be between 1 and 5 or '-'"
                                    })
                            except ValueError:
                                errors.append({
                                    "file": file_name,
                                    "line": line_num,
                                    "col": score_col,
                                    "msg": f"Value '{score_val}' must be an integer 1-5 or '-'"
                                })

    # 3. Validate Referential Integrity (Foreign Keys)
    print("🔗 Validating relational integrity...")
    
    # Check that every session referenced in metrics exists in sessions.csv
    for sid in referenced_session_ids_in_metrics:
        if sid not in session_ids:
            errors.append({
                "file": "fitness_metrics.csv",
                "line": "N/A",
                "col": "Session_Id",
                "msg": f"Foreign Key Error: Session_Id '{sid}' referenced in fitness_metrics does not exist in sessions.csv"
            })

    # Check that every session referenced in match details exists in sessions.csv
    for sid in referenced_session_ids_in_matches:
        if sid not in session_ids:
            errors.append({
                "file": "match_details.csv",
                "line": "N/A",
                "col": "Session_Id",
                "msg": f"Foreign Key Error: Session_Id '{sid}' referenced in match_details does not exist in sessions.csv"
            })

    # Check that every session referenced in padel reviews exists in sessions.csv
    for sid in referenced_session_ids_in_reviews:
        if sid not in session_ids:
            errors.append({
                "file": "padel_match_reviews.csv",
                "line": "N/A",
                "col": "Session_Id",
                "msg": f"Foreign Key Error: Session_Id '{sid}' referenced in padel_match_reviews does not exist in sessions.csv"
            })

    # Check that every match referenced in padel reviews exists in match_details.csv
    for mid in referenced_match_ids_in_reviews:
        if mid not in match_ids:
            errors.append({
                "file": "padel_match_reviews.csv",
                "line": "N/A",
                "col": "Match_Id",
                "msg": f"Foreign Key Error: Match_Id '{mid}' referenced in padel_match_reviews does not exist in match_details.csv"
            })

    # Check that every player referenced in match_details exists in players.csv
    for pid, line_num, col in referenced_player_ids_in_matches:
        if pid not in player_ids:
            errors.append({
                "file": "match_details.csv",
                "line": line_num,
                "col": col,
                "msg": f"Foreign Key Error: Player_Id '{pid}' referenced in match_details does not exist in players.csv"
            })

    # Check that every player referenced in padel reviews exists in players.csv
    for pid, line_num, col in referenced_player_ids_in_reviews:
        if pid not in player_ids:
            errors.append({
                "file": "padel_match_reviews.csv",
                "line": line_num,
                "col": col,
                "msg": f"Foreign Key Error: Player_Id '{pid}' referenced in padel_match_reviews does not exist in players.csv"
            })

    # 3.5 Validate Match_Id invariant and sequential Match_Number per session
    print("🎯 Validating Match_Id invariant and Match_Number sequence...")

    # Collect match rows with line numbers
    match_rows = []  # (session_id, match_id, match_number, line_num)
    with open(os.path.join(data_dir, "match_details.csv"), "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for line_num, row in enumerate(reader, start=2):
            match_rows.append((
                row.get("Session_Id"),
                row.get("Match_Id"),
                row.get("Match_Number"),
                line_num,
            ))

    # Build per-session list of (match_number, match_id, line_num) preserving file order
    per_session = {}
    for sid, mid, mn, ln in match_rows:
        per_session.setdefault(sid, []).append((mn, mid, ln))

    for sid, entries in per_session.items():
        # 1. Match_Id must equal Session_Id + "-m" + Match_Number
        for mn, mid, ln in entries:
            expected = f"{sid}-m{mn}"
            if mid != expected:
                errors.append({
                    "file": "match_details.csv",
                    "line": ln,
                    "col": "Match_Id",
                    "msg": f"Match_Id '{mid}' no coincide con Session_Id+'-m'+Match_Number (esperado '{expected}')"
                })
        # 2. Match_Number must be a strict ascending sequence 1,2,3...
        try:
            nums = [int(mn) for mn, _, _ in entries]
        except (ValueError, TypeError):
            continue  # integer tipo already reported above
        if nums != list(range(1, len(nums) + 1)):
            errors.append({
                "file": "match_details.csv",
                "line": entries[0][2],
                "col": "Match_Number",
                "msg": f"Match_Number en sesión '{sid}' no es secuencia 1..{len(nums)} (encontrado {nums})"
            })

    # 3.6 Validate that Session_Id embeds a date matching the row's Date (sessions)
    #     and that Match_Id's date prefix matches its Session_Id's date (match_details)
    print("📅 Validating embedded dates in Session_Id / Match_Id...")

    # sessions.csv: Session_Id should start with the row's Date
    with open(os.path.join(data_dir, "sessions.csv"), "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for line_num, row in enumerate(reader, start=2):
            sid = row.get("Session_Id")
            date_val = row.get("Date")
            if sid and date_val and not sid.startswith(date_val):
                errors.append({
                    "file": "sessions.csv",
                    "line": line_num,
                    "col": "Session_Id",
                    "msg": f"Session_Id '{sid}' no empieza con la fecha de la fila '{date_val}'"
                })

    # match_details.csv: Match_Id date prefix must equal Session_Id date prefix
    with open(os.path.join(data_dir, "match_details.csv"), "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for line_num, row in enumerate(reader, start=2):
            sid = row.get("Session_Id")
            mid = row.get("Match_Id")
            if sid and mid:
                sid_date = sid[:10]
                mid_date = mid[:10]
                if sid_date != mid_date:
                    errors.append({
                        "file": "match_details.csv",
                        "line": line_num,
                        "col": "Match_Id",
                        "msg": f"Fecha en Match_Id '{mid}' ({mid_date}) no coincide con la de Session_Id '{sid}' ({sid_date})"
                    })

        # 4 # 4. Print Summary and Exit
    print("-" * 60)
    print(f"📊 Validation Summary:")
    print(f"   - Total errors found: {len(errors)}")
    print("-" * 60)

    if errors:
        print("❌ DETAILED ERRORS FOUND:\n")
        for err in errors:
            print(f"📍 File: {err['file']} | Line {err['line']} | Column: {err['col']}")
            print(f"   ⚠️ {err['msg']}")
            print("-" * 40)
        sys.exit(1)
    else:
        print("✅ All CSV files are 100% valid and consistent with the new Multi-CSV schema!")
        sys.exit(0)

if __name__ == "__main__":
    main()
