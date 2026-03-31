from playwright.sync_api import sync_playwright
import json


class TexasUnclaimed:
    def __init__(self):
        self.url = "https://claimittexas.gov/app/claim-search"

    def run(self, max_records=50):
        results = []

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            print("Loading Texas site...")

            captured_payloads = []

            # INTERCEPT NETWORK RESPONSES
            def handle_response(response):
                try:
                    if "application/json" in response.headers.get("content-type", ""):
                        data = response.json()
                        captured_payloads.append(data)
                except:
                    pass

            page.on("response", handle_response)

            page.goto(self.url, wait_until="networkidle")
            page.wait_for_timeout(8000)

            browser.close()

        # EXTRACT ANY STRUCTURED DATA FOUND
        for payload in captured_payloads:
            if isinstance(payload, list):
                for item in payload:
                    if len(results) >= max_records:
                        break

                    results.append({
                        "raw": item,
                        "state": "Texas"
                    })

            elif isinstance(payload, dict):
                for k, v in payload.items():
                    if isinstance(v, list):
                        for item in v:
                            if len(results) >= max_records:
                                break

                            results.append({
                                "raw": item,
                                "state": "Texas"
                            })

        print(f"Texas total records: {len(results)}")
        return results
