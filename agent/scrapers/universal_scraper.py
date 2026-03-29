from bs4 import BeautifulSoup
from scrapers.base_scraper import BaseScraper


class UniversalScraper(BaseScraper):
    def __init__(self, county_name, state, url):
        super().__init__(county_name=county_name, state=state, url=url)

    def scrape(self):
        html = self.get_page()

        soup = BeautifulSoup(html, "html.parser")

        results = []

        # -----------------------------
        # 1. TABLE EXTRACTION
        # -----------------------------
        rows = soup.find_all("tr")
        for row in rows:
            cols = row.find_all("td")
            text = self.normalize(row.get_text())

            if len(cols) >= 2 and text:
                results.append(self._build_record(text))

        # -----------------------------
        # 2. LIST EXTRACTION
        # -----------------------------
        items = soup.find_all("li")
        for item in items:
            text = self.normalize(item.get_text())

            if text:
                results.append(self._build_record(text))

        # -----------------------------
        # 3. DIV / PARAGRAPH MINING
        # -----------------------------
        blocks = soup.find_all(["div", "p"])
        for b in blocks:
            text = self.normalize(b.get_text())

            if self._looks_relevant(text):
                results.append(self._build_record(text))

        return results

    # -----------------------------
    # HELPERS
    # -----------------------------

    def _looks_relevant(self, text):
        if not text or len(text) < 12:
            return False

        keywords = [
            "tax", "sale", "excess", "fund",
            "property", "owner", "parcel",
            "amount", "$", "unclaimed"
        ]

        t = text.lower()
        return any(k in t for k in keywords)

    def _build_record(self, text):
        return {
            "county": self.county_name,
            "state": self.state,
            "source": self.url,
            "raw": text
        }
