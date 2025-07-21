import json
import logging
from datetime import datetime
from pathlib import Path
from playwright.sync_api import sync_playwright

logger = logging.getLogger(__name__)

NAICS_CODES = ["541511", "541512", "541513", "541519", "518210", "511210"]
BASE_URL_TEMPLATE = (
    "https://sam.gov/search/?index=opp&page={page}&pageSize=25&sort=-modifiedDate"
    "&sfm[status][is_active]=true"
    "&sfm[simpleSearch][keywordTags][0][value]={naics}"
)

def scrape_and_save_raw_html(output_file="data/raw_scraped_data.json"):
    results = []
    debug_dir = Path("debug")
    debug_dir.mkdir(exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=250)
        context = browser.new_context(viewport={"width": 1280, "height": 800})
        page = context.new_page()

        for naics in NAICS_CODES:
            page_num = 1
            logger.info(f"Scraping NAICS: {naics}")

            while True:
                url = BASE_URL_TEMPLATE.format(page=page_num, naics=naics)
                logger.info(f"Navigating to page {page_num}: {url}")
                page.goto(url, timeout=60000)

                page.wait_for_timeout(4000)
                page.keyboard.press("End")
                page.wait_for_timeout(4000)

                try:
                    page.wait_for_selector(".search-result-card", timeout=8000)
                    cards = page.query_selector_all(".search-result-card")
                except:
                    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                    logger.warning(f"[{naics} - Page {page_num}] No result cards. Saving debug files.")
                    page.screenshot(path=str(debug_dir / f"{naics}_p{page_num}_{ts}.png"))
                    html = page.content()
                    with open(debug_dir / f"{naics}_p{page_num}_{ts}.html", "w", encoding="utf-8") as f:
                        f.write(html)
                    break

                if not cards:
                    logger.info(f"No cards found on page {page_num} — stop.")
                    break

                logger.info(f"Found {len(cards)} cards on page {page_num}")

                for card in cards:
                    try:
                        title_el = card.query_selector("h3 a")
                        title = title_el.inner_text().strip() if title_el else "Untitled"
                        link = title_el.get_attribute("href") if title_el else ""
                        if link and not link.startswith("http"):
                            link = "https://sam.gov" + link

                        desc_el = card.query_selector("p")
                        description = desc_el.inner_text().strip() if desc_el else ""

                        agency_el = card.query_selector(".search-result-subtitle span")
                        agency = agency_el.inner_text().strip() if agency_el else "Unknown"

                        raw_text = card.inner_text().strip()

                        results.append({
                            "title": title,
                            "description": description,
                            "link": link,
                            "agency": agency,
                            "text": raw_text
                        })
                    except Exception as e:
                        logger.warning(f"Parse error on page {page_num}, NAICS {naics}: {e}")

                page_num += 1

        context.close()
        browser.close()

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    logger.info(f"Scraping complete. {len(results)} opportunities saved to {output_file}")

