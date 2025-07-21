import os
import sys
from datetime import datetime

sys.path.append(os.path.abspath("."))

from core.raw_scraper import scrape_and_save_raw_html
from core.opportunity_parser import filter_opportunities_from_raw_html
from scraper.logger import setup_logger
from utils.structured_exporter import export_structured_raw_to_csv
from utils.email_dispatcher import send_email_with_attachments

logger = setup_logger()

def main():
    logger.info("Starting SAM.gov scraping and filtering pipeline")

    raw_output_path = os.path.join("data", "raw_scraped_data.json")
    logger.info("Scraping multiple NAICS-based URLs...")
    scrape_and_save_raw_html(output_file=raw_output_path)

    logger.info("Loading and filtering scraped data...")
    filtered_opportunities = filter_opportunities_from_raw_html()

    if filtered_opportunities:
        logger.info(f"Filtered opportunities: {len(filtered_opportunities)}")
    else:
        logger.info("No relevant opportunities matched filters.")

    csv_file, json_file = export_structured_raw_to_csv(
        filtered_data=filtered_opportunities,
        export_dir="exports"
    )

    if filtered_opportunities:
        subject = f"GovScraper Report {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        body = "Please find attached the filtered opportunity report from SAM.gov."
        send_email_with_attachments(subject, body, [csv_file, json_file])
        logger.info("Email with attachments sent.")
    else:
        logger.info("No email sent since no matching opportunities.")

if __name__ == "__main__":
    main()

