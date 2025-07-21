import os
import json
from pathlib import Path
import shutil

REQUIRED_DIRS = [
    "scraper", "core", "utils", "data", "exports", "logs", "scheduler"
]

REQUIRED_FILES = [
    "core/raw_scraper.py",
    "core/opportunity_parser.py",
    "scraper/browser_driver.py",
    "utils/structured_exporter.py",
    "data/filters.json",
    "data/agency_performance.json",
    ".env",
    "main.py"
]

def test_directory_structure():
    print("\n[ENV CHECK] Validating folder structure...")
    missing_dirs = [d for d in REQUIRED_DIRS if not Path(d).exists()]
    if missing_dirs:
        print(f"[FAIL] Missing directories: {missing_dirs}")
    else:
        print("[PASS] All required directories exist.")

def test_required_files():
    print("\n[ENV CHECK] Checking required Python and JSON files...")
    missing_files = [f for f in REQUIRED_FILES if not Path(f).exists()]
    if missing_files:
        print(f"[FAIL] Missing files: {missing_files}")
    else:
        print("[PASS] All required files found.")

def test_playwright_installed():
    print("\n[ENV CHECK] Verifying Playwright installation...")
    try:
        import playwright
        print("[PASS] Playwright is installed.")
    except ImportError:
        print("[FAIL] Playwright not found. Run: pip install playwright")

if __name__ == "__main__":
    test_directory_structure()
    test_required_files()
    test_playwright_installed()
