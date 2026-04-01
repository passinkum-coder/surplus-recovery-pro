from agent.database.supabase_client import SupabaseDB
from agent.sources.florida_unclaimed import FloridaUnclaimedScraper


def main():
    print("\n🚀 STARTING SURPLUS RECOVERY PRO PIPELINE\n")

    db = SupabaseDB()

    print("🟢 Supabase connected")
    print("🟢 Florida Playwright scraper initialized")

    query = "SMITH"

    print("\n========================================")
    print("🚀 Running state pipeline: FL")
    print(f"🔎 Query: {query}")
    print("🇺🇸 Florida Playwright pipeline active\n")

    scraper = FloridaUnclaimedScraper()

    results = scraper.search(query)

    print("\n📊 FINAL RESULTS:")
    print(results)

    # optional insert
    if results:
        try:
            db.insert("fl_unclaimed_results", {
                "query": query,
                "results": results
            })
            print("🟢 Inserted into Supabase")
        except Exception as e:
            print(f"⚠️ DB error: {e}")

    print("\n✅ PIPELINE COMPLETE")


if __name__ == "__main__":
    main()
