from agent.sources.texas_unclaimed import TexasUnclaimed


class AdaptiveScraperEngine:

    def __init__(self):
        print("🚀 Adaptive Engine Initialized")

    def run_search(self, state, counties, query, config):

        print("\n🚀 STARTING SEARCH PIPELINE")
        print("=" * 50)
        print(f"🧭 Strategy selected for {state}: dom_form")
        print(f"🔎 Query: {query}")
        print(f"🏘 Counties: {len(counties)}")

        if state.lower() == "texas":
            return self._run_texas(counties, query, config)

        print(f"⚠️ No handler for state: {state}")
        return []

    # -----------------------------
    # TEXAS LIVE DOM HANDLER
    # -----------------------------
    def _run_texas(self, counties, query, config):

        print("🇺🇸 Running REAL Texas scraper via adaptive engine")

        driver = config.get("driver", None)

        # 🧠 SAFE GUARD: prevents crash if browser not initialized
        if driver is None:
            print("⚠️ No Selenium driver found — running fallback mode (no DOM scraping)")
            return []

        try:
            tx = TexasUnclaimed(driver)

            # URL should come from config (or fallback default)
            url = config.get(
                "url",
                "https://example.com/texas-unclaimed-property"
            )

            results = tx.run(url=url)

            print(f"📊 Texas records returned: {len(results)}")

            return results

        except Exception as e:
            print(f"❌ Texas scraper failed: {e}")
            return []
