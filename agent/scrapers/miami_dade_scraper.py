from scrapers.base_scraper import BaseScraper
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup


class MiamiDadeScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            county_name="Miami-Dade",
            state="FL",
            url="https://www.miamidade.gov/Apps/PA/PAClaims/Home/UnclaimedProperty"
        )


    def scrape(self):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            page.goto(self.url, wait_until="networkidle")
            page.wait_for_timeout(5000)

            html = page.content()
            browser.close()

        soup = BeautifulSoup(html, "html.parser")

        records = []

        # STEP 1: TRY TABLE PARSING
        rows = soup.find_all("tr")

        for r in rows:
            cols = r.find_all("td")

            if len(cols) < 2:
                continue

            records.append({
                "county": self.county_name,
                "state": self.state,
                "record_id": cols[0].get_text(strip=True) if cols[0] else None,
                "owner": cols[1].get_text(strip=True) if len(cols) > 1 else None,
                "amount": cols[2].get_text(strip=True) if len(cols) > 2 else None,
                "url": self.url
            })

        # STEP 2: FALLBACK DIV PARSING (IF TABLE EMPTY)
        if not records:
            blocks = soup.find_all("div")

            for b in blocks:
                text = b.get_text(strip=True)

                if not text or len(text) < 15:
                    continue

                records.append({
                    "county": self.county_name,
                    "state": self.state,
                    "record_id": text[:60],
                    "owner": None,
                    "amount": None,
                    "url": self.url
                })

        return records
