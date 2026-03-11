from scrapers.base_scraper import BaseScraper
from processors.pdf_processor import extract_pdf
from processors.table_processor import extract_table
from playwright.sync_api import sync_playwright
import logging

logger = logging.getLogger(__name__)


class FultonScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            county_name="Fulton",
            url="https://www.fultoncountyga.gov/tax-commissioner/excess-funds"
        )

    def scrape(self):
        content = self.get_page()
        soup_check = content.lower()
        if ".pdf" in soup_check:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(content, "html.parser")
            pdf_link = soup.find("a", href=lambda h: h and h.endswith(".pdf"))
            if pdf_link:
                pdf_url = pdf_link["href"]
                if not pdf_url.startswith("http"):
                    pdf_url = "https://www.fultoncountyga.gov" + pdf_url
                records = extract_pdf(pdf_url, self.county_name)
                return self.normalize(records)
        records = extract_table(content, self.county_name)
        return self.normalize(records)


class GwinnettScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            county_name="Gwinnett",
            url="https://www.
