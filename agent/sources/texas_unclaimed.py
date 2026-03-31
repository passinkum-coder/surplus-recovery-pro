from playwright.sync_api import sync_playwright
import json
import re


class TexasUnclaimed:
    def __init__(self):
        self.url = "https://www.claimittexas.gov/app/claim-search"

        # we store API responses here
        self.captured_payloads = []

    def run(self, max_records=50):
        print("\n🚀 STARTING TEXAS NETWORK CAPTURE PIPELINE")
        print("=" * 60)

        results = []

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            # -----------------------------
            # NETWORK INTERCEPTOR (CRITICAL)
            # -----------------------------
            def handle_response(response):
                try:
                    url = response.url

                    # Capture only likely API/XHR calls
                    if any(x in url.lower() for x in ["api", "search", "claim", "unclaimed", "results"]):
                        try:
                            content_type = response.headers.get("content-type", "")

                            if "application/json" in content_type:
                                data = response.json()

                                print(f"\n📡 CAPTURED API RESPONSE:")
                                print(f"URL: {url}")

                                self.captured_payloads.append(data)

                        except:
                            pass

                except:
                    pass

            page.on("response", handle_response)

            # -----------------------------
            # LOAD PAGE
            # -----------------------------
            print("📡 Loading Texas ClaimIt page...")
            page.goto(self.url, wait_until="networkidle")

            page.wait_for_timeout(3000)

            # -----------------------------
            # FIND INPUT
            # -----------------------------
            print("🔍 Locating search input...")

            inputs = page.query_selector_all("input")

            if not inputs:
                print("❌ No input fields found")
                browser.close()
                return []

            search = inputs[0]

            # -----------------------------
            # SEARCH TRIGGER
            # -----------------------------
            print("✍️ Entering search: JOHN")
            search.fill("john")

            page.wait_for_timeout(1000)

            print("🔍 Submitting search...")
            search.press("Enter")

            # -----------------------------
            # WAIT FOR NETWORK CALLS
            # -----------------------------
            print("⏳ Waiting for API responses...")
            page.wait_for_timeout(8000)

            browser.close()

        # -----------------------------
        # PARSE CAPTURED PAYLOADS
        # -----------------------------
        print("\n========================")
        print("PROCESSING CAPTURED DATA")
        print("========================")

        for payload in self.captured_payloads:
            extracted = self.extract_records(payload)
            results.extend(extracted)

        # -----------------------------
        # FINAL OUTPUT
        # -----------------------------
        print("\n========================")
        print("FINAL RESULTS")
        print("========================")
        print("TOTAL RECORDS:", len(results))

        return results[:max_records]

    # -----------------------------
    # EXTRACT RECORDS FROM JSON
    # -----------------------------
    def extract_records(self, payload):
        records = []

        try:
            # CASE 1: list response
            if isinstance(payload, list):
                for item in payload:
                    rec = self.normalize(item)
                    if rec:
                        records.append(rec)

            # CASE 2: dict response
            elif isinstance(payload, dict):

                # common API patterns
                possible_keys = ["data", "results", "items", "records", "content"]

                found = False

                for key in possible_keys:
                    if key in payload and isinstance(payload[key], list):
                        for item in payload[key]:
                            rec = self.normalize(item)
                            if rec:
                                records.append(rec)
                        found = True
                        break

                if not found:
                    rec = self.normalize(payload)
                    if rec:
                        records.append(rec)

        except:
            pass

        return records

    # -----------------------------
    # NORMALIZE RECORD STRUCTURE
    # -----------------------------
    def normalize(self, item):
        try:
            if not isinstance(item, dict):
                return None

            return {
                "owner_name": item.get("ownerName") or item.get("name") or item.get("owner"),
                "address": item.get("address"),
                "city": item.get("city"),
                "state": "TX",
                "county": item.get("county"),
                "amount": item.get("amount") or item.get("value"),
                "raw": item
            }

        except:
            return None
