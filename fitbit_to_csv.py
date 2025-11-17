#!/usr/bin/env python3
import os
import sys
import glob
import json
import csv
from datetime import datetime

def parse_date(d):
    # Input like "07/15/24" -> "2024-07-15"
    dt = datetime.strptime(d, "%m/%d/%y").date()
    return dt.strftime("%Y-%m-%d")

def main(folder):
    # date_str -> {"weight": float, "bmi": float|None, "fat": float|None}
    by_date = {}

    json_paths = glob.glob(os.path.join(folder, "*.json"))
    for path in json_paths:
        with open(path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                continue  # skip broken files

        # Expect each file to be a list of entries like your sample
        if isinstance(data, dict):
            # if some files wrap data differently, try to pull a list out
            # e.g., {"weight": [...]} or similar
            for key in ("weight", "weights", "data", "items"):
                if key in data and isinstance(data[key], list):
                    data = data[key]
                    break

        if not isinstance(data, list):
            continue

        for entry in data:
            if not isinstance(entry, dict):
                continue

            date_raw = entry.get("date")
            if not date_raw:
                continue

            date_str = parse_date(date_raw)

            w = entry.get("weight")
            bmi = entry.get("bmi")
            fat = entry.get("fat")  # adjust if your field has another name

            if w is None:
                # if weight missing, only store if we have nothing yet
                if date_str not in by_date:
                    by_date[date_str] = {"weight": None, "bmi": bmi, "fat": fat}
                else:
                    # fill bmi/fat if we don't have them yet
                    cur = by_date[date_str]
                    if cur.get("bmi") is None and bmi is not None:
                        cur["bmi"] = bmi
                    if cur.get("fat") is None and fat is not None:
                        cur["fat"] = fat
                continue

            # First entry for this date
            if date_str not in by_date:
                by_date[date_str] = {"weight": w, "bmi": bmi, "fat": fat}
            else:
                cur = by_date[date_str]
                cur_w = cur.get("weight")
                # keep the lowest weight; overwrite bmi/fat with the chosen record
                if cur_w is None or w < cur_w:
                    cur["weight"] = w
                    cur["bmi"] = bmi
                    cur["fat"] = fat
                else:
                    # even if this weight is higher, we can optionally
                    # fill missing bmi/fat from it (comment out if unwanted)
                    if cur.get("bmi") is None and bmi is not None:
                        cur["bmi"] = bmi
                    if cur.get("fat") is None and fat is not None:
                        cur["fat"] = fat

    # Write CSV
    out_path = os.path.join(folder, "fitbit_weights.csv")
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["date", "lbs", "bmi", "fat"])

        for date_str in sorted(by_date.keys()):
            rec = by_date[date_str]
            w = rec.get("weight")
            bmi = rec.get("bmi")
            fat = rec.get("fat")

            writer.writerow([
                date_str,
                "" if w is None else w,
                "" if bmi is None else bmi,
                "" if fat is None else fat
            ])

    print(f"Wrote {out_path}")

if __name__ == "__main__":
    folder = sys.argv[1] if len(sys.argv) > 1 else "."
    main(folder)
