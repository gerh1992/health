#!/usr/bin/env python3
import os
import sys
import csv
import json
import re
from datetime import datetime

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
    primary_key_columns = {
        "biometrics.csv": "Date",
        "sessions.csv": "Session_Id",
        "fitness_metrics.csv": "Metric_Id",
        "match_details.csv": "Match_Id",
        "supplements.csv": "Date",
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
                            int(val)
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
                            float(val)
                        except ValueError:
                            errors.append({
                                "file": file_name,
                                "line": line_num,
                                "col": col_name,
                                "msg": f"Value '{val}' must be a decimal/float or '-'"
                            })

                # Collect and track relationships
                if file_name == "sessions.csv":
                    session_ids.add(row.get("Session_Id"))
                elif file_name == "fitness_metrics.csv":
                    referenced_session_ids_in_metrics.add(row.get("Session_Id"))
                elif file_name == "match_details.csv":
                    referenced_session_ids_in_matches.add(row.get("Session_Id"))

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

    # 4. Print Summary and Exit
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
