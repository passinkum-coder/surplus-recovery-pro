
import sys
from scrapers.county_scrapers import (
    FultonScraper, GwinnettScraper, CobbScraper, DeKalbScraper,
    CherokeeScraper, ClaytonScraper, HenryScraper,
    ForsythScraper, HallScraper, RichmondScraper
)
from database.supabase_client import upsert_records, get_record_count

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

SCRAPERS = [
    FultonScraper(),
    GwinnettScraper(),
    CobbScraper(),
    DeKalbScraper(),
    CherokeeScraper(),
    ClaytonScraper(),
    HenryScraper(),
    ForsythScraper(),
    HallScraper(),
    RichmondScraper(),
]

def run():
    total_inserted = 0
    errors = []

    logger.info("=== SurplusRecoveryPro Scraper Starting ===")

    for scraper in SCRAPERS:
        logger.info(f"Scraping {scraper.county_name} County...")
        try:
            records = scraper.scrape()
            if records:
                count = upsert_records(records)
                total_inserted += count
                logger.info(f"  ✓ {scraper.county_name}: {count} records loaded")
            else:
                logger.warning(f"  ⚠ {scraper.county_name}: No records found")
        except Exception as e:
            msg = f"{scraper.county_name}: {str(e)}"
            logger.error(f"  ✗ {msg}")
            errors.append(msg)

    logger.info(f"=== Done: {total_inserted} total records inserted ===")

    if errors:
        logger.warning(f"Errors in {len(errors)} counties:")
        for e in errors:
            logger.warning(f"  - {e}")

    total_in_db = get_record_count()
    logger.info(f"Total records now in database: {total_in_db}")

    if len(errors) == len(SCRAPERS):
        sys.exit(1)

if __name__ == "__main__":
    run()
