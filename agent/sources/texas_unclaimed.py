import re
import json
import requests


class TexasUnclaimed:
    def __init__(self):
        self.base_url = "https://www.claimittexas.gov/"
        self.max_records = 50

    def run(self, max_records=50):
        print("\n🚀 STARTING TEXAS JS BUNDLE EXTRACTION")
        print("=" * 50)

        self.max_records = max_records
        records = []

        # STEP 1: FETCH HOMEPAGE
        print("📡 Fetching homepage...")
        r = requests.get(self.base_url, timeout=30)
        html = r.text

        # STEP 2: DISCOVER JS FILES
        js_files = re.findall(r'src="([^"]+\.js)"', html)
        js_files = list(set(js_files))

        print(f"JS FILES FOUND: {len(js_files)}")

        # STEP 3: SCAN ALL JS FILES
        for js in js_files:
            url = js if js.startswith("http") else self.base_url.rstrip("/") + "/" + js

            print(f"\n🔍 SCANNING: {js}")

            try:
                res = requests.get(url, timeout=30)
                text = res.text

                # STEP 4: EXTRACT JS OBJECT CANDIDATES
                candidates = re.findall(r'\{[^{}]{30,}\}', text)

                print(f"OBJECTS FOUND: {len(candidates)}")

                for c in candidates:
                    parsed = self.normalize(c)
                    if parsed:
                        records.append(parsed)

                    if len(records) >= self.max_records:
                        print("\n⚠️ MAX RECORDS REACHED")
                        return records

            except Exception as e:
                print(f"❌ ERROR: {e}")

        print("\n========================")
        print("FINAL RESULTS")
        print("========================")
        print("TOTAL RECORDS:", len(records))

        return records

    # -----------------------------
    # NORMALIZER (CLEAN DATA ONLY)
    # -----------------------------
    def normalize(self, raw):
        try:
            cleaned = raw.replace("'", '"')

            data = json.loads(cleaned)

            # only keep meaningful records
            if not any(k in data for k in ["name", "owner", "amount", "address"]):
                return None

            return {
                "owner_name": data.get("name") or data.get("owner"),
                "address": data.get("address"),
                "amount": data.get("amount"),
                "county": data.get("county"),
                "state": "TX"
            }

        except:
            return None
