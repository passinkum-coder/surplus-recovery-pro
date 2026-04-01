import os
from agent.database.supabase_client import SupabaseDB
from agent.sources.florida_api import FloridaAPIScraper


def main():
    print("\n🚀 STARTING SURPLUS RECOVERY PRO PIPELINE\n")

    # Initialize DB (optional if you insert later)
    db = SupabaseDB()

    print("🟢 Supabase connected")
    print("🟢 Florida Playwright scraper initialized")

    # -----------------------------
    # CONFIG
    # -----------------------------
    query = "SMITH"

    # -----------------------------
    # INIT SCRAPER
    # -----------------------------
    scraper = FloridaUnclaimedScraper()

    print("\n========================================")
    print("🚀 Running state pipeline: FL")
    print(f"🔎 Query: {query}")
    print("🇺🇸 Florida Playwright pipeline active\n")

    # -----------------------------
    # RUN PLAYWRIGHT SCRAPER
    # -----------------------------
    results = scraper.search(query)

    # -----------------------------
    # OUTPUT RESULTS
    # -----------------------------
    print("\n📊 FINAL RESULTS:")
    print(results)

    # -----------------------------
    # OPTIONAL: INSERT INTO SUPABASE
    # -----------------------------
    if results:
        try:
            db.insert("fl_unclaimed_results", {
                "query": query,
                "results": results
            })
            print("🟢 Results inserted into Supabase")
        except Exception as e:
            print(f"⚠️ Supabase insert failed: {e}")

    print("\n✅ PIPELINE COMPLETE")


if __name__ == "__main__":
    main()
