import re
import requests
from bs4 import BeautifulSoup


class TexasUnclaimed:
    def __init__(self):
        self.base_url = "https://www.claimittexas.gov/app/claim-search"
        self.js_links = []
        self.endpoints = set()

    # -----------------------------
    # FETCH HTML
    # -----------------------------
    def fetch_html(self):
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        try:
            r = requests.get(self.base_url, headers=headers, timeout=30)
            return r.text or ""
        except Exception:
            return ""

    # -----------------------------
    # EXTRACT JS FILES
    # -----------------------------
    def extract_js_files(self, html):
        if not isinstance(html, str):
            return

        soup = BeautifulSoup(html, "html.parser")

        for script in soup.find_all("script"):
            src = script.get("src")
            if src and ".js" in src:
                if src.startswith("/"):
                    src = "https://www.claimittexas.gov" + src
                self.js_links.append(src)

    # -----------------------------
    # PATCH 1: SAFE JS DOWNLOAD
    # -----------------------------
    def download_js(self, url):
        try:
            r = requests.get(url, timeout=30)
            if r.status_code == 200:
                return r.text or ""
            return ""
        except Exception:
            return ""

    # -----------------------------
    # PATCH 2: SAFE SCAN FUNCTION
    # -----------------------------
    def scan_for_endpoints(self, js_text):
        if not isinstance(js_text, str):
            return

        patterns = [
            r"https://[a-zA-Z0-9./?=_\-]+",
            r"/SWS/[a-zA-Z0-9/_\-]+",
            r"/api/[a-zA-Z0-9/_\-]+",
            r"graphql",
            r"fetch\\(\\s*['\"](.*?)['\"]",
            r"axios\\.[a-zA-Z]+\\(['\"](.*?)['\"]"
        ]

        for pattern in patterns:
            try:
                matches = re.findall(pattern, js_text, re.IGNORECASE)

                for m in matches:
                    if isinstance(m, tuple):
                        m = m[0]
                    if isinstance(m, str) and len(m) > 3:
                        self.endpoints.add(m)

            except Exception:
                continue

    # -----------------------------
    # MAIN RUN
    # -----------------------------
    def run(self, max_records=50):
        print("🚀 STARTING JS BUNDLE RECON")

        html = self.fetch_html()
        self.extract_js_files(html)

        print(f"JS FILES FOUND: {len(self.js_links)}")

        for js in self.js_links:
            print(f"SCANNING: {js}")
            content = self.download_js(js)
            self.scan_for_endpoints(content)

        print("\n========================")
        print("DISCOVERED ENDPOINTS")
        print("========================")

        if not self.endpoints:
            print("NO ENDPOINTS FOUND (IMPORTANT SIGNAL)")
        else:
            for e in sorted(self.endpoints):
                print(e)

        print("\nDONE RECON")
        return list(self.endpoints)
