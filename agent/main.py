from scrapers.cherokee import CherokeeScraper

def upsert_records(records):
    print("Upserting:", len(records))

scrapers = [
    CherokeeScraper(),
]

for scraper in scrapers:
    print("Running", scraper.county_name)

    try:
        records = scraper.scrape()

        print("COUNTY:", scraper.county_name)
        print("RECORDS:", records)
        print("COUNT:", len(records) if records else 0)

        if records:
            upsert_records(records)

    except Exception as e:
        print("Error:", scraper.county_name, e)
