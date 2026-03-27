class BaseScraper:
    def __init__(self, county_name=None):
        self.county_name = county_name

    def scrape(self):
        raise NotImplementedError("Scrape method must be implemented by child class")
