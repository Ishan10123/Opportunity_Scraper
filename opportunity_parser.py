import os
import json
import re
import logging
from datetime import datetime
from bs4 import BeautifulSoup

DATA_DIR = "data"
AGENCY_PERFORMANCE_FILE = os.path.join(DATA_DIR, "agency_performance.json")
FILTERS_FILE = os.path.join(DATA_DIR, "filters.json")
RAW_HTML_FILE = os.path.join(DATA_DIR, "raw_scraped_data.json")

logger = logging.getLogger(__name__)

def load_json_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def extract_team_size(text):
    match = re.search(r"(?:team\s*size\s*[:\-]?\s*)?(\d{2,3})", text.lower())
    return int(match.group(1)) if match else None

def extract_smart_fit_score(text):
    match = re.search(r"(?:smart\s*fit\s*score\s*[:\-]?\s*)(\d{2,3})", text.lower())
    return int(match.group(1)) if match else None

def classify_opportunity(text, agency, filters, perf_data):
    content = text.lower()

    if any(hw.lower() in content for hw in filters.get("ignore_keywords", [])):
        return "Ignore"

    is_good_agency = agency.strip() in perf_data.get("good_agencies", [])

    best_keywords = filters.get("best_fit_keywords", [])
    moderate_keywords = filters.get("moderate_fit_keywords", [])

    matched_best = any(kw.lower() in content for kw in best_keywords)
    matched_moderate = any(kw.lower() in content for kw in moderate_keywords)

    score = extract_smart_fit_score(content)
    team_size = extract_team_size(content)

    if matched_best and is_good_agency:
        return "Best Fit"
    elif matched_moderate or (score and score > 40) or (team_size and 15 <= team_size <= 40):
        return "Moderate"

    return "Ignore"

def extract_opportunities_from_html(html: str) -> list:
    soup = BeautifulSoup(html, "html.parser")
    results = []
    cards = soup.select(".usa-card__container")

    for card in cards:
        title_elem = card.select_one(".usa-card__heading a")
        description_elem = card.select_one(".usa-card__description")
        agency_elem = card.select_one(".usa-card__footer .usa-card__footer-item")

        title = title_elem.get_text(strip=True) if title_elem else ""
        link = f"https://sam.gov{title_elem['href']}" if title_elem and title_elem.has_attr("href") else ""
        description = description_elem.get_text(strip=True) if description_elem else ""
        agency = agency_elem.get_text(strip=True) if agency_elem else ""

        if title:
            results.append({
                "title": title,
                "description": description,
                "link": link,
                "agency": agency,
                "requirements": description
            })

    return results

def filter_opportunities_from_raw_html():
    logger.info("Loading raw data from raw_scraped_data.json")

    filters = load_json_file(FILTERS_FILE)
    performance = load_json_file(AGENCY_PERFORMANCE_FILE)
    data = load_json_file(RAW_HTML_FILE)

    results = []

    for entry in data:
        text = entry.get("text", "")
        agency = entry.get("agency", "Unknown")

        fit = classify_opportunity(text, agency, filters, performance)
        if fit == "Ignore":
            continue

        structured = {
            "title": entry.get("title", "Untitled"),
            "description": entry.get("description", "N/A"),
            "link": entry.get("link", ""),
            "agency": agency,
            "requirements": text[:500],
            "fit": fit,
            "source": "SAM.gov",
            "timestamp": datetime.now().isoformat()
        }
        results.append(structured)

    logger.info(f"Total filtered opportunities: {len(results)}")
    return results

