from scrapers.base_scraper import BaseScraper
from processors.pdf_processor import extract_pdf
from processors.table_processor import extract_table
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__)


class HarrisScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            county_name="Harris",
            url="https://www.harriscountytax.com/surplus-funds"
        )
        self.state = "Texas"

    def scrape(self):
        content = self.get_page()
        soup = BeautifulSoup(content, "html.parser")
        pdf_link = soup.find("a", href=lambda h: h and h.lower().endswith(".pdf"))
        if pdf_link:
            pdf_url = pdf_link["href"]
            if not pdf_url.startswith("http"):
                pdf_url = "https://www.harriscountytax.com" + pdf_url
            records = extract_pdf(pdf_url, self.county_name)
        else:
            records = extract_table(content, self.county_name)
        return self.normalize(records)

    def normalize(self, records):
        clean = []
        for r in records:
            if not r.get("property_address") or not r.get("surplus_amount"):
                continue
            clean.append({
                "county": self.county_name,
                "state": self.state,
                "property_address": str(r.get("property_address", "")).strip(),
                "owner_name": str(r.get("owner_name", "")).strip() or None,
                "parcel_id": str(r.get("parcel_id", "")).strip() or None,
                "sale_date": r.get("sale_date") or None,
                "surplus_amount": float(r.get("surplus_amount", 0)),
                "source_url": self.url,
                "data_type": "tax_sale",
                "status": "active"
            })
        return clean


class DallasScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            county_name="Dallas",
            url="https://www.dallascounty.org/departments/tax/surplus-funds.php"
        )
        self.state = "Texas"

    def scrape(self):
        content = self.get_page()
        records = extract_table(content, self.county_name)
        return self.normalize(records)

    def normalize(self, records):
        clean = []
        for r in records:
            if not r.get("property_address") or not r.get("surplus_amount"):
                continue
            clean.append({
                "county": self.county_name,
                "state": self.state,
                "property_address": str(r.get("property_address", "")).strip(),
                "owner_name": str(r.get("owner_name", "")).strip() or None,
                "parcel_id": str(r.get("parcel_id", "")).strip() or None,
                "sale_date": r.get("sale_date") or None,
                "surplus_amount": float(r.get("surplus_amount", 0)),
                "source_url": self.url,
                "data_type": "tax_sale",
                "status": "active"
            })
        return clean


class TarrantScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            county_name="Tarrant",
            url="https://www.tarrantcounty.com/en/tax/property-tax/surplus-funds.html"
        )
        self.state = "Texas"

    def scrape(self):
        content = self.get_page()
        records = extract_table(content, self.county_name)
        return self.normalize(records)

    def normalize(self, records):
        clean = []
        for r in records:
            if not r.get("property_address") or not r.get("surplus_amount"):
                continue
            clean.append({
                "county": self.county_name,
                "state": self.state,
                "property_address": str(r.get("property_address", "")).strip(),
                "owner_name": str(r.get("owner_name", "")).strip() or None,
                "parcel_id": str(r.get("parcel_id", "")).strip() or None,
                "sale_date": r.get("sale_date") or None,
                "surplus_amount": float(r.get("surplus_amount", 0)),
                "source_url": self.url,
                "data_type": "tax_sale",
                "status": "active"
            })
        return clean


class BexarScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            county_name="Bexar",
            url="https://www.bexar.org/2923/Surplus-Funds"
        )
        self.state = "Texas"

    def scrape(self):
        content = self.get_page()
        records = extract_table(content, self.county_name)
        return self.normalize(records)

    def normalize(self, records):
        clean = []
        for r in records:
            if not r.get("property_address") or not r.get("surplus_amount"):
                continue
            clean.append({
                "county": self.county_name,
                "state": self.state,
                "property_address": str(r.get("property_address", "")).strip(),
                "owner_name": str(r.get("owner_name", "")).strip() or None,
                "parcel_id": str(r.get("parcel_id", "")).strip() or None,
                "sale_date": r.get("sale_date") or None,
                "surplus_amount": float(r.get("surplus_amount", 0)),
                "source_url": self.url,
                "data_type": "tax_sale",
                "status": "active"
            })
        return clean


class TravisScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            county_name="Travis",
            url="https://www.traviscountytax.org/surplus-funds"
        )
        self.state = "Texas"

    def scrape(self):
        content = self.get_page()
        records = extract_table(content, self.county_name)
        return self.normalize(records)

    def normalize(self, records):
        clean = []
        for r in records:
            if not r.get("property_address") or not r.get("surplus_amount"):
                continue
            clean.append({
                "county": self.county_name,
                "state": self.state,
                "property_address": str(r.get("property_address", "")).strip(),
                "owner_name": str(r.get("owner_name", "")).strip() or None,
                "parcel_id": str(r.get("parcel_id", "")).strip() or None,
                "sale_date": r.get("sale_date") or None,
                "surplus_amount": float(r.get("surplus_amount", 0)),
                "source_url": self.url,
                "data_type": "tax_sale",
                "status": "active"
            })
        return clean
