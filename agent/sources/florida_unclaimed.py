from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
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

    # ----------------------------
    # DEBUG HELPERS
    # ----------------------------
    def save_debug(self, name="debug"):
        os.makedirs("debug", exist_ok=True)

        # Screenshot
        screenshot_path = f"debug/{name}.png"
        self.driver.save_screenshot(screenshot_path)
        print(f"📸 Screenshot saved: {screenshot_path}")

        # HTML dump
        html_path = f"debug/{name}.html"
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(self.driver.page_source)

        print(f"📄 HTML saved: {html_path}")

    # ----------------------------
    # MAIN SEARCH
    # ----------------------------
    def search(self, query: str):

        print(f"🔎 Searching Florida Unclaimed for: {query}")

        results = []

        try:
            url = "https://fltreasurehunt.gov/"
            self.driver.get(url)

            time.sleep(3)

            print("🌐 Page loaded")
            self.save_debug("step1_home")

            # Try clicking search
            buttons = self.driver.find_elements(By.TAG_NAME, "a")
            clicked = False

            for btn in buttons:
                if "Search" in btn.text:
                    btn.click()
                    clicked = True
                    break

            print(f"🔘 Search button clicked: {clicked}")

            time.sleep(3)
            self.save_debug("step2_search_page")

            # Try input
            inputs = self.driver.find_elements(By.TAG_NAME, "input")

            input_found = False
            for inp in inputs:
                name = inp.get_attribute("name") or ""
                if "last" in name.lower():
                    inp.send_keys(query)
                    input_found = True
                    break

            print(f"⌨️ Input field found: {input_found}")

            # Submit
            try:
                self.driver.find_element(By.TAG_NAME, "button").click()
                print("🚀 Form submitted")
            except:
                print("⚠️ Submit button not found")

            time.sleep(5)
            self.save_debug("step3_results")

            # ----------------------------
            # TRY MULTIPLE EXTRACTION METHODS
            # ----------------------------

            # Method 1: table rows
            rows = self.driver.find_elements(By.CSS_SELECTOR, "table tbody tr")
            print(f"📊 Table rows found: {len(rows)}")

            for row in rows:
                cols = row.find_elements(By.TAG_NAME, "td")

                if len(cols) >= 3:
                    results.append({
                        "full_name": cols[0].text,
                        "property_address": cols[1].text,
                        "amount": cols[2].text,
                        "state": "FL",
                        "source": "unclaimed_property"
                    })

            # Method 2: fallback text scan
            if not results:
                print("⚠️ No table results — scanning page text")

                text = self.driver.page_source.lower()

                if query.lower() in text:
                    print("🟡 Query exists in page but not structured")
                else:
                    print("🔴 Query NOT found in page")

        except Exception as e:
            print(f"❌ Scraper error: {e}")
            self.save_debug("error")

        finally:
            self.driver.quit()

        print(f"📊 FINAL RESULTS: {len(results)}")

        return results
