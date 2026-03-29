from scrapers.base_scraper import BaseScraper
import requests


class MiamiDadeScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            county_name="Miami-Dade",
            state="FL",
            url="https://www.miamidade.gov/Apps/PA/PAClaims/Home/UnclaimedProperty"
        )

    def scrape(self):
        session = requests.Session()

        headers = {
            "User-Agent": "Mozilla/5.0",
            "Accept": "application/json, text/plain, */*"
        }

        try:
            # Step 1: initialize session (cookies, tokens if any)
            session.get(self.url, headers=headers, timeout=30)

            # Step 2: attempt known API-style endpoints
            endpoints = [
                self.url + "/Search",
                self.url + "/GetData",
                self.url + "/api/search",
                self.url + "/api/claims"
            ]

            results = []

            for endpoint in endpoints:
                try:
                    r = session.get(endpoint, headers=headers, timeout=20)

                    if r.status_code != 200:
                        continue

                    try:
                        data = r.json()
                    except:
                        continue

                    # CASE 1: list response
                    if isinstance(data, list):
                        for item in data:
                            results.append({
                                "county": self.county_name,
                                "state": self.state,
                                "record_id": item.get("id") or item.get("name"),
                                "owner": item.get("owner"),
                                "amount": item.get("amount"),
                                "url": endpoint
                            })

                    # CASE 2: dict response
                    elif isinstance(data, dict):
                        for key in ["data", "results", "items"]:
                            if key in data and isinstance(data[key], list):
                                for item in data[key]:
                                    results.append({
                                        "county": self.county_name,
                                        "state": self.state,
                                        "record_id": item.get("id") or item.get("name"),
                                        "owner": item.get("owner"),
                                        "amount": item.get("amount"),
                                        "url": endpoint
                                    })

                except:
                    continue

            return results

        except Exception:
            return []
