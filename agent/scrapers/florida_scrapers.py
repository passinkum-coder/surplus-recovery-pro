from scrapers.base_scraper import BaseScraper


class MiamiDadeScraper(BaseScraper):
    def __init__(self):
        super().__init__(county_name="Miami-Dade")


class BrowardScraper(BaseScraper):
    def __init__(self):
        super().__init__(county_name="Broward")


class PalmBeachScraper(BaseScraper):
    def __init__(self):
        super().__init__(county_name="Palm Beach")


class HillsboroughScraper(BaseScraper):
    def __init__(self):
        super().__init__(county_name="Hillsborough")


class OrangeScraper(BaseScraper):
    def __init__(self):
        super().__init__(county_name="Orange")
