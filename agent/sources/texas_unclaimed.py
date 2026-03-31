from playwright.sync_api import sync_playwright


class TexasUnclaimed:
    def __init__(self):
        self.url = "https://www.claimittexas.gov/app/claim-search"
        self.captured_payloads = []

    def run(self, max_records=50):
        print("\n🚀 STARTING TEXAS NETWORK CAPTURE PIPELINE")
        print("=" * 60)

        results = []

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            # -----------------------------
            # NETWORK CAPTURE (FIXED + PROPERLY INDENTED)
            # -----------------------------
            def handle_response(response):
                try:
                    request = response.request
                    url = response.url
                    method = request.method

                    # skip junk assets only
                    if any(x in url for x in [".png", ".jpg", ".css", ".svg"]):
                        return

                    content_type = response.headers.get("content-type", "")

                    if "application/json" in content_type:
                        try:
                            data = response.json()

                            print("\n📡 CAPTURED RESPONSE")
                            print("METHOD:", method)
                            print("URL:", url)

                            self.captured_payloads.append({
                                "url": url,
                                "method": method,
                                "data": data
                            })

                        except:
                            pass

                except Exception as e:
                    pass

            page.on("response", handle_response)

            # -----------------------------
            # LOAD PAGE
            # -----------------------------
            print("📡 Loading Texas page...")
            page.goto(self.url, wait_until="networkidle")

            page.wait_for_timeout(3000)

            # -----------------------------
            # SEARCH INPUT
            # -----------------------------
            inputs = page.query_selector_all("input")

            if not inputs:
                print("❌ No input found")
                browser.close()
                return []

            search = inputs[0]

            print("✍️ Searching JOHN")
            search.fill("john")

            search.press("Enter")

            print("⏳ Waiting for network responses...")
            page.wait_for_timeout(8000)

            browser.close()

        # -----------------------------
        # PROCESS RESULTS
        # -----------------------------
        print("\n========================")
        print("PROCESSING CAPTURED DATA")
        print("========================")

        for payload in self.captured_payloads:
            if isinstance(payload.get("data"), dict):
                results.append(payload)

        print("\n========================")
        print("FINAL RESULTS")
        print("========================")
        print("TOTAL RECORDS:", len(results))

        return results[:max_records]
