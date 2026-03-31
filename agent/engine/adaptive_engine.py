from dataclasses import dataclass
from typing import List, Dict, Any, Optional
import time

from agent.engine.state_registry import STATE_STRATEGY


class AdaptiveScraperEngine:

    def __init__(self):
        print("🚀 Adaptive Engine Initialized")

    # -------------------------
    # MAIN ENTRY POINT
    # -------------------------
    def run_search(self, state: str, counties: list, query: str, config: dict):

        print("\n🚀 STARTING SEARCH PIPELINE")
        print("=" * 50)

        # Normalize input
        state = state.lower()

        # Get strategy from registry
        strategy = STATE_STRATEGY.get(state, "dom_form")

        print(f"🧭 Strategy selected for {state}: {strategy}")
        print(f"🔎 Query: {query}")
        print(f"🏘 Counties: {len(counties)}")

        results = []

        # -------------------------
        # ROUTING LOGIC
        # -------------------------
        if strategy == "dom_form":

            if state == "texas":
                print("🇺🇸 Running Texas scraper")
                results = self._run_texas(counties, query, config)

            else:
                print(f"🏛 Running DOM scraper for {state}")
                results = self._run_dom_generic(state, counties, query, config)

        elif strategy == "api":
            print(f"🌐 Running API scraper for {state}")
            results = self._run_api(state, counties, query, config)

        elif strategy == "hybrid":
            print(f"⚡ Running Hybrid scraper for {state}")
            results = self._run_hybrid(state, counties, query, config)

        else:
            print("⚠️ Unknown strategy → defaulting to DOM")
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

    # -------------------------
    # TEXAS SCRAPER (YOU ALREADY HAVE REAL LOGIC)
    # -------------------------
    def _run_texas(self, counties, query, config):
        print("Running Texas logic...")
        return []

    # -------------------------
    # GENERIC DOM SCRAPER (USED FOR FLORIDA ETC)
    # -------------------------
    def _run_dom_generic(self, state, counties, query, config):
        print(f"Running generic DOM scraper for {state}...")
        return []

    # -------------------------
    # API SCRAPER (PLACEHOLDER)
    # -------------------------
    def _run_api(self, state, counties, query, config):
        print(f"Running API scraper for {state}...")
        return []

    # -------------------------
    # HYBRID SCRAPER (PLACEHOLDER)
    # -------------------------
    def _run_hybrid(self, state, counties, query, config):
        print(f"Running hybrid scraper for {state}...")
        return []
