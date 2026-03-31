from playwright.sync_api import sync_playwright


class TexasUnclaimed:
    def __init__(self):
        self.url = "https://claimittexas.gov/app/claim-search"

    def run(self, max_records=50):

        captured = []

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            def log_request(request):
                print("REQ:", request.method, request.url)

            def log_response(response):
                print("RES:", response.status, response.url)

            page.on("request", log_request)
            page.on("response", log_response)

            page.goto(self.url, wait_until="networkidle")
            page.wait_for_timeout(10000)

            browser.close()

        print("DONE DEBUG RUN")
        return []
