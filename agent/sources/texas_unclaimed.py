def _run_texas(self, counties, query, config):

    print("🇺🇸 Running REAL Texas scraper via adaptive engine")

    from sources.texas_unclaimed import TexasUnclaimed

    tx = TexasUnclaimed()
    raw_data = tx.run(max_records=50)

    print(f"RAW TEXAS RECORDS FOUND: {len(raw_data)}")

    # ----------------------------
    # CLEAN FILTER (INLINE SAFE)
    # ----------------------------
    cleaned = []

    for item in raw_data:

        text = item.get("text", "").strip()

        if not text:
            continue

        if "No properties" in text:
            continue

        if "Previous" in text:
            continue

        if "Select an Action" in text:
            continue

        if "Owner Name" in text and "Property Type" in text:
            continue

        if len(text) < 10:
            continue

        cleaned.append(item)

    print(f"CLEAN TEXAS RECORDS: {len(cleaned)}")

    return cleaned
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
