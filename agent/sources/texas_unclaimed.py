from playwright.sync_api import sync_playwright


class TexasUnclaimed:
    def __init__(self):
        self.url = "https://www.claimittexas.gov/app/claim-search"
        self.captured_requests = []
        self.captured_responses = []

    def run(self, max_records=50):
        print("\n🚀 STARTING TEXAS NETWORK CAPTURE PIPELINE")
        print("=" * 60)

        results = []

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            # ==============================
            # REQUEST CAPTURE
            # ==============================
            def handle_request(request):
                try:
                    url = request.url
                    method = request.method

                    post_data = None
                    try:
                        post_data = request.post_data
                    except:
                        pass

                    if any(x in url.lower() for x in ["sws", "search", "claim", "query", "api"]):
                        print("\n🔥 REQUEST CAPTURED")
                        print("METHOD:", method)
                        print("URL:", url)
                        if post_data:
                            print("POST DATA:", post_data)

                        self.captured_requests.append({
                            "url": url,
                            "method": method,
                            "post_data": post_data
                        })

                except:
                    pass

            # ==============================
            # RESPONSE CAPTURE
            # ==============================
            def handle_response(response):
                try:
                    url = response.url

                    if any(x in url.lower() for x in ["sws", "search", "claim", "query", "api"]):
                        try:
                            content_type = response.headers.get("content-type", "")

                            if "application/json" in content_type:
                                data = response.json()

                                print("\n📡 RESPONSE CAPTURED")
                                print("URL:", url)

                                self.captured_responses.append({
                                    "url": url,
                                    "data": data
                                })

                        except:
                            pass

                except:
                    pass

            page.on("request", handle_request)
            page.on("response", handle_response)

            # ==============================
            # LOAD PAGE
            # ==============================
            print("📡 Loading Texas ClaimIt page...")
            page.goto(self.url, wait_until="networkidle")

            page.wait_for_timeout(3000)

            # ==============================
            # SEARCH FLOW (FIXED)
            # ==============================
            print("🔍 Locating input field...")

            inputs = page.query_selector_all("input")
            if not inputs:
                print("❌ No input fields found")
                browser.close()
                return []

            search = inputs[0]

            print("✍️ Typing search query: JOHN")
            search.fill("john")

            page.wait_for_timeout(1500)

            print("🖱 Attempting to trigger search via button click...")

            buttons = page.query_selector_all("button")
            clicked = False

            for b in buttons:
                try:
                    txt = (b.inner_text() or "").lower()
                    if "search" in txt or "find" in txt or "submit" in txt:
                        b.click()
                        clicked = True
                        print("✅ Search button clicked")
                        break
                except:
                    pass

            if not clicked:
                print("⚠️ No search button found — fallback click center")
                page.mouse.click(400, 300)

            print("⏳ Waiting for API responses...")
            page.wait_for_timeout(12000)

            browser.close()

        # ==============================
        # PROCESS RESULTS
        # ==============================
        print("\n========================")
        print("PROCESSING CAPTURED DATA")
        print("========================")

        for r in self.captured_responses:
            data = r.get("data")

            if isinstance(data, list):
                results.extend(data)

            elif isinstance(data, dict):
                for key in ["data", "results", "items", "records"]:
                    if key in data and isinstance(data[key], list):
                        results.extend(data[key])

        print("\n========================")
        print("FINAL RESULTS")
        print("========================")
        print("REQUESTS CAPTURED:", len(self.captured_requests))
        print("RESPONSES CAPTURED:", len(self.captured_responses))
        print("TOTAL RECORDS:", len(results))

        return results[:max_records]
