#!/usr/bin/env python3
"""Compute the daily readiness band (green/yellow/red) from biometrics.csv.

Rule (READINESS_RULES.md):
- The WORST signal wins.
- Green:  HRV/RHR ~ baseline, sleep >= 7h, energy ok
- Yellow: HRV down 5-10% OR sleep 6-7h OR energy 4-5
- Red:    HRV down >=10% vs 7-day baseline for >=3 consecutive days AND sleep <7h

Placeholders (`-`) are unknown and ignored, never treated as zero or as good.
"""
import argparse
import csv
import sys
from datetime import date, datetime, timedelta

BASELINE_DAYS = 7
RED_HRV_DROP = 0.10       # 10%
RED_CONSECUTIVE_DAYS = 3
YELLOW_HRV_DROP = 0.05    # 5%
RED_SLEEP_HOURS = 7.0
YELLOW_SLEEP_HI, YELLOW_SLEEP_LO = 7.0, 6.0
YELLOW_ENERGY_LO, YELLOW_ENERGY_HI = 4, 5


def parse_float(v):
    if v is None or str(v).strip() in ("-", ""):
        return None
    try:
        return float(v)
    except ValueError:
        return None


def parse_int(v):
    f = parse_float(v)
    return int(f) if f is not None else None


def load_biometrics(path):
    rows = []
    with open(path, newline="", encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            rows.append({
                "date": datetime.strptime(r["Date"].strip(), "%Y-%m-%d").date(),
                "sleep": parse_float(r.get("Sleep_Hours")),
                "hrv": parse_int(r.get("HRV_Morning")),
                "rhr": parse_int(r.get("RHR_Night")),
                "sleep_q": parse_int(r.get("Sleep_Quality")),
                "energy": parse_int(r.get("Energy_Level")),
            })
    return sorted(rows, key=lambda r: r["date"])


def baseline_hrv(rows, idx):
    """Mean HRV over the up-to-BASELINE_DAYS valid values strictly before idx."""
    vals = []
    for r in rows[max(0, idx - BASELINE_DAYS):idx]:
        if r["hrv"] is not None:
            vals.append(r["hrv"])
    if not vals:
        return None
    return sum(vals) / len(vals)


def compute_bands(rows):
    """Return a dict date -> band reason. Band uses WORST signal wins."""
    out = {}
    red_streak = 0
    for i, r in enumerate(rows):
        base = baseline_hrv(rows, i)
        hrv_drop = None
        if r["hrv"] is not None and base:
            hrv_drop = (base - r["hrv"]) / base  # positive = drop

        sleep_bad = r["sleep"] is not None and r["sleep"] < RED_SLEEP_HOURS
        hrv_red = hrv_drop is not None and hrv_drop >= RED_HRV_DROP
        hrv_yellow = hrv_drop is not None and YELLOW_HRV_DROP <= hrv_drop < RED_HRV_DROP
        sleep_yellow = r["sleep"] is not None and YELLOW_SLEEP_LO <= r["sleep"] < YELLOW_SLEEP_HI
        energy_yellow = r["energy"] is not None and YELLOW_ENERGY_LO <= r["energy"] <= YELLOW_ENERGY_HI

        # Red streak: HRV red consecutively (dates must be consecutive days)
        if hrv_red:
            red_streak += 1
        else:
            red_streak = 0

        reasons = []
        if red_streak >= RED_CONSECUTIVE_DAYS and sleep_bad:
            out[r["date"]] = ("red", "HRV↓≥10% ×%dd y sueño <7h" % red_streak)
            continue

        # Green check first (all clear)
        if not hrv_red and not hrv_yellow and not sleep_yellow and not energy_yellow:
            out[r["date"]] = ("green", "señales ok")
            continue

        # Yellow (worst of the partial signals)
        band = "yellow"
        if hrv_red:
            reasons.append("HRV↓%.0f%%" % (hrv_drop * 100))
        elif hrv_yellow:
            reasons.append("HRV↓%.0f%%" % (hrv_drop * 100))
        if sleep_yellow:
            reasons.append("sueño %.1fh" % r["sleep"])
        if energy_yellow:
            reasons.append("energía %d" % r["energy"])
        out[r["date"]] = (band, ", ".join(reasons) if reasons else "señal parcial")
    return out


def main():
    p = argparse.ArgumentParser(description="Readiness band from biometrics.csv")
    p.add_argument("--path", default="performance/data/biometrics.csv")
    p.add_argument("--date", help="YYYY-MM-DD to evaluate (default: last row)")
    args = p.parse_args()

    try:
        rows = load_biometrics(args.path)
    except FileNotFoundError:
        sys.exit(f"ERROR: no se encontró {args.path}")
    if not rows:
        sys.exit("ERROR: sin datos en biometrics.csv")

    bands = compute_bands(rows)

    target = datetime.strptime(args.date, "%Y-%m-%d").date() if args.date else rows[-1]["date"]
    if target not in bands:
        # No data that day -> no band computable
        print(f"{target}: sin datos suficientes para evaluar")
        return

    emoji = {"green": "🟢", "yellow": "🟡", "red": "🔴"}
    band, reason = bands[target]
    print(f"{target}: {emoji[band]} {band.upper()} — {reason}")

    # Summary of last 7 evaluable days for context
    print("\nÚltimos días evaluables:")
    for r in rows[-7:]:
        d = r["date"]
        b, why = bands.get(d, ("-", "sin señal"))
        e = emoji.get(b, "⚪")
        print(f"  {d}: {e} {b.upper():6} {why}  (HRV={r['hrv']}, RHR={r['rhr']}, sueño={r['sleep']})")


if __name__ == "__main__":
    main()
