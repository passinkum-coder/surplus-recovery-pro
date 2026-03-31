import re
import requests
from bs4 import BeautifulSoup


class TexasUnclaimed:
    def __init__(self):
        self.base_url = "https://www.claimittexas.gov/app/claim-search"
        self.js_links = []
        self.endpoints = set()

    def fetch_html(self):
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        r = requests.get(self.base_url, headers=headers, timeout=30)
        return r.text

    def extract_js_files(self, html):
        soup = BeautifulSoup(html, "html.parser")

        for script in soup.find_all("script"):
            src = script.get("src")
            if src and ".js" in src:
                if src.startswith("/"):
                    src = "https://www.claimittexas.gov" + src
                self.js_links.append(src)

    def download_js(self, url):
        try:
            r = requests.get(url, timeout=30)
            return r.text
        except Exception:
            return ""

    def scan_for_endpoints(self, js_text):
        patterns = [
            r"https://[a-zA-Z0-9./?=_-]+",
            r"/SWS/[a-zA-Z0-9/_-]+",
            r"/api/[a-zA-Z0-9/_-]+",
            r"graphql",
            r"fetch\\(\\s*['\"](.*?)['\"]",
            r"axios\\.[getpostPUTdelete]+\\(['\"](.*?)['\"]"
        ]

        for pattern in patterns:
            matches = re.findall(pattern, js_text, re.IGNORECASE)
            for m in matches:
                if isinstance(m, tuple):
                    m = m[0]
                self.endpoints.add(m)

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

        for e in sorted(self.endpoints):
            print(e)

        print("\nDONE RECON")
        return list(self.endpoints)
