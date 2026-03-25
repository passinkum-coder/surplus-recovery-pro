import logging
import sys
from scrapers.county_scrapers import (
    FultonScraper, GwinnettScraper, CobbScraper, DeKalbScraper,
    CherokeeScraper, ClaytonScraper, HenryScraper,
    ForsythScraper, HallScraper, RichmondScraper
)
from scrapers.florida_scrapers import (
    MiamiDadeScraper, BrowardScraper, PalmBeachScraper,
    HillsboroughScraper, OrangeCountyFLScraper
)
from scrapers.texas_scrapers import (
    HarrisScraper, DallasScraper, TarrantScraper,
    BexarScraper, TravisScraper
)
from database.supabase_client import upsert_records, get_record_count
from alert_system import check_and_create_alerts

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

GEORGIA_SCRAPERS = [
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

FLORIDA_SCRAPERS = [
    MiamiDadeScraper(),
    BrowardScraper(),
    PalmBeachScraper(),
    HillsboroughScraper(),
    OrangeCountyFLScraper(),
]

TEXAS_SCRAPERS = [
    HarrisScraper(),
    DallasScraper(),
    TarrantScraper(),
    BexarScraper(),
    TravisScraper(),
]

ALL_SCRAPERS = GEORGIA_SCRAPERS + FLORIDA_SCRAPERS + TEXAS_SCRAPERS


def run():
    total_inserted = 0
    errors = []

    logger.info("=== SurplusRecoveryPro Scraper Starting ===")
    logger.info(f"Running {len(ALL_SCRAPERS)} scrapers across Georgia, Florida, and Texas")

    for scraper in ALL_SCRAPERS:
        state = getattr(scraper, 'state', 'Georgia')
        logger.info(f"Scraping {scraper.county_name} County, {state}...")
        try:
            records = scraper.scrape()
            if records:
                count = upsert_records(records)
                total_inserted += count
                logger.info(f"  ✓ {scraper.county_name}: {count} records loaded")
                check_and_create_alerts(records)
            else:
                logger.warning(f"  ⚠ {scraper.county_name}: No records found")
        except Exception as e:
            msg = f"{scraper.county_name} ({state}): {str(e)}"
            logger.error(f"  ✗ {msg}")
            errors.append(msg)

    logger.info(f"=== Done: {total_inserted} total records inserted ===")

    if errors:
        logger.warning(f"Errors in {len(errors)} counties:")
        for e in errors:
            logger.warning(f"  - {e}")

    total_in_db = get_record_count()
    logger.info(f"Total records now in database: {total_in_db}")

    if len(errors) == len(ALL_SCRAPERS):
        sys.exit(1)


if __name__ == "__main__":
    run()
