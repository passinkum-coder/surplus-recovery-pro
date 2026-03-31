from playwright.sync_api import sync_playwright
import json
import time


class TexasUnclaimed:
    def __init__(self):
        self.url = "https://www.claimittexas.gov/app/claim-search"
        self.captured_requests = []

    def run(self, max_records=50):
        print("🚀 STARTING NETWORK CAPTURE PIPELINE")

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            # -----------------------------
            # CAPTURE ALL NETWORK REQUESTS
            # -----------------------------
            def handle_request(request):
                if any(x in request.url.lower() for x in ["search", "claim", "sws", "api", "graphql"]):
                    self.captured_requests.append({
                        "url": request.url,
                        "method": request.method,
                        "post_data": request.post_data,
                        "headers": request.headers
                    })
                    print("📡 REQUEST CAPTURED:", request.method, request.url)

            def handle_response(response):
                if any(x in response.url.lower() for x in ["search", "claim", "sws", "api", "graphql"]):
                    try:
                        print("📥 RESPONSE:", response.status, response.url)
                    except Exception:
                        pass

            page.on("request", handle_request)
            page.on("response", handle_response)

            # -----------------------------
            # LOAD PAGE
            # -----------------------------
            page.goto(self.url, wait_until="networkidle")
            page.wait_for_timeout(3000)

            # -----------------------------
            # TRY TO TRIGGER SEARCH
            # -----------------------------
            inputs = page.query_selector_all("input")

            print(f"INPUT FIELDS FOUND: {len(inputs)}")

            if len(inputs) == 0:
                print("❌ NO INPUT FIELDS FOUND")
                browser.close()
                return []

            # Use first input as search field
            search_box = inputs[0]

            print("✍️ ENTERING TEST QUERY...")
            search_box.fill("John")

            page.wait_for_timeout(1000)

            print("🔍 TRIGGERING SEARCH (ENTER)")
            search_box.press("Enter")

            # wait for network calls
            page.wait_for_timeout(8000)

            # -----------------------------
            # OUTPUT RESULTS
            # -----------------------------
            print("\n============================")
            print("CAPTURED REQUESTS")
            print("============================")

            if not self.captured_requests:
                print("NO REQUESTS CAPTURED")
                print("\n⚠️ IMPORTANT: This means:")
                print("- Either no backend request is triggered")
                print("- OR results are rendered locally in JS (no API)")
            else:
                for req in self.captured_requests:
                    print("\n----------------------------")
                    print("URL:", req["url"])
                    print("METHOD:", req["method"])
                    print("POST DATA:", req["post_data"])

            # save for later pipeline step
            with open("texas_requests.json", "w") as f:
                json.dump(self.captured_requests, f, indent=2)

            browser.close()

            print("\n🚀 PIPELINE COMPLETE")
            return self.captured_requests
