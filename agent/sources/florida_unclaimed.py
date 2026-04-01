import requests
import json


class FloridaUnclaimedScraper:

    def __init__(self):
        print("🟢 Florida API scraper initialized")

        self.session = requests.Session()

        self.session.headers.update({
            "User-Agent": "Mozilla/5.0",
            "Accept": "application/json, text/plain, */*",
        })

    def test_known_endpoints(self, query: str):

        print(f"🔎 Testing API paths for: {query}")

        base_urls = [
            "https://www.fltreasurehunt.gov",
            "https://www.fltreasurehunt.gov/api",
            "https://www.fltreasurehunt.gov/app",
        ]

        test_paths = [
            "/search",
            "/api/search",
            "/api/claim-search",
            "/claims/search",
            "/unclaimed/search",
            "/property/search",
        ]

        results_found = []

        for base in base_urls:
            for path in test_paths:

                url = base + path
                params = {"q": query, "name": query, "search": query}

                try:
                    r = self.session.get(url, params=params, timeout=10)

                    print(f"→ {url} [{r.status_code}]")

                    if r.status_code == 200:

                        content_type = r.headers.get("content-type", "")

                        if "json" in content_type:
                            print("🟢 JSON RESPONSE FOUND")
                            try:
                                data = r.json()
                                results_found.append({
                                    "url": url,
                                    "data": data
                                })
                            except:
                                pass

                        elif len(r.text) > 200 and query.lower() in r.text.lower():
                            print("🟡 POSSIBLE HTML MATCH")

                except Exception as e:
                    print(f"❌ {url} failed: {e}")

        return results_found

    def search(self, query: str):

        print(f"\n🚀 API SEARCH START: {query}\n")

        results = self.test_known_endpoints(query)

        print("\n📊 FINAL RESULTS:")
        print(json.dumps(results, indent=2)[:2000])

        return results
