import json
from playwright.sync_api import sync_playwright


class TexasUnclaimed:
    def __init__(self):
        self.url = "https://www.claimittexas.gov/app/claim-search"

    def run(self, max_records=50):
        print("\n🚀 STARTING RUNTIME STATE EXTRACTION (PLAYWRIGHT)")
        print("=" * 60)

        results = []

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            # -----------------------------
            # CAPTURE XHR / FETCH RESPONSES
            # -----------------------------
            def handle_response(response):
                try:
                    url = response.url.lower()

                    if any(k in url for k in ["search", "claim", "api", "graphql", "sws"]):
                        print("📡 API RESPONSE:", response.status, response.url)

                        try:
                            data = response.json()

                            extracted = self.extract(data)
                            if extracted:
                                results.extend(extracted)

                        except:
                            pass

                except:
                    pass

            page.on("response", handle_response)

            # -----------------------------
            # LOAD PAGE
            # -----------------------------
            page.goto(self.url, wait_until="networkidle")
            page.wait_for_timeout(4000)

            # -----------------------------
            # FIND INPUT FIELD
            # -----------------------------
            inputs = page.query_selector_all("input")

            if not inputs:
                print("❌ NO INPUT FIELDS FOUND")
                browser.close()
                return []

            search = inputs[0]

            print("✍️ ENTERING SEARCH TERM: JOHN")
            search.fill("john")

            page.wait_for_timeout(1000)

            print("🔍 TRIGGERING SEARCH")
            search.press("Enter")

            # allow network + rendering
            page.wait_for_timeout(8000)

            browser.close()

        # -----------------------------
        # FINAL OUTPUT
        # -----------------------------
        print("\n========================")
        print("FINAL RESULTS")
        print("========================")
        print("TOTAL RECORDS:", len(results))

        return results[:max_records]

    # -----------------------------
    # EXTRACT STRUCTURED RECORDS
    # -----------------------------
    def extract(self, data):
        records = []

        try:
            # Case 1: list of results
            if isinstance(data, list):
                for item in data:
                    parsed = self.normalize(item)
                    if parsed:
                        records.append(parsed)

            # Case 2: dict with embedded results
            elif isinstance(data, dict):
                for key in ["results", "data", "items", "claims"]:
                    if key in data and isinstance(data[key], list):
                        for item in data[key]:
                            parsed = self.normalize(item)
                            if parsed:
                                records.append(parsed)

        except:
            pass

        return records

    # -----------------------------
    # NORMALIZE RECORD
    # -----------------------------
    def normalize(self, item):
        try:
            if not isinstance(item, dict):
                return None

            return {
                "owner_name": item.get("name") or item.get("owner"),
                "address": item.get("address"),
                "amount": item.get("amount"),
                "county": item.get("county"),
                "state": "TX"
            }

        except:
            return None
