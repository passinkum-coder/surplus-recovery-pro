import requests
from bs4 import BeautifulSoup


class UniversalScraper:
    def __init__(self, county_name=None, source_url=None, *args, **kwargs):
        self.county_name = county_name
        self.source_url = source_url


    # MAIN ENTRY POINT
    def run(self):
        html = self.get_page()
        records = self.parse(html)
        return self.normalize(records)


    def scrape(self):
        return self.run()


    def fetch(self):
        return self.run()


    def get_data(self):
        return self.run()


    # FETCH PAGE
    def get_page(self):
        if not self.source_url:
            return ""

        try:
            headers = {
                "User-Agent": "Mozilla/5.0"
            }

            response = requests.get(self.source_url, headers=headers, timeout=20)
            response.raise_for_status()
            return response.text

        except Exception as e:
            print(f"[WARN] Failed to fetch {self.county_name}: {e}")
            return ""


    # 🟢 STEP 3: BASIC WORKING PARSER (REPLACES EMPTY OUTPUT)
    def parse(self, html):
        if not html:
            return []

        soup = BeautifulSoup(html, "html.parser")

        records = []

        # Generic extraction fallback (works across most basic listing pages)
        items = soup.find_all("tr") or soup.find_all("li") or soup.find_all("div")

        for i in items:
            text = i.get_text(strip=True)

            # filter junk noise
            if not text or len(text) < 10:
                continue

            records.append({
                "record_id": text[:60],
                "amount": None,
                "owner": None,
                "url": self.source_url
            })

        return records


    # OUTPUT CONTRACT NORMALIZER
    def normalize(self, records):
        if not records:
            return []

        normalized = []

        for r in records:
            normalized.append({
                "county": self.county_name,
                "source": self.source_url,
                "record_id": r.get("record_id"),
                "amount": r.get("amount"),
                "owner": r.get("owner"),
                "url": r.get("url")
            })

        return normalized
