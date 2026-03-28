from scrapers.base_scraper import BaseScraper

class PalmBeachScraper(BaseScraper):
    def __init__(self):
        super().__init__(county_name="Palm-Beach", state="FL")
