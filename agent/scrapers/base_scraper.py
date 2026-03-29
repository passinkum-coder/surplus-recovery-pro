from playwright.sync_api import sync_playwright


class BaseScraper:
    def __init__(self, county_name=None, state=None, url=None):
        self.county_name = county_name
        self.state = state
        self.url = url

    def get_page(self, url):
        """
        Fetch page HTML using Playwright (bypasses most 403 blocks)
        """
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=True,
                args=["--no-sandbox", "--disable-setuid-sandbox"]
            )

            page = browser.new_page()

            page.goto(url, wait_until="networkidle", timeout=60000)

            html = page.content()

            browser.close()
            return html

    def scrape(self):
        raise NotImplementedError("Each scraper must implement scrape()")
