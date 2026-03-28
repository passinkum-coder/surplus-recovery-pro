from scrapers.base_scraper import BaseScraper

class MiamiDadeScraper(BaseScraper):
    def __init__(self):
        super().__init__(county_name="Miami-Dade")
