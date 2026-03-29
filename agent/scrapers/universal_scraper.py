from scrapers.base_scraper import BaseScraper


class UniversalScraper(BaseScraper):
    def __init__(self, county_name: str, state: str, url: str):
        super().__init__(
            county_name=county_name,
            state=state,
            url=url
        )

    def scrape(self):
        """
        Universal scraper v2:
        - Works for ALL counties
        - Uses Playwright fallback extraction
        - No site-specific logic needed
        """

        from playwright.sync_api import sync_playwright

        html = ""

        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()

                page.goto(self.url, wait_until="networkidle")

                # allow JS rendering
                page.wait_for_timeout(5000)

                html = page.content()

                browser.close()

        except Exception as e:
            return [{
                "county": self.county_name,
                "state": self.state,
                "error": str(e),
                "raw_text": ""
            }]

        # fallback extraction (simple safe universal output)
        return [{
            "county": self.county_name,
            "state": self.state,
            "raw_text": html[:3000]
        }]
