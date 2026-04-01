import time

class DOMEngine:

    def __init__(self, driver):
        self.driver = driver

    def get_text(self, selector, default=""):
        try:
            return self.driver.find_element("css selector", selector).text.strip()
        except Exception:
            return default

    def get_elements(self, selector):
        try:
            return self.driver.find_elements("css selector", selector)
        except Exception:
            return []

    def wait(self, seconds=2):
        time.sleep(seconds)
