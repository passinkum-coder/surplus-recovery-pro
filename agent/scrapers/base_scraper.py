class BaseScraper:
    def __init__(self, county_name=None, url=None):
        self.county_name = county_name
        self.url = url

    def scrape(self):
        """
        Must be overridden by child scrapers.
        Should return a list of dict records.
        """
        raise NotImplementedError("scrape() must be implemented by subclass")
