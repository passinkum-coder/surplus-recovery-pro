from scrapers.base_scraper import BaseScraper

class BrowardScraper(BaseScraper):
    def __init__(self):
        super().__init__(county_name="Broward", state="FL")
