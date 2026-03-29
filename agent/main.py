from scrapers.county_scrapers import load_scrapers


def main():
    # Load all scrapers from single source of truth
    scrapers = load_scrapers()

    print(f"TOTAL SCRAPERS LOADED: {len(scrapers)}")

    # Run each scraper safely
    for scraper in scrapers:
        try:
            print(f"============================")
            print(f"Running: {scraper.county_name}")
            
            records = scraper.run()

            # Handle case where run() returns None
            if records is None:
                records = []

            print(f"COUNTY: {scraper.county_name}")
            print(f"RECORDS FOUND: {len(records)}")

            # Optional: upsert logging if your scraper handles DB internally
            print(f"Upserting: {len(records)}")

        except Exception as e:
            print(f"ERROR in {scraper.county_name}: {e}")


if __name__ == "__main__":
    main()
