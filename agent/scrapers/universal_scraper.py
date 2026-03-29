from bs4 import BeautifulSoup
import re
from scrapers.base_scraper import BaseScraper


class UniversalScraper(BaseScraper):
    """
    v2 Universal Scraper:
    - structured extraction (name, amount, parcel, owner)
    - works across GA / FL / TX counties
    - safe fallback parsing for messy government HTML
    """

    def __init__(self, county_name, state, url):
        super().__init__(county_name=county_name, state=state, url=url)

    # =========================
    # MAIN ENTRY
    # =========================
    def scrape(self):
        html = self.get_page()
        soup = BeautifulSoup(html, "html.parser")

        results = []

        # 1. TABLE ROWS (highest accuracy source)
        for row in soup.find_all("tr"):
            text = self.clean(row.get_text(" "))

            if not text:
                continue

            record = self.parse_record(text)
            if record:
                results.append(record)

        # 2. LIST ITEMS
        for li in soup.find_all("li"):
            text = self.clean(li.get_text(" "))

            record = self.parse_record(text)
            if record:
                results.append(record)

        # 3. DIV / PARAGRAPH FALLBACK
        for tag in soup.find_all(["div", "p"]):
            text = self.clean(tag.get_text(" "))

            if self.is_relevant(text):
                record = self.parse_record(text)
                if record:
                    results.append(record)

        return self.deduplicate(results)

    # =========================
    # PARSING ENGINE
    # =========================
    def parse_record(self, text):
        if len(text) < 10:
            return None

        amount = self.extract_amount(text)
        parcel = self.extract_parcel(text)
        name = self.extract_name(text)

        # must have at least something meaningful
        if not (amount or parcel or name):
            return None

        return {
            "county": self.county_name,
            "state": self.state,
            "name": name,
            "amount": amount,
            "parcel_id": parcel,
            "source": self.url,
            "raw": text
        }

    # =========================
    # EXTRACTION HELPERS
    # =========================

    def extract_amount(self, text):
        match = re.search(r"\$[\d,]+(?:\.\d{2})?", text)
        return match.group(0) if match else None

    def extract_parcel(self, text):
        patterns = [
            r"\b\d{3,}-\d{2,}-\d{2,}\b",
            r"\b[A-Z0-9]{6,}\b"
        ]

        for p in patterns:
            match = re.search(p, text)
            if match:
                return match.group(0)

        return None

    def extract_name(self, text):
        # crude but effective government-name capture
        text = re.sub(r"\$[\d,]+(?:\.\d{2})?", "", text)
        text = re.sub(r"\b\d{3,}-\d{2,}-\d{2,}\b", "", text)
        text = re.sub(r"\s+", " ", text).strip()

        if len(text) > 5:
            return text[:120]

        return None

    # =========================
    # FILTERING
    # =========================

    def is_relevant(self, text):
        if not text or len(text) < 12:
            return False

        keywords = [
            "tax", "sale", "excess", "fund",
            "unclaimed", "property", "owner",
            "parcel", "refund", "$"
        ]

        t = text.lower()
        return any(k in t for k in keywords)

    # =========================
    # UTILITIES
    # =========================

    def clean(self, text):
        return re.sub(r"\s+", " ", text).strip()

    def deduplicate(self, items):
        seen = set()
        unique = []

        for item in items:
            key = (item.get("name"), item.get("amount"), item.get("parcel_id"))

            if key not in seen:
                seen.add(key)
                unique.append(item)

        return unique
