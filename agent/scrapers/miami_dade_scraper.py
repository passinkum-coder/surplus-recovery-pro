from bs4 import BeautifulSoup
from scrapers.base_scraper import BaseScraper


class MiamiDadeScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            county_name="Miami-Dade",
            state="FL",
            url="https://www.miamidade.gov/Apps/PA/PAClaims/Home/UnclaimedProperty"
        )

    def scrape(self):
        html = self.get_page()

        soup = BeautifulSoup(html, "html.parser")

        results = []

        # Try multiple possible table patterns (robust scraping)
        rows = soup.select("table tr")

        for row in rows:
            cols = row.find_all("td")

            if len(cols) < 2:
                continue

            text = self.normalize(cols[0].get_text())

            if not text:
                continue

            results.append({
                "county": self.county_name,
                "state": self.state,
                "source": self.url,
                "raw_text": text
            })

        return results
