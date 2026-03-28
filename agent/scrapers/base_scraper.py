class BaseScraper:
    def __init__(self, county_name, state=None, url=None):
        self.county_name = county_name
        self.state = state
        self.url = url
