from playwright.sync_api import sync_playwright


class TexasUnclaimed:
    def __init__(self):
        self.url = "https://claimittexas.gov/app/claim-search"

    def run(self, max_requests=5):
        captured = []

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            # 🔥 CAPTURE ALL API CALLS
            def log_response(response):
                try:
                    if "api" in response.url or "search" in response.url:
                        print("API:", response.url)
                        print("STATUS:", response.status)
                except:
                    pass

            page.on("response", log_response)

            page.goto(self.url, wait_until="networkidle")
            page.wait_for_timeout(5000)

            # 🔥 FORCE ANY USER ACTION
            try:
                page.keyboard.type("a")
                page.wait_for_timeout(3000)
            except:
                pass

            # 🔥 LET PAGE FIRE XHR CALLS
            page.wait_for_timeout(8000)

            browser.close()

        print("DEBUG COMPLETE — check API logs above")
        return captured
