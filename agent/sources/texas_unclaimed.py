from agent.sources.base_dom_scraper import BaseDOMScraper
from agent.sources.state_adapter import StateAdapter

class TexasUnclaimed:

    def __init__(self, driver):
        self.scraper = BaseDOMScraper(driver, "TX")

    def search_logic(self, driver, dom):

        # ⚠️ THESE SELECTORS WILL BE ADJUSTED ONCE SITE IS CONFIRMED
        rows = dom.get_elements("table tbody tr")

        results = []

        for r in rows:

            try:
                cols = r.find_elements("tag name", "td")

                if len(cols) < 5:
                    continue

                results.append({
                    "property_id": cols[0].text,
                    "owner_name": cols[1].text,
                    "address": cols[2].text,
                    "city": cols[3].text,
                    "zip": "",
                    "county": "",
                    "amount": cols[4].text,
                    "property_type": "UNKNOWN",
                    "year_reported": 0
                })

            except Exception:
                continue

        return results

    def run(self, url, max_records=50):

        raw = self.scraper.run(url, self.search_logic)

        return StateAdapter.normalize_list(raw, "TX")
