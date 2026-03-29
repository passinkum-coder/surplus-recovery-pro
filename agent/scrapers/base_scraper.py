import requests

class BaseScraper:
    def __init__(self, county_name=None, state=None, url=None):
        self.county_name = county_name
        self.state = state
        self.url = url

    def scrape(self):
        raise NotImplementedError

    def get_page(self, url, timeout=15):
        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
        return response.text
