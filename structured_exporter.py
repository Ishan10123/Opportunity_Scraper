import os
import csv
import json
from datetime import datetime

def get_timestamp():
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def export_structured_raw_to_csv(filtered_data: list, export_dir: str = "exports"):
    if not filtered_data:
        print("[INFO] No data to export.")
        return None, None

    os.makedirs(export_dir, exist_ok=True)
    timestamp = get_timestamp()
    
    csv_path = os.path.join(export_dir, f"exported_results_{timestamp}.csv")
    json_path = os.path.join(export_dir, f"exported_results_{timestamp}.json")

    with open(csv_path, mode="w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=[
            "title", "description", "link", "agency",
            "requirements", "fit", "source", "timestamp"
        ])
        writer.writeheader()
        for row in filtered_data:
            writer.writerow(row)

    with open(json_path, mode="w", encoding="utf-8") as jsonfile:
        json.dump(filtered_data, jsonfile, indent=4)

    print("[OK] Export completed successfully:")
    print(f" - CSV  : {csv_path}")
    print(f" - JSON : {json_path}")

    return csv_path, json_path
