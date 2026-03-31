from dataclasses import dataclass
from typing import List, Dict, Any, Optional
import time

# Import your existing scrapers
from agent.sources.texas_unclaimed import TexasUnclaimed


# =========================
# USER TIER CONFIG
# =========================

TIER_CONFIG = {
    "free": {
        "max_states": 1,
        "max_counties": 1,
        "max_records": 5,
        "depth": "low"
    },
    "pro": {
        "max_states": 3,
        "max_counties": 5,
        "max_records": 50,
        "depth": "medium"
    },
    "elite": {
        "max_states": 50,
        "max_counties": 999,
        "max_records": 500,
        "depth": "deep"
    }
}


# =========================
# CORE ENGINE
# =========================

class AdaptiveScraperEngine:

    def __init__(self):
        self.scrapers = {
            "texas": TexasUnclaimed()
        }

    # -------------------------
    # ENTRY POINT
    # -------------------------
    def run_search(
        self,
        state: str,
        counties: List[str],
        query: str,
        tier: str = "free"
    ) -> Dict[str, Any]:

        print("\n🚀 ADAPTIVE ENGINE START")
        print("=" * 60)

        config = TIER_CONFIG.get(tier, TIER_CONFIG["free"])

        print(f"👤 Tier: {tier}")
        print(f"📍 State: {state}")
        print(f"🏘 Counties requested: {len(counties)}")

        # -------------------------
        # APPLY TIER LIMITS
        # -------------------------
        counties = counties[:config["max_counties"]]

        print(f"🔒 Counties allowed: {len(counties)}")

        results = []

        # -------------------------
        # ROUTING LOGIC
        # -------------------------
        if state.lower() == "texas":
            results = self._run_texas(counties, query, config)
        else:
            results = self._run_generic(state, counties, query, config)

        # -------------------------
        # FINAL NORMALIZATION
        # -------------------------
        output = {
            "state": state,
            "tier": tier,
            "total_results": len(results),
            "results": results[:config["max_records"]],
            "strategy": "adaptive_engine_v1"
        }

        print("\n========================")
        print("ENGINE COMPLETE")
        print("========================")
        print("TOTAL RESULTS:", len(results))

        return output

    # -------------------------
    # TEXAS ROUTE (YOUR FIXED SYSTEM)
    # -------------------------
    def _run_texas(self, counties, query, config):

        print("\n🇺🇸 Running Texas DOM scraper...")

        scraper = self.scrapers["texas"]

        results = []

        try:
            data = scraper.run(max_records=config["max_records"])

            for item in data:
                results.append({
                    "state": "TX",
                    "county": "unknown",
                    "query": query,
                    "data": item,
                    "source": "dom_scrape"
                })

        except Exception as e:
            print("❌ Texas scraper error:", str(e))

        return results

    # -------------------------
    # GENERIC ROUTE (FUTURE STATES)
    # -------------------------
    def _run_generic(self, state, counties, query, config):

        print(f"\n⚙️ Running generic scraper for {state}")

        results = []

        for county in counties:

            print(f"📍 Processing county: {county}")

            # Placeholder hybrid logic (future-proof)
            county_results = self._hybrid_scrape(state, county, query)

            for r in county_results:
                results.append({
                    "state": state,
                    "county": county,
                    "query": query,
                    "data": r,
                    "source": "hybrid"
                })

            time.sleep(0.5)  # rate control

        return results

    # -------------------------
    # HYBRID STRATEGY (FUTURE ENGINE CORE)
    # -------------------------
    def _hybrid_scrape(self, state, county, query):

        """
        This is where future upgrades go:
        - API detection
        - network capture
        - DOM fallback
        """

        # Placeholder until you wire other states
        return [{
            "message": f"No scraper yet for {state}-{county}",
            "query": query
        }]
