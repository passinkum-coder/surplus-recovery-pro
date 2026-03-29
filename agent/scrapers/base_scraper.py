import requests

class BaseScraper:
    def __init__(self, county_name=None, state=None, url=None):
        self.county_name = county_name
        self.state = state
        self.url = url

    def scrape(self):
        raise NotImplementedError

    def get_page(self, url=None, **kwargs):
        """
        SAFE:
        - works with self.get_page()
        - works with self.get_page(self.url)
        - works with explicit URL
        """

        target_url = url or self.url

        if not target_url:
            raise ValueError(
                f"{self.__class__.__name__} has no URL (pass url or set self.url)"
            )

        headers = {"User-Agent": "Mozilla/5.0"}

        response = requests.get(target_url, headers=headers, timeout=15)
        response.raise_for_status()
        return response.text
