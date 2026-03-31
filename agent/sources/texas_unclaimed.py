import requests


class TexasUnclaimed:
    def __init__(self):
        self.base_url = "https://claimittexas.gov/app/claim-search"
        self.api_url = "https://claimittexas.gov/api/claim-search"
        self.headers = {
            "User-Agent": "Mozilla/5.0",
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json"
        }

    def fetch_page(self, page=1, query="A"):
        payload = {
            "lastName": query,
            "page": page,
            "pageSize": 50
        }

        try:
            response = requests.post(
                self.api_url,
                json=payload,
                headers=self.headers,
                timeout=30
            )

            if response.status_code != 200:
                return []

            data = response.json()

            return data.get("results", [])

        except Exception:
            return []

    def run(self, max_pages=5):
        all_results = []

        for page in range(1, max_pages + 1):
            print(f"Fetching Texas page {page}")

            results = self.fetch_page(page=page)

            if not results:
                break

            for item in results:
                all_results.append({
                    "state": "TX",
                    "county": None,
                    "owner": item.get("ownerName"),
                    "amount": item.get("amount"),
                    "city": item.get("city"),
                    "source": "Texas Unclaimed",
                    "status": "new"
                })

        print(f"Texas total records: {len(all_results)}")

        return all_results
