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
    csv_path = os.path.normpath(os.path.join(script_dir, "..", "data", "performance_log.csv"))

    print(f"🔍 Starting performance log validation...")
    print(f"📂 Schema file: {schema_path}")
    print(f"📂 Data file: {csv_path}")
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

    # 2. Load and parse the CSV
    if not os.path.exists(csv_path):
        print(f"❌ ERROR: CSV file not found at: {csv_path}")
        sys.exit(1)

    # Define schema rules for fast lookup
    columns_spec = schema.get("columns", [])
    expected_headers = [col["name"] for col in columns_spec]
    volume_rules = schema.get("volume_detail_rules", {})

    errors = []
    rows_checked = 0

    with open(csv_path, "r", encoding="utf-8") as f:
        # Detect CSV dialect to ensure correct reading
        reader = csv.DictReader(f)
        headers = reader.fieldnames

        if not headers:
            print("❌ ERROR: The CSV file is empty or has no headers.")
            sys.exit(1)

        # Validate CSV headers
        if headers != expected_headers:
            errors.append({
                "line": 1,
                "date": "N/A",
                "col": "Headers",
                "msg": f"CSV headers do not match schema.\nExpected: {expected_headers}\nFound: {headers}"
            })
            # If headers are wrong, we cannot reliably continue validation
            print_summary_and_exit(errors, rows_checked)

        # Validate row by row (lines in DictReader start at 2 due to headers)
        for line_num, row in enumerate(reader, start=2):
            rows_checked += 1
            date_val = row.get("Date", "Unknown")

            # A. Validate Date
            if "Date" in row:
                if not re.match(r"^\d{4}-\d{2}-\d{2}$", row["Date"]):
                    errors.append({
                        "line": line_num,
                        "date": date_val,
                        "col": "Date",
                        "msg": f"Invalid date format '{row['Date']}'. Must be YYYY-MM-DD"
                    })
                else:
                    try:
                        datetime.strptime(row["Date"], "%Y-%m-%d")
                    except ValueError:
                        errors.append({
                            "line": line_num,
                            "date": date_val,
                            "col": "Date",
                            "msg": f"Non-existent or invalid date '{row['Date']}'"
                        })

            # B. Validate Category (Enum)
            category_spec = next((c for c in columns_spec if c["name"] == "Category"), None)
            if category_spec and "Category" in row:
                allowed_categories = category_spec.get("allowed", [])
                if row["Category"] not in allowed_categories:
                    errors.append({
                        "line": line_num,
                        "date": date_val,
                        "col": "Category",
                        "msg": f"Category '{row['Category']}' not allowed. Allowed values: {allowed_categories}"
                    })

            # C. Validate Entry_Type (Enum)
            entry_type_spec = next((c for c in columns_spec if c["name"] == "Entry_Type"), None)
            if entry_type_spec and "Entry_Type" in row:
                allowed_entry_types = entry_type_spec.get("allowed", [])
                if row["Entry_Type"] not in allowed_entry_types:
                    errors.append({
                        "line": line_num,
                        "date": date_val,
                        "col": "Entry_Type",
                        "msg": f"Entry type '{row['Entry_Type']}' not allowed. Allowed values: {allowed_entry_types}"
                    })

            # D. Validate Session_Tag (Enum)
            session_tag_spec = next((c for c in columns_spec if c["name"] == "Session_Tag"), None)
            if session_tag_spec and "Session_Tag" in row:
                allowed_tags = session_tag_spec.get("allowed", [])
                if row["Session_Tag"] not in allowed_tags:
                    errors.append({
                        "line": line_num,
                        "date": date_val,
                        "col": "Session_Tag",
                        "msg": f"Session tag '{row['Session_Tag']}' not allowed. Allowed values: {allowed_tags}"
                    })

            # E. Validate RPE (Num/String or '-')
            if "RPE" in row:
                rpe_val = row["RPE"]
                if rpe_val != "-":
                    # Accept simple number or fraction (e.g. 8, 8/10)
                    if not re.match(r"^\d+(?:\/\d+)?$", rpe_val):
                        errors.append({
                            "line": line_num,
                            "date": date_val,
                            "col": "RPE",
                            "msg": f"Invalid RPE '{rpe_val}'. Must be an integer, a fraction (e.g. 8/10), or '-'"
                        })

            # F. Validate HRV_Morning
            if "HRV_Morning" in row:
                hrv_val = row["HRV_Morning"]
                if hrv_val != "-" and not hrv_val.isdigit():
                    errors.append({
                        "line": line_num,
                        "date": date_val,
                        "col": "HRV_Morning",
                        "msg": f"Invalid HRV '{hrv_val}'. Must be an integer or '-'"
                    })

            # G. Validate RHR_Night
            if "RHR_Night" in row:
                rhr_val = row["RHR_Night"]
                if rhr_val != "-" and not rhr_val.isdigit():
                    errors.append({
                        "line": line_num,
                        "date": date_val,
                        "col": "RHR_Night",
                        "msg": f"Invalid RHR '{rhr_val}'. Must be an integer or '-'"
                    })

            # H. Validate Volume_Detail based on Category + Entry_Type rules
            if "Volume_Detail" in row and "Category" in row and "Entry_Type" in row:
                cat = row["Category"]
                etype = row["Entry_Type"]
                volume_val = row["Volume_Detail"]

                cat_rules = volume_rules.get(cat, {})
                rule = cat_rules.get(etype)

                if rule:
                    pattern = rule.get("pattern")
                    if pattern:
                        if not re.match(pattern, volume_val):
                            errors.append({
                                "line": line_num,
                                "date": date_val,
                                "col": "Volume_Detail",
                                "msg": f"Inconsistent format in Volume_Detail for {cat} ({etype}): '{volume_val}'.\n   Expected detail: {rule.get('notes')}"
                            })

    print_summary_and_exit(errors, rows_checked)

def print_summary_and_exit(errors, rows_checked):
    print(f"📊 Validation Summary:")
    print(f"   - Processed rows: {rows_checked}")
    print(f"   - Errors found: {len(errors)}")
    print("-" * 60)

    if errors:
        print("❌ DETAILED ERRORS FOUND:\n")
        for err in errors:
            print(f"📍 Line {err['line']} | Date: {err['date']} | Column: {err['col']}")
            print(f"   ⚠️ {err['msg']}")
            print("-" * 40)
        sys.exit(1)
    else:
        print("✅ The CSV file is 100% valid and consistent with the schema!")
        sys.exit(0)

if __name__ == "__main__":
    main()
