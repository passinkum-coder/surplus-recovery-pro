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
        captured = []

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            # Capture JSON responses
            def handle_response(response):
                try:
                    if "application/json" in response.headers.get("content-type", ""):
                        captured.append(response.json())
                except:
                    pass

            page.on("response", handle_response)

            page.goto(self.url, wait_until="networkidle")
            page.wait_for_timeout(3000)

            # 🔥 STEP 1: FIND INPUT FIELD AND TYPE SEARCH VALUE
            try:
                inputs = page.query_selector_all("input")

                for inp in inputs:
                    try:
                        name = (inp.get_attribute("name") or "").lower()
                        placeholder = (inp.get_attribute("placeholder") or "").lower()

                        if "name" in name or "search" in name or "name" in placeholder:
                            inp.fill("a")  # 🔥 KEY STEP: FORCE RESULTS
                            break
                    except:
                        continue
            except:
                pass

            page.wait_for_timeout(2000)

            # 🔥 STEP 2: CLICK SEARCH BUTTON
            try:
                buttons = page.query_selector_all("button")

                for btn in buttons:
                    try:
                        text = btn.inner_text().lower()
                        if "search" in text or "submit" in text:
                            btn.click()
                            page.wait_for_timeout(6000)
                            break
                    except:
                        continue
            except:
                pass

            browser.close()

        # 🔥 STEP 3: EXTRACT DATA
        for item in captured:
            if isinstance(item, list):
                for r in item:
                    results.append({
                        "county": self.county_name,
                        "state": self.state,
                        "record_id": str(r.get("id") or r.get("name") or ""),
                        "owner": r.get("owner") or r.get("name"),
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
                                "record_id": str(r.get("id") or r.get("name") or ""),
                                "owner": r.get("owner") or r.get("name"),
                                "amount": r.get("amount"),
                                "url": self.url
                            })

        return results
