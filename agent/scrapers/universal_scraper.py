class UniversalScraper:
    def __init__(self, county_name=None, source_url=None, *args, **kwargs):
        self.county_name = county_name
        self.source_url = source_url


    # MAIN ENTRY POINT
    def run(self):
        html = self.get_page()
        records = self.parse(html)
        return self.normalize(records)


    def scrape(self):
        return self.run()


    def fetch(self):
        return self.run()


    def get_data(self):
        return self.run()


    # NORMALIZER (STANDARD OUTPUT CONTRACT)
    def normalize(self, records):
        if not records:
            return []

        normalized = []

        for r in records:
            normalized.append({
                "county": self.county_name,
                "source": self.source_url,
                "record_id": r.get("record_id"),
                "amount": r.get("amount"),
                "owner": r.get("owner"),
                "url": r.get("url")
            })

        return normalized


    # PLACEHOLDER: KEEP YOUR EXISTING IMPLEMENTATION IF YOU ALREADY HAVE ONE
    def get_page(self):
        raise NotImplementedError("get_page() must be implemented per scraper")


    # PLACEHOLDER: KEEP YOUR EXISTING PARSE LOGIC
    def parse(self, html):
        raise NotImplementedError("parse() must be implemented per scraper")
