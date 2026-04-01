import os
from agent.database.supabase_client import SupabaseDB

# State source modules (we will wire these properly)
from agent.sources.florida_unclaimed import FloridaUnclaimedScraper

# (we will add these next)
# from agent.sources.georgia.georgia_foreclosure import GeorgiaScraper
# from agent.sources.texas.texas_foreclosure import TexasScraper


# ----------------------------
# CONFIG
# ----------------------------

STATE_CONFIG = {
    "GA": {
        "enabled": True,
        "module": "georgia"
    },
    "FL": {
        "enabled": True,
        "module": "florida"
    },
    "TX": {
        "enabled": True,
        "module": "texas"
    }
}


# ----------------------------
# ENGINE WRAPPER
# ----------------------------

class PipelineEngine:

    def __init__(self):
        self.db = SupabaseDB()

        # initialize scrapers
        self.fl_scraper = FloridaUnclaimedScraper()

        # placeholders for now
        self.ga_scraper = None
        self.tx_scraper = None

    def run_state(self, state: str, query: str):

        print("\n========================================")
        print(f"🚀 Running state pipeline: {state}")
        print(f"🔎 Query: {query}")

        results = []

        # ----------------------
        # FLORIDA
        # ----------------------
        if state == "FL":
            print("🇺🇸 Florida pipeline active")

            results = self.fl_scraper.search(query)

        # ----------------------
        # GEORGIA (not wired yet)
        # ----------------------
        elif state == "GA":
            print("🇺🇸 Georgia pipeline (NOT WIRED YET)")
            results = []  # placeholder until GA module added

        # ----------------------
        # TEXAS (not wired yet)
        # ----------------------
        elif state == "TX":
            print("🇺🇸 Texas pipeline (NOT WIRED YET)")
            results = []

        else:
            print("❌ Unsupported state")
            return []

        # ----------------------
        # SAVE TO SUPABASE
        # ----------------------
        if results:
            self.db.insert_records(results)
            print(f"🟢 Inserted {len(results)} records into Supabase")
        else:
            print("⚠️ No results to insert")

        return results


# ----------------------------
# MAIN ENTRY
# ----------------------------

def main():

    print("\n🚀 STARTING SURPLUS RECOVERY PRO PIPELINE")

    engine = PipelineEngine()

    # TEMP TEST RUN (you can later loop counties here)
    state = os.getenv("STATE", "FL")
    query = os.getenv("QUERY", "JOHN")

    engine.run_state(state, query)

    print("\n✅ PIPELINE COMPLETE")


if __name__ == "__main__":
    main()
