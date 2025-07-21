from playwright.sync_api import sync_playwright, TimeoutError
import os
import time
from datetime import datetime

def launch_browser_and_scrape_opportunities(urls, headless=True):
    scraped_data = []
    container_selector = ".usa-card__container"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        page = browser.new_page()

        for url in urls:
            print(f"[INFO] Navigating to: {url}")
            try:
                page.goto(url, wait_until="domcontentloaded", timeout=60000)

                # Scroll down slowly to trigger lazy-loaded elements
                for step in range(5):
                    page.mouse.wheel(0, 1000)
                    time.sleep(1)

                # Give some extra time for JS rendering
                time.sleep(3)

                # DEBUG: Save screenshot for analysis
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                screenshot_path = f"screenshot_{timestamp}.png"
                page.screenshot(path=screenshot_path, full_page=True)
                print(f"[DEBUG] Screenshot saved: {screenshot_path}")

                # Try waiting for cards
                try:
                    page.wait_for_selector(container_selector, timeout=10000)
                except TimeoutError:
                    print("[WARNING] Card container not found even after scroll + delay.")
                    continue

                card_elements = page.query_selector_all(container_selector)
                print(f"[INFO] Found {len(card_elements)} opportunity cards.")

                for elem in card_elements:
                    try:
                        title = elem.query_selector("h3") or elem.query_selector("h2")
                        title = title.inner_text().strip() if title else "N/A"

                        desc = elem.query_selector("p")
                        desc = desc.inner_text().strip() if desc else ""

                        link_elem = elem.query_selector("a")
                        link = link_elem.get_attribute("href") if link_elem else "N/A"

                        scraped_data.append({
                            "title": title,
                            "description": desc,
                            "link": link,
                            "agency": "SAM.gov",
                            "requirements": desc
                        })
                    except Exception as e:
                        print(f"[ERROR] Error parsing element: {e}")

            except Exception as e:
                print(f"[ERROR] Failed to process URL: {url} => {e}")

        browser.close()

    return scraped_data
