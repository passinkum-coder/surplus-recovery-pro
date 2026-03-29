from scrapers.base_scraper import BaseScraper
from playwright.sync_api import sync_playwright
import json


class MiamiDadeScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            county_name="Miami-Dade",
            state="FL",
            url="https://www.miamidade.gov/Apps/PA/PAClaims/Home/UnclaimedProperty"
        )

    def scrape(self):
        captured = []

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            # capture ALL responses
            def handle_response(response):
                try:
                    ct = response.headers.get("content-type", "")
                    if "application/json" in ct:
                        try:
                            captured.append(response.json())
                        except:
                            pass
                except:
                    pass

            page.on("response", handle_response)

            page.goto(self.url, wait_until="networkidle")

            # 🔥 FORCE USER-LIKE ACTIONS
            page.wait_for_timeout(3000)

            # try triggering any JS search (if exists safely ignored if not found)
            try:
                page.keyboard.press("Enter")
                page.wait_for_timeout(5000)
            except:
                pass

            browser.close()

        results = []

        # extract whatever structure exists
        for item in captured:
            if isinstance(item, list):
                for r in item:
                    results.append({
                        "county": self.county_name,
                        "state": self.state,
                        "record_id": str(r.get("id") or r.get("name")),
                        "owner": r.get("owner"),
                        "amount": r.get("amount"),
                        "url": self.url
                    })

            elif isinstance(item, dict):
                for key in ["data", "results", "items"]:
                    if key in item and isinstance(item[key], list):
                        for r in item[key]:
                            results.append({
                                "county": self.county_name,
                                "state": self.state,
                                "record_id": str(r.get("id") or r.get("name")),
                                "owner": r.get("owner"),
                                "amount": r.get("amount"),
                                "url": self.url
                            })

        return results
