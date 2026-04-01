from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import os


class FloridaUnclaimedScraper:

    def __init__(self):
        print("🟢 Florida scraper initialized")

        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        self.driver = webdriver.Chrome(options=options)

    # -----------------------------
    # FULL PAGE INTROSPECTION TOOL
    # -----------------------------
    def dump_page_insights(self, label="debug"):

        os.makedirs("debug", exist_ok=True)

        print("\n🧠 PAGE INTROSPECTION START")

        html = self.driver.page_source

        # Save HTML
        with open(f"debug/{label}.html", "w", encoding="utf-8") as f:
            f.write(html)

        print(f"📄 HTML saved: debug/{label}.html")

        # Screenshot
        self.driver.save_screenshot(f"debug/{label}.png")
        print(f"📸 Screenshot saved: debug/{label}.png")

        # -----------------------------
        # IFRAME DETECTION
        # -----------------------------
        iframes = self.driver.find_elements(By.TAG_NAME, "iframe")
        print(f"🧩 Iframes found: {len(iframes)}")

        for i, frame in enumerate(iframes):
            print(f"   iframe {i}: {frame.get_attribute('src')}")

        # -----------------------------
        # SCRIPT INSPECTION (API hints)
        # -----------------------------
        scripts = self.driver.find_elements(By.TAG_NAME, "script")

        api_hits = []

        for s in scripts:
            src = s.get_attribute("src")
            if src:
                if any(x in src.lower() for x in ["api", "search", "claim", "unclaimed"]):
                    api_hits.append(src)

        print(f"\n🔍 Potential API scripts found: {len(api_hits)}")

        for api in api_hits[:10]:
            print("   API:", api)

        # -----------------------------
        # LINK INSPECTION
        # -----------------------------
        links = self.driver.find_elements(By.TAG_NAME, "a")

        print(f"\n🔗 Total links: {len(links)}")

        for l in links[:20]:
            href = l.get_attribute("href")
            text = l.text.strip()
            if href:
                print(f"   {text} -> {href}")

        print("\n🧠 PAGE INTROSPECTION END\n")

    # -----------------------------
    # MAIN SEARCH FLOW (DEBUG ONLY)
    # -----------------------------
    def search(self, query: str):

        print(f"🔎 Searching Florida Unclaimed for: {query}")

        try:
            url = "https://www.fltreasurehunt.gov/app/claim-search"
            self.driver.get(url)

            time.sleep(5)

            print("🌐 Page loaded")

            self.dump_page_insights("step1_inspect")

        except Exception as e:
            print(f"❌ Error: {e}")

        finally:
            self.driver.quit()

        return []
