from dataclasses import dataclass
from typing import List, Dict, Any
import time

from agent.engine.state_registry import STATE_STRATEGY


class AdaptiveScraperEngine:

    def __init__(self):
        print("🚀 Adaptive Engine Initialized")

    # =========================================================
    # MAIN ENTRY POINT
    # =========================================================
    def run_search(self, state: str, counties: list, query: str, config: dict):

        print("\n🚀 STARTING SEARCH PIPELINE")
        print("=" * 50)

        state = (state or "").strip().lower()

        strategy = STATE_STRATEGY.get(state, "dom_form")

        print(f"🧭 Strategy selected for {state}: {strategy}")
        print(f"🔎 Query: {query}")
        print(f"🏘 Counties: {len(counties)}")

        results = []

        if strategy == "dom_form":

            if state == "texas":
                results = self._run_texas(counties, query, config)
            else:
                results = self._run_dom_generic(state, counties, query, config)

        elif strategy == "api":
            results = self._run_api(state, counties, query, config)

        elif strategy == "hybrid":
            results = self._run_hybrid(state, counties, query, config)

        else:
            print("⚠ Unknown strategy → defaulting to DOM")
            results = self._run_dom_generic(state, counties, query, config)

        print("\n========================")
        print("PIPELINE COMPLETE")
        print("========================")
        print("TOTAL RESULTS:", len(results))

        return {
            "state": state,
            "strategy": strategy,
            "total_results": len(results),
            "results": results
        }

    # =========================================================
    # TEXAS REAL SCRAPER
    # =========================================================
    def _run_texas(self, counties, query, config):

        print("🇺🇸 Running REAL Texas scraper via adaptive engine")

        from sources.texas_unclaimed import TexasUnclaimed

        tx = TexasUnclaimed()
        data = tx.run(max_records=50)

        print(f"TEXAS RECORDS FOUND: {len(data)}")

        return data

    # =========================================================
    # DOM SCRAPER (FLORIDA + OTHERS)
    # =========================================================
    def _run_dom_generic(self, state, counties, query, config):

        print(f"🏛 Running DOM scraper for {state}...")

        state = (state or "").strip().lower()

        # -----------------------------
        # FLORIDA REAL IMPLEMENTATION
        # -----------------------------
        if state == "florida":
            try:
                from sources.florida_unclaimed import FloridaUnclaimed

                scraper = FloridaUnclaimed()
                data = scraper.run(max_records=50)

                print(f"🌴 Florida records found: {len(data)}")

                return data

            except Exception as e:
                print(f"❌ Florida scraper failed: {e}")
                return []

        # -----------------------------
        # DEFAULT FALLBACK
        # -----------------------------
        print(f"⚠ No DOM scraper implemented for: {state}")
        return []

    # =========================================================
    # API SCRAPER
    # =========================================================
    def _run_api(self, state, counties, query, config):
        print(f"🌐 Running API scraper for {state}...")
        return []

    # =========================================================
    # HYBRID SCRAPER
    # =========================================================
    def _run_hybrid(self, state, counties, query, config):
        print(f"⚡ Running hybrid scraper for {state}...")
        return []
