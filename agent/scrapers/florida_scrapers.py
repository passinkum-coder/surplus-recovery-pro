from scrapers.miami_dade_scraper import MiamiDadeScraper
from scrapers.broward_scraper import BrowardScraper
from scrapers.palm_beach_scraper import PalmBeachScraper


# =========================
# FLORIDA COUNTY SCRAPERS
# =========================

class HillsboroughScraper:
    def __init__(self):
        self.county_name = "Hillsborough"
        self.state = "FL"

    def scrape(self):
        # TODO: add real logic if needed
        return []


class OrangeCountyScraper:
    def __init__(self):
        self.county_name = "Orange"
        self.state = "FL"

    def scrape(self):
        # TODO: add real logic if needed
        return []


# =========================
# LOADER
# =========================

def load_scrapers():
    return [
        MiamiDadeScraper(),
        BrowardScraper(),
        PalmBeachScraper(),
        HillsboroughScraper(),
        OrangeCountyScraper(),
    ]
