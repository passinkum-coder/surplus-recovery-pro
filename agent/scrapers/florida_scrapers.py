from scrapers.miami_dade_scraper import MiamiDadeScraper
from scrapers.broward_scraper import BrowardScraper
from scrapers.palm_beach_scraper import PalmBeachScraper

# If these are defined INSIDE this file, do NOT import them
# just include them below


def load_scrapers():
    return [
        MiamiDadeScraper(),
        BrowardScraper(),
        PalmBeachScraper(),
        HillsboroughScraper(),
        OrangeCountyScraper(),
    ]
