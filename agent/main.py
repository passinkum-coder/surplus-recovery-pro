from scrapers.county_scrapers import load_scrapers as load_ga
from scrapers.florida_scrapers import load_scrapers as load_fl
from scrapers.texas_scrapers import load_scrapers as load_tx


def upsert_records(records):
    print("Upserting:", len(records))


def run_all_scrapers():
    scrapers = []

    # Load all states
    scrapers += load_ga()
    scrapers += load_fl()
    scrapers += load_tx()

    print(f"TOTAL SCRAPERS LOADED: {len(scrapers)}")

    for scraper in scrapers:
        print("\n============================")
        print("Running:", scraper.county_name)

        try:
            records = scraper.scrape()

            print("COUNTY:", scraper.county_name)
            print("RECORDS FOUND:", len(records) if records else 0)

            if records:
                upsert_records(records)

        except Exception as e:
            print("ERROR:", scraper.county_name, str(e))


if __name__ == "__main__":
    run_all_scrapers()
