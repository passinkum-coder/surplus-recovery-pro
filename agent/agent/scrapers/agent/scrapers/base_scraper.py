
from playwright.sync_api import sync_playwright
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BaseScraper:
    def __init__(self, county_name, url, data_type="tax_sale"):
        self.county_name = county_name
        self.url = url
        self.data_type = data_type

    def get_page(self):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            )
            page = context.new_page()
            page.goto(self.url, timeout=30000, wait_until="networkidle")
            content = page.content()
            browser.close()
            return content

    def scrape(self):
        raise NotImplementedError("Each county scraper must implement scrape()")

    def normalize(self, records):
        """Ensure all records have required fields and correct types."""
        clean = []
        for r in records:
            if not r.get("property_address") or not r.get("surplus_amount"):
                continue
            clean.append({
                "county": self.county_name,
                "state": "Georgia",
                "property_address": str(r.get("property_address", "")).strip(),
                "owner_name": str(r.get("owner_name", "")).strip() or None,
                "parcel_id": str(r.get("parcel_id", "")).strip() or None,
                "sale_date": r.get("sale_date") or None,
                "surplus_amount": float(r.get("surplus_amount", 0)),
                "source_url": self.url,
                "data_type": self.data_type,
                "status": "active"
            })
        return clean
