from playwright.sync_api import sync_playwright
import time


class TexasUnclaimed:
    def __init__(self):
        self.url = "https://www.claimittexas.gov/app/claim-search"

    def run(self, max_records=50):
        results = []

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            # capture API calls
            def log_response(response):
                if any(x in response.url.lower() for x in ["api", "search", "claim", "graphql"]):
                    print("HIT API:", response.url)

            page.on("response", log_response)

            page.goto(self.url, wait_until="networkidle")

            # wait for JS app to load fully
            page.wait_for_timeout(5000)

            # TRY TO FIND SEARCH INPUT
            inputs = page.query_selector_all("input")

            print(f"FOUND INPUTS: {len(inputs)}")

            if len(inputs) == 0:
                print("NO SEARCH INPUT FOUND")
                browser.close()
                return []

            search_box = inputs[0]

            # simulate real user search
            search_box.fill("John")
            search_box.press("Enter")

            print("SEARCH TRIGGERED")

            # wait for results request
            page.wait_for_timeout(8000)

            browser.close()

        print("DONE REAL SEARCH RUN")
        return results
