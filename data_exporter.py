import csv
import json
import os
from datetime import datetime
from typing import List, Dict

EXPORT_DIR = "exports"

def ensure_export_dir():
    os.makedirs(EXPORT_DIR, exist_ok=True)

def generate_export_filenames():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_filename = os.path.join(EXPORT_DIR, f"exported_results_{timestamp}.csv")
    json_filename = os.path.join(EXPORT_DIR, f"exported_results_{timestamp}.json")
    return csv_filename, json_filename

def export_to_csv(opportunities: List[Dict], csv_path: str):
    if not opportunities:
        print("[INFO] No opportunities to export to CSV.")
        return

    fieldnames = [
        "title", "description", "link", "agency",
        "requirements", "fit", "source", "timestamp"
    ]

    with open(csv_path, mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for opp in opportunities:
            writer.writerow({key: opp.get(key, "") for key in fieldnames})

def export_to_json(opportunities: List[Dict], json_path: str):
    if not opportunities:
        print("[INFO] No opportunities to export to JSON.")
        return

    with open(json_path, mode='w', encoding='utf-8') as jsonfile:
        json.dump(opportunities, jsonfile, indent=4, ensure_ascii=False)

def export_all(opportunities: List[Dict]):
    ensure_export_dir()
    csv_path, json_path = generate_export_filenames()
    export_to_csv(opportunities, csv_path)
    export_to_json(opportunities, json_path)
    print(f"\n Export completed:")
    print(f" CSV : {csv_path}")
    print(f" JSON: {json_path}")
    return csv_path, json_path

