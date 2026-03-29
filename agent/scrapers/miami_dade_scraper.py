from scrapers.base_scraper import BaseScraper


class MiamiDadeScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            county_name="Miami-Dade",
            state="FL",
            url="https://www.miamidade.gov/Apps/PA/PAClaims/Home/UnclaimedProperty"
        )

    def scrape(self):
        from playwright.sync_api import sync_playwright

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            page.goto(self.url, wait_until="networkidle")

            # wait for ANY visible content container
            page.wait_for_timeout(5000)

            content = page.content()
            browser.close()

        # fallback extraction (simple text capture)
        return [{
            "county": self.county_name,
            "state": self.state,
            "raw_text": content[:2000]
        }]
