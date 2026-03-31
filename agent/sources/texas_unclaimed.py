from playwright.sync_api import sync_playwright


class TexasUnclaimed:
    def __init__(self):
        self.url = "https://claimittexas.gov/app/claim-search"

    def run(self, max_records=50):
        results = []

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            page.goto(self.url, wait_until="networkidle")
            page.wait_for_timeout(3000)

            # 🔥 STEP 1: FIND SEARCH INPUT AND TYPE
            try:
                inputs = page.query_selector_all("input")

                for inp in inputs:
                    try:
                        placeholder = (inp.get_attribute("placeholder") or "").lower()
                        name = (inp.get_attribute("name") or "").lower()

                        if "name" in placeholder or "name" in name:
                            inp.fill("a")  # force results
                            break
                    except:
                        continue
            except:
                pass

            page.wait_for_timeout(2000)

            # 🔥 STEP 2: CLICK SEARCH BUTTON
            try:
                buttons = page.query_selector_all("button")

                for btn in buttons:
                    try:
                        text = btn.inner_text().lower()
                        if "search" in text:
                            btn.click()
                            page.wait_for_timeout(6000)
                            break
                    except:
                        continue
            except:
                pass

            # 🔥 STEP 3: SCRAPE RESULTS TABLE
            rows = page.query_selector_all("table tr")

            for row in rows[:max_records]:
                try:
                    cols = row.query_selector_all("td")

                    if len(cols) < 2:
                        continue

                    results.append({
                        "state": "TX",
                        "county": None,
                        "owner": cols[0].inner_text().strip(),
                        "amount": cols[1].inner_text().strip() if len(cols) > 1 else None,
                        "city": cols[2].inner_text().strip() if len(cols) > 2 else None,
                        "source": "Texas Unclaimed",
                        "status": "new"
                    })
                except:
                    continue

            browser.close()

        print(f"Texas total records: {len(results)}")

        return results
