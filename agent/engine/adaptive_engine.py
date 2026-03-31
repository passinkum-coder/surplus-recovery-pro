def _run_dom_generic(self, state, counties, query, config):

    print(f"🏛 Running DOM scraper for {state}...")

    # Normalize state input
    state = (state or "").strip().lower()

    # -----------------------------
    # FLORIDA IMPLEMENTATION
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
    # DEFAULT FALLBACK (OTHER STATES)
    # -----------------------------
    print(f"⚠ No scraper implemented for state: {state}")
    return []
