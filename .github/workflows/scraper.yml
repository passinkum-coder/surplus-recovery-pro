import time
from playwright.sync_api import sync_playwright


class BaseScraper:
    def __init__(self, county_name=None, state=None):
        self.county_name = county_name
        self.state = state

    def get_page(self, url):
        """
        Fetch page HTML using a real browser (bypasses 403 blocks)
        """
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=True,
                args=["--no-sandbox", "--disable-setuid-sandbox"]
            )

            page = browser.new_page()

            # Go to page and wait for full load
            page.goto(url, wait_until="networkidle", timeout=60000)

            html = page.content()

            browser.close()
            return html

    def scrape(self):
        """
        Override this in each county scraper
        """
        raise NotImplementedError("scrape() must be implemented in child class")
