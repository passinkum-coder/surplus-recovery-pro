from scrapers.base_scraper import BaseScraper
import requests
from bs4 import BeautifulSoup


class MiamiDadeScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            county_name="Miami-Dade",
            state="FL",
            url="https://www.miamidade.gov/Apps/PA/PAClaims/Home/UnclaimedProperty"
        )

    def scrape(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"
        }

        try:
            response = requests.get(self.url, headers=headers, timeout=30)
            html = response.text
        except Exception:
            return []

        soup = BeautifulSoup(html, "html.parser")

        results = []

        # ----------------------------
        # STEP 1: TABLE EXTRACTION
        # ----------------------------
        rows = soup.find_all("tr")

        for row in rows:
            cols = row.find_all("td")

            if len(cols) < 2:
                continue

            results.append({
                "county": self.county_name,
                "state": self.state,
                "record_id": cols[0].get_text(strip=True),
                "owner": cols[1].get_text(strip=True) if len(cols) > 1 else None,
                "amount": cols[2].get_text(strip=True) if len(cols) > 2 else None,
                "url": self.url
            })

        # ----------------------------
        # STEP 2: GENERIC DIV FALLBACK
        # ----------------------------
        if not results:
            blocks = soup.find_all("div")

            for b in blocks:
                text = b.get_text(" ", strip=True)

                if len(text) < 20:
                    continue

                # only keep meaningful chunks
                if any(keyword in text.lower() for keyword in ["property", "claim", "owner", "amount", "unclaimed"]):
                    results.append({
                        "county": self.county_name,
                        "state": self.state,
                        "record_id": text[:80],
                        "owner": None,
                        "amount": None,
                        "url": self.url
                    })

        return results
