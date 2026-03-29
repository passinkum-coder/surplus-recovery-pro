from scrapers.base_scraper import BaseScraper
from playwright.sync_api import sync_playwright


class MiamiDadeScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            county_name="Miami-Dade",
            state="FL",
            url="https://www.miamidade.gov/Apps/PA/PAClaims/Home/UnclaimedProperty"
        )


    def scrape(self):
        results = []

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            captured_json = []

            # 🔥 Capture API responses
            def handle_response(response):
                try:
                    ct = response.headers.get("content-type", "")
                    if "application/json" in ct:
                        try:
                            data = response.json()
                            captured_json.append(data)
                        except:
                            pass
                except:
                    pass

            page.on("response", handle_response)

            page.goto(self.url, wait_until="networkidle")
            page.wait_for_timeout(8000)

            browser.close()

        # 🔥 Extract records from captured JSON
        for item in captured_json:
            if isinstance(item, list):
                for r in item:
                    results.append({
                        "county": self.county_name,
                        "state": self.state,
                        "record_id": str(r.get("id") or r.get("record_id") or r.get("name") or ""),
                        "owner": r.get("owner") or r.get("name"),
                        "amount": r.get("amount"),
                        "url": self.url
                    })

            elif isinstance(item, dict):
                # sometimes API wraps data inside keys like "data"
                for key in ["data", "results", "items"]:
                    if key in item and isinstance(item[key], list):
                        for r in item[key]:
                            results.append({
                                "county": self.county_name,
                                "state": self.state,
                                "record_id": str(r.get("id") or r.get("record_id") or r.get("name") or ""),
                                "owner": r.get("owner") or r.get("name"),
                                "amount": r.get("amount"),
                                "url": self.url
                            })

        return results
