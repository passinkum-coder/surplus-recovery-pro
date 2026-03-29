from scrapers.base_scraper import BaseScraper
from scrapers.miami_dade_scraper import MiamiDadeScraper
from scrapers.broward_scraper import BrowardScraper
from scrapers.palm_beach_scraper import PalmBeachScraper


# =========================
# GEORGIA / OTHER SCRAPERS
# =========================

class CherokeeScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            county_name="Cherokee",
            state="GA",
            url="https://www.cherokeega.com/Tax-Commissioner/Excess-Funds/"
        )

    def scrape(self):
        html = self.get_page()

        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html, "html.parser")

        results = []

        elements = soup.find_all(["li", "p", "div", "tr"])

        for el in elements:
            text = self.normalize(el.get_text())

            if not text or len(text) < 12:
                continue

            keywords = [
                "tax", "sale", "excess", "fund", "property",
                "owner", "parcel", "amount", "$"
            ]

            if any(k in text.lower() for k in keywords):
                results.append({
                    "county": self.county_name,
                    "state": self.state,
                    "data": text
                })

        return results


class OrangeCountyScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            county_name="Orange",
            state="FL",
            url="https://example.com"
        )

    def scrape(self):
        html = self.get_page()
        return []


class HillsboroughScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            county_name="Hillsborough",
            state="FL",
            url="https://example.com"
        )

    def scrape(self):
        html = self.get_page()
        return []


# =========================
# LOADER FUNCTION
# =========================

def load_scrapers():
    return [
        CherokeeScraper(),
        MiamiDadeScraper(),
        BrowardScraper(),
        PalmBeachScraper(),
        HillsboroughScraper(),
        OrangeCountyScraper(),
    ]
