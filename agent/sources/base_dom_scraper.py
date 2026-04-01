from agent.sources.dom_engine import DOMEngine

class BaseDOMScraper:

    def __init__(self, driver, state_code):
        self.driver = driver
        self.dom = DOMEngine(driver)
        self.state = state_code

    def run(self, url, search_fn):
        print(f"🌐 Running LIVE DOM scraper for {self.state}")

        self.driver.get(url)
        self.dom.wait(3)

        raw_results = search_fn(self.driver, self.dom)

        print(f"📊 Raw results found: {len(raw_results)}")

        return raw_results
