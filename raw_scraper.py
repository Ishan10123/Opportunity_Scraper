import json
from playwright.sync_api import sync_playwright
import time
import os
from datetime import datetime
from scraper.logger import setup_logger

logger = setup_logger()

NAICS_URLS = [
    "https://sam.gov/search/?index=opp&page=1&pageSize=25&sort=-modifiedDate&sfm[status][is_active]=true&sfm[simpleSearch][keywordTags][0][value]=541511",
    "https://sam.gov/search/?index=opp&page=1&pageSize=25&sort=-modifiedDate&sfm[status][is_active]=true&sfm[simpleSearch][keywordTags][0][value]=541512",
    "https://sam.gov/search/?index=opp&page=1&pageSize=25&sort=-modifiedDate&sfm[status][is_active]=true&sfm[simpleSearch][keywordTags][0][value]=541513",
    "https://sam.gov/search/?index=opp&page=1&pageSize=25&sort=-modifiedDate&sfm[status][is_active]=true&sfm[simpleSearch][keywordTags][0][value]=541519",
    "https://sam.gov/search/?index=opp&page=1&pageSize=25&sort=-modifiedDate&sfm[status][is_active]=true&sfm[simpleSearch][keywordTags][0][value]=518210",
    "https://sam.gov/search/?index=opp&page=1&pageSize=25&sort=-modifiedDate&sfm[status][is_active]=true&sfm[simpleSearch][keywordTags][0][value]=511210"
]

def scrape_and_save_raw_html(output_file="data/raw_scraped_data.json"):
    logger.info(f"Navigating and scraping {len(NAICS_URLS)} URLs...")
    raw_data = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        for url in NAICS_URLS:
            try:
                logger.info(f"Navigating to: {url}")
                page.goto(url, timeout=60000)
                page.wait_for_timeout(5000)
                page.evaluate("window.scrollBy(0, document.body.scrollHeight);")
                page.wait_for_timeout(3000)

                html_content = page.content()
                text_content = page.inner_text("body")

                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                screenshot_name = f"screenshot_{timestamp}.png"
                page.screenshot(path=screenshot_name)

                raw_data.append({
                    "url": url,
                    "html": html_content,
                    "text": text_content,
                    "timestamp": timestamp,
                })

            except Exception as e:
                logger.error(f"Failed to process URL: {url} => {e}")

        context.close()
        browser.close()

    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(raw_data, f, indent=2, ensure_ascii=False)

    logger.info(f"Raw HTML and text saved to {output_file}")