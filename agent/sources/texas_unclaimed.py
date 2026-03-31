from playwright.sync_api import sync_playwright


class TexasUnclaimed:
    def __init__(self):
        self.url = "https://claimittexas.gov/app/claim-search"

    def run(self, max_records=50):
        results = []

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            print("Fetching Texas page...")

            page.goto(self.url, wait_until="networkidle")
            page.wait_for_timeout(5000)

            # Try to trigger any lazy-loaded data
            try:
                page.keyboard.type("a")
                page.wait_for_timeout(3000)
            except:
                pass

            page.wait_for_timeout(5000)

            # ⚠️ DOM extraction fallback (safe baseline)
            rows = page.query_selector_all("table tr")

            for row in rows[:max_records]:
                cols = row.query_selector_all("td")
                if len(cols) >= 2:
                    results.append({
                        "name": cols[0].inner_text().strip(),
                        "value": cols[1].inner_text().strip(),
                        "state": "Texas"
                    })

            browser.close()

        print(f"Texas total records: {len(results)}")
        return results
