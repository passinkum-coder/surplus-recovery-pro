from scrapers.county_scrapers import load_scrapers


def main():
    # Load scrapers FIRST
    scrapers = load_scrapers()

    print(f"TOTAL SCRAPERS LOADED: {len(scrapers)}")

    # Loop through scrapers
    for scraper in scrapers:
        try:
            print(f"============================")
            print(f"Running: {scraper.county_name}")

            # Flexible execution method support
            records = []

            if hasattr(scraper, "run"):
                records = scraper.run()
            elif hasattr(scraper, "scrape"):
                records = scraper.scrape()
            elif hasattr(scraper, "fetch"):
                records = scraper.fetch()
            elif hasattr(scraper, "get_data"):
                records = scraper.get_data()
            else:
                raise Exception(f"No valid method for {scraper.county_name}")

            if records is None:
                records = []

            print(f"COUNTY: {scraper.county_name}")
            print(f"RECORDS FOUND: {len(records)}")
            print(f"Upserting: {len(records)}")

        except Exception as e:
            print(f"ERROR in {scraper.county_name}: {e}")


if __name__ == "__main__":
    main()
