from scrapers.base_scraper import BaseScraper
from playwright.sync_api import sync_playwright


class MiamiDadeScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            county_name="Miami-Dade",
            state="FL",
            url="https://www.miamidade.gov/Apps/PA/PAClaims/Home/UnclaimedProperty"
        )

    def scrape(self):
        results = []

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            page.goto(self.url, wait_until="networkidle")
            page.wait_for_timeout(3000)

            # 🔥 Fill ANY text input with a value
            try:
                inputs = page.query_selector_all("input")

                for inp in inputs:
                    try:
                        inp.fill("a")
                        break
                    except:
                        continue
            except:
                pass

            page.wait_for_timeout(2000)

            # 🔥 Submit the form (REAL KEY STEP)
            try:
                page.keyboard.press("Enter")
                page.wait_for_timeout(6000)
            except:
                pass

            # 🔥 Now scrape FULL HTML after submission
            content = page.content()

            browser.close()

        # 🔥 BASIC EXTRACTION FROM RESULT PAGE
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(content, "html.parser")

        rows = soup.find_all("tr")

        for row in rows:
            cols = row.find_all("td")

            if len(cols) < 2:
                continue

            results.append({
                "county": self.county_name,
                "state": self.state,
                "record_id": cols[0].get_text(strip=True),
                "owner": cols[1].get_text(strip=True),
                "amount": cols[2].get_text(strip=True) if len(cols) > 2 else None,
                "url": self.url
            })

        return results
