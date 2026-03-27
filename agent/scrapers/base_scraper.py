class BaseScraper:
    def __init__(self, county_name=None, url=None):
        self.county_name = county_name
        self.url = url

    def scrape(self):
        raise NotImplementedError("Each scraper must implement scrape()")
