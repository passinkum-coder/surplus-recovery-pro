from scrapers.base_scraper import BaseScraper
from processors.pdf_processor import extract_pdf
from processors.table_processor import extract_table
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__)


class MiamiDadeScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            county_name="Miami-Dade",
            url="https://www.miamidade.gov/taxcollector/tax-deed-surplus.asp"
        )
        self.state = "Florida"

    def scrape(self):
        content = self.get_page()
        soup = BeautifulSoup(content, "html.parser")
        pdf_link = soup.find("a", href=lambda h: h and h.lower().endswith(".pdf"))
        if pdf_link:
            pdf_url = pdf_link["href"]
            if not pdf_url.startswith("http"):
                pdf_url = "https://www.miamidade.gov" + pdf_url
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


class BrowardScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            county_name="Broward",
            url="https://www.broward.org/RecordsTaxesTreasury/TaxDeeds/Pages/SurplusFunds.aspx"
        )
        self.state = "Florida"

    def scrape(self):
        content = self.get_page()
        soup = BeautifulSoup(content, "html.parser")
        pdf_link = soup.find("a", href=lambda h: h and h.lower().endswith(".pdf"))
        if pdf_link:
            pdf_url = pdf_link["href"]
            if not pdf_url.startswith("http"):
                pdf_url = "https://www.broward.org" + pdf_url
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


class PalmBeachScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            county_name="Palm Beach",
            url="https://www.pbctax.com/tax-deed-surplus-funds/"
        )
        self.state = "Florida"

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


class HillsboroughScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            county_name="Hillsborough",
            url="https://www.hillstax.org/tax-deed/surplus-funds/"
        )
        self.state = "Florida"

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


class OrangeCountyFLScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            county_name="Orange",
            url="https://www.octaxcol.com/tax-deed-surplus/"
        )
        self.state = "Florida"

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
