import os

from agent.engine.adaptive_engine import AdaptiveScraperEngine
from agent.database.supabase_client import SupabaseDB


# -----------------------------
# SELENIUM DRIVER SETUP
# -----------------------------
def create_driver():
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options

        options = Options()
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")

        driver = webdriver.Chrome(options=options)

        print("🟢 Selenium driver created")
        return driver

    except Exception as e:
        print(f"⚠️ Selenium failed to start: {e}")
        return None


# -----------------------------
# MAIN ENTRY
# -----------------------------
def main():

    print("\n🚀 STARTING DATA PIPELINE\n")
    print("=" * 40)

    # Create engine + database
    engine = AdaptiveScraperEngine()
    db = SupabaseDB()

    # Create Selenium driver (THIS FIXES YOUR ISSUE)
    driver = create_driver()

    # -----------------------------
    # CONFIG PASSED INTO ENGINE
    # -----------------------------
    config = {
        "driver": driver,
        "url": os.getenv(
            "TARGET_URL",
            "https://example.com/texas-unclaimed-property"
        )
    }

    # -----------------------------
    # INPUT SETTINGS
    # -----------------------------
    state = "texas"
    counties = [
        "Miami-Dade",
        "Broward",
        "Palm Beach",
        "Hillsborough",
        "Orange",
        "Fulton",
        "Cobb",
        "Cherokee",
        "Harris",
        "Dallas"
    ]

    query = os.getenv("SEARCH_QUERY", "JOHN")

    # -----------------------------
    # RUN ENGINE
    # -----------------------------
    results = engine.run_search(
        state=state,
        counties=counties,
        query=query,
        config=config
    )

    print("\nFINAL RESULT:")
    print(results)

    # -----------------------------
    # PUSH TO SUPABASE
    # -----------------------------
    if results:
        db.upsert_records("unclaimed_property", results)
    else:
        print("⚠️ No results to insert into Supabase")

    print("\n✅ PIPELINE COMPLETE")


if __name__ == "__main__":
    main()
