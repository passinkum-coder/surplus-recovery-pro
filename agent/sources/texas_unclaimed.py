from agent.sources.base_schema import BaseSchema

class TexasUnclaimed:

    def __init__(self):
        print("🇺🇸 Texas Unclaimed Scraper Initialized")

    def run(self, max_records=50):

        print("🚀 Texas unified scraper running...")

        raw = [
            {
                "property_id": "TX-001",
                "owner_name": "JOHN TEST",
                "address": "123 MAIN ST",
                "city": "HOUSTON",
                "zip": "77001",
                "county": "Harris",
                "amount": 120.50,
                "property_type": "UNCLAIMED",
                "year_reported": 2023
            }
        ]

        normalized = [
            BaseSchema.normalize(r, "TX")
            for r in raw
        ]

        print(f"📊 Texas normalized records: {len(normalized)}")

        return normalized
