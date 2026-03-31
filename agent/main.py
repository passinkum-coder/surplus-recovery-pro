import os

from scrapers.county_scrapers import load_scrapers
from agent.engine.adaptive_engine import AdaptiveScraperEngine


def run_county_scrapers():
    print("========================================")
    print("RUNNING COUNTY SCRAPERS")
    print("========================================")

    scrapers = load_scrapers()

    print(f"TOTAL SCRAPERS LOADED: {len(scrapers)}")

    for scraper in scrapers:
        print("\n============================")
        print(f"Running: {scraper.county_name}")

        try:
            data = scraper.scrape()

            print(f"COUNTY: {scraper.county_name}")
            print(f"RECORDS FOUND: {len(data)}")

            if data:
                print(f"Upserting: {len(data)}")

        except Exception as e:
            print(f"ERROR in {scraper.county_name}: {e}")


def run_state_pipeline():
    print("\n========================================")
    print("RUNNING STATE PIPELINE (ADAPTIVE)")
    print("========================================")

    engine = AdaptiveScraperEngine()

    # You can later replace this with dynamic input
    state = "texas"
    counties = []
    query = "JOHN"
    config = {}

    result = engine.run_search(state, counties, query, config)

    print("\nFINAL RESULT:")
    print(result)


def main():
    print("\n🚀 STARTING DATA PIPELINE\n")

    # OLD SYSTEM (optional keep for now)
    run_county_scrapers()

    # NEW SYSTEM (THIS IS THE FIX)
    run_state_pipeline()

    print("\n✅ PIPELINE COMPLETE\n")


if __name__ == "__main__":
    main()
