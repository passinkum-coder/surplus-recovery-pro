from scrapers.base_scraper import BaseScraper


class HarrisScraper(BaseScraper):
    def __init__(self):
        super().__init__(county_name="Harris", state="TX")


class DallasScraper(BaseScraper):
    def __init__(self):
        super().__init__(county_name="Dallas", state="TX")


class TarrantScraper(BaseScraper):
    def __init__(self):
        super().__init__(county_name="Tarrant", state="TX")


class BexarScraper(BaseScraper):
    def __init__(self):
        super().__init__(county_name="Bexar", state="TX")


class TravisScraper(BaseScraper):
    def __init__(self):
        super().__init__(county_name="Travis", state="TX")
