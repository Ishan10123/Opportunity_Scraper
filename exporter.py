import json
import csv
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Tuple
from scraper.logger import get_logger

logger = get_logger("exporter")

EXPORT_DIR = Path("exports")

def export_opportunities_to_files(opportunities: List[Dict]) -> Tuple[str, str]:
    """
    Exports filtered opportunities to both CSV and JSON.
    Returns: tuple of file paths (csv_file, json_file)
    """
    if not opportunities:
        logger.info("No opportunities to export.")
        return "", ""

    EXPORT_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_file = EXPORT_DIR / f"exported_results_{timestamp}.csv"
    json_file = EXPORT_DIR / f"exported_results_{timestamp}.json"

    try:
        with open(csv_file, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=opportunities[0].keys())
            writer.writeheader()
            writer.writerows(opportunities)
        logger.info(f"Exported opportunities to CSV: {csv_file}")
    except Exception as e:
        logger.error(f"Failed to write CSV: {e}")

    try:
        with open(json_file, mode="w", encoding="utf-8") as f:
            json.dump(opportunities, f, indent=2, ensure_ascii=False)
        logger.info(f"Exported opportunities to JSON: {json_file}")
    except Exception as e:
        logger.error(f"Failed to write JSON: {e}")

    return str(csv_file), str(json_file)

