from .base_scraper import BaseScraper
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
            url="https://www.gwinnettcounty.com/web/gwinnett/departments/financialservices/taxcommissioner/excessfunds"
        )

    def scrape(self):
        content = self.get_page()
        records = extract_table(content, self.county_name)
        return self.normalize(records)


class CobbScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            county_name="Cobb",
            url="https://www.cobbtax.org/property-taxes/excess-funds/"
        )

    def scrape(self):
        content = self.get_page()
        records = extract_table(content, self.county_name)
        return self.normalize(records)


class DeKalbScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            county_name="DeKalb",
            url="https://www.dekalbcountyga.gov/tax-commissioner/excess-funds"
        )

    def scrape(self):
    html = self.get_page()

    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")

    results = []

    elements = soup.find_all(["li", "p", "div", "tr"])

    for el in elements:
        text = self.normalize(el.get_text())

        if not text or len(text) < 12:
            continue

        keywords = [
            "tax", "sale", "excess", "fund", "property",
            "owner", "parcel", "amount", "$"
        ]

        if any(k in text.lower() for k in keywords):
            results.append({
                "county": self.county_name,
                "state": self.state,
                "data": text
            })

    return results

    def scrape(self):
        content = self.get_page()
        records = extract_table(content, self.county_name)
        return self.normalize(records)


class ClaytonScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            county_name="Clayton",
            url="https://www.claytoncountyga.gov/government/tax-commissioner/excess-funds"
        )

    def scrape(self):
        content = self.get_page()
        records = extract_table(content, self.county_name)
        return self.normalize(records)


class HenryScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            county_name="Henry",
            url="https://www.co.henry.ga.us/departments/tax_commissioner/excess_funds.php"
        )

    def scrape(self):
        content = self.get_page()
        records = extract_table(content, self.county_name)
        return self.normalize(records)


class ForsythScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            county_name="Forsyth",
            url="https://www.forsythco.com/Departments-Offices/Tax-Commissioner/Excess-Funds"
        )

    def scrape(self):
        content = self.get_page()
        records = extract_table(content, self.county_name)
        return self.normalize(records)


class HallScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            county_name="Hall",
            url="https://www.hallcounty.org/219/Excess-Funds"
        )

    def scrape(self):
        content = self.get_page()
        records = extract_table(content, self.county_name)
        return self.normalize(records)


class RichmondScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            county_name="Richmond",
            url="https://www.augustaga.gov/1235/Excess-Funds"
        )
def load_scrapers():
    return [
        CherokeeScraper(),
        # add your other Georgia counties here
    ]
