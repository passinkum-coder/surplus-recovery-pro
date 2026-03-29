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
        requests_log = []

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            # 🔥 Capture ALL network requests
            def log_request(request):
                try:
                    requests_log.append({
                        "method": request.method,
                        "url": request.url
                    })
                except:
                    pass

            page.on("request", log_request)

            page.goto(self.url, wait_until="networkidle")
            page.wait_for_timeout(8000)

            browser.close()

        # 🔥 PRINT ALL REQUESTS (DEBUG OUTPUT)
        print("\n================ NETWORK REQUESTS ================\n")

        for r in requests_log:
            print(f"[{r['method']}] {r['url']}")

        print("\n================ END REQUEST LOG ================\n")

        # IMPORTANT: no parsing yet, only discovery mode
        return []
