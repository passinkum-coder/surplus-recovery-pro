for scraper in scrapers:
    try:
        print(f"============================")
        print(f"Running: {scraper.county_name}")

        # 🔥 SAFE EXECUTION WRAPPER (handles different scraper designs)
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
            raise Exception(
                f"No valid method found for {scraper.county_name}. "
                f"Expected: run(), scrape(), fetch(), or get_data()"
            )

        # Normalize output
        if records is None:
            records = []

        print(f"COUNTY: {scraper.county_name}")
        print(f"RECORDS FOUND: {len(records)}")
        print(f"Upserting: {len(records)}")

    except Exception as e:
        print(f"ERROR in {scraper.county_name}: {e}")
