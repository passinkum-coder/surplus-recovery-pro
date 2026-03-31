import re
import requests


class TexasUnclaimed:
    def __init__(self):
        self.base_url = "https://www.claimittexas.gov/"

        # Known JS bundles (can be expanded later automatically)
        self.js_files = [
            "main.aaf8085b48ee1eb5.js",
            "runtime.*.js",
            "polyfills.*.js"
        ]

    def run(self, max_records=50):
        print("\n🚀 STARTING TEXAS JS BUNDLE EXTRACTION")
        print("=" * 50)

        all_records = []

        # STEP 1: fetch homepage to discover real bundle names
        print("📡 Fetching homepage...")
        r = requests.get(self.base_url, timeout=30)
        html = r.text

        # extract real JS files dynamically
        js_matches = re.findall(r'src="([^"]+\.js)"', html)
        js_files = list(set(js_matches))

        print(f"JS FILES FOUND: {len(js_files)}")

        # STEP 2: scan each JS file
        for js in js_files:
            if not js.startswith("http"):
                url = self.base_url.rstrip("/") + "/" + js
            else:
                url = js

            print(f"\n🔍 SCANNING: {js}")

            try:
                res = requests.get(url, timeout=30)
                text = res.text

                # STEP 3: extract JSON-like objects
                objects = re.findall(r'\{[^{}]{30,}\}', text)

                print(f"OBJECTS FOUND: {len(objects)}")

                for obj in objects:
                    if any(k in obj.lower() for k in [
                        "name", "owner", "amount", "address", "claim"
                    ]):
                        all_records.append(obj)

                        if len(all_records) >= max_records:
                            print("\n⚠️ MAX RECORDS REACHED")
                            return all_records

            except Exception as e:
                print(f"❌ ERROR FETCHING {js}: {e}")

        print("\n========================")
        print("FINAL RESULTS")
        print("========================")
        print("TOTAL RECORDS:", len(all_records))

        if len(all_records) == 0:
            print("\n⚠️ NO DATA FOUND")
            print("This confirms data is likely:")
            print("- runtime hydrated (Angular state)")
            print("- or encrypted after load")
            print("- or requires session auth")

        return all_records
