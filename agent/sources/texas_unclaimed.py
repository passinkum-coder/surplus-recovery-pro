from playwright.sync_api import sync_playwright


class TexasUnclaimed:
    def __init__(self):
        self.url = "https://www.claimittexas.gov/app/claim-search"

    def run(self, max_records=50):
        print("\n🚀 STARTING TEXAS FORM-BASED PIPELINE")
        print("=" * 60)

        results = []

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            # -----------------------------
            # LOAD PAGE
            # -----------------------------
            print("📡 Loading page...")
            page.goto(self.url, wait_until="networkidle")
            page.wait_for_timeout(3000)

            # -----------------------------
            # FIND FORM FIELDS (CRITICAL FIX)
            # -----------------------------
            inputs = page.query_selector_all("input")

            last_name = None
            first_name = None

            for i in inputs:
                try:
                    name = (i.get_attribute("name") or "").lower()
                    placeholder = (i.get_attribute("placeholder") or "").lower()

                    if "last" in name or "last" in placeholder:
                        last_name = i
                    elif "first" in name or "first" in placeholder:
                        first_name = i
                except:
                    pass

            if not last_name:
                print("❌ Last name field not found")
                browser.close()
                return []

            # -----------------------------
            # FILL FORM PROPERLY
            # -----------------------------
            print("✍️ Filling last name: JOHN")
            last_name.fill("john")

            if first_name:
                print("✍️ Filling first name: TEST")
                first_name.fill("test")

            page.wait_for_timeout(1000)

            # -----------------------------
            # SUBMIT FORM (REAL TRIGGER)
            # -----------------------------
            print("🖱 Submitting form...")

            buttons = page.query_selector_all("button")

            submitted = False
            for b in buttons:
                try:
                    txt = (b.inner_text() or "").lower()
                    if "search" in txt or "submit" in txt or "find" in txt:
                        b.click()
                        submitted = True
                        print("✅ Form submitted via button")
                        break
                except:
                    pass

            if not submitted:
                print("⚠️ No submit button found — pressing Enter fallback")
                page.keyboard.press("Enter")

            # -----------------------------
            # WAIT FOR UI UPDATE (NOT NETWORK)
            # -----------------------------
            page.wait_for_timeout(8000)

            # -----------------------------
            # SCRAPE RESULTS FROM DOM (IMPORTANT FIX)
            # -----------------------------
            print("📊 Extracting results from page DOM...")

            rows = page.query_selector_all("table tr, .result, .record, li")

            for r in rows:
                try:
                    text = r.inner_text().strip()
                    if text and len(text) > 5:
                        results.append({"text": text})
                except:
                    pass

            browser.close()

        print("\n========================")
        print("FINAL RESULTS")
        print("========================")
        print("TOTAL RECORDS:", len(results))

        return results[:max_records]
