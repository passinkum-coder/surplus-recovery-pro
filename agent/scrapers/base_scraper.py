class BaseScraper:
    def __init__(self):
        pass

    def scrape(self):
        raise NotImplementedError("Scrape method must be implemented by child class")
