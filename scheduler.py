import subprocess
import time
import logging
from datetime import datetime

LOG_FILE = "logs/scheduler.log"

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def run_pipeline():
    logging.info("Triggering main.py scraping pipeline...")
    try:
        result = subprocess.run(["python", "main.py"], capture_output=True, text=True)
        logging.info(result.stdout)
        if result.stderr:
            logging.error(result.stderr)
    except Exception as e:
        logging.error(f"Error running main.py: {e}")

def schedule_every(minutes: int = 30):
    logging.info(f"Starting scheduler to run every {minutes} minutes.")
    while True:
        start_time = datetime.now()
        run_pipeline()
        elapsed = (datetime.now() - start_time).total_seconds()
        sleep_duration = max(60 * minutes - elapsed, 0)
        logging.info(f"Waiting {sleep_duration / 60:.1f} minutes before next run.\n")
        time.sleep(sleep_duration)

if __name__ == "__main__":
    try:
        schedule_every(minutes=30)
    except KeyboardInterrupt:
        logging.info("Scheduler interrupted manually. Exiting...")
