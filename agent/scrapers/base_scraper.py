class BaseScraper:
    def __init__(self, county_name, state=None):
        self.county_name = county_name
        self.state = state

    def scrape(self):
        """
        Override this method in each county scraper.
        This is the main entry point for scraping logic.
        """
        raise NotImplementedError("Each scraper must implement scrape()")

    def format_result(self, data):
        """
        Standard formatting for scraped results.
        You can expand this later when you add database/storage.
        """
        return {
            "county": self.county_name,
            "state": self.state,
            "data": data
        }
