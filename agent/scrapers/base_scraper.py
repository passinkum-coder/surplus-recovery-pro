class BaseScraper:
    def __init__(self, county_name=None, state=None, url=None):
        self.county_name = county_name
        self.state = state
        self.url = url

    def get_page(self, url=None):
        from playwright.sync_api import sync_playwright

        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=True,
                args=["--no-sandbox", "--disable-setuid-sandbox"]
            )

            page = browser.new_page()

            target_url = url or self.url
            if not target_url:
                raise ValueError("No URL provided")

            page.goto(target_url, wait_until="networkidle", timeout=60000)

            html = page.content()
            browser.close()

            return html

    def scrape(self):
        raise NotImplementedError("scrape() must be implemented in child class")
