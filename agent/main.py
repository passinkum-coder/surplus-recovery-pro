import os

# --- EXISTING SCRAPER IMPORT ---
from scrapers.county_scrapers import load_scrapers

# --- NEW STATE DATA SOURCE ---
from sources.texas_unclaimed import TexasUnclaimed


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
                # 👉 plug your Supabase insert here later

        except Exception as e:
            print(f"ERROR in {scraper.county_name}: {e}")


def run_texas_pipeline():
    print("\n========================================")
    print("RUNNING STATE PIPELINE: TEXAS")
    print("========================================")

    tx = TexasUnclaimed()

    data = tx.run(max_pages=3)

    print(f"\nTEXAS RECORDS FOUND: {len(data)}")

    if data:
        print(f"Upserting: {len(data)}")
        # 👉 plug your Supabase insert here later


def main():
    print("\n🚀 STARTING DATA PIPELINE\n")

    # --- RUN OLD SYSTEM (safe to keep) ---
    run_county_scrapers()

    # --- RUN NEW SYSTEM (REAL DATA) ---
    run_texas_pipeline()

    print("\n✅ PIPELINE COMPLETE\n")


if __name__ == "__main__":
    main()
