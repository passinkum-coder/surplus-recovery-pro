from bs4 import BeautifulSoup
from processors.pdf_processor import parse_amount, parse_date
import logging

logger = logging.getLogger(__name__)

def extract_table(html_content, county_name):
    """Extract surplus fund records from HTML tables."""
    soup = BeautifulSoup(html_content, "html.parser")
    tables = soup.find_all("table")
    records = []

    for table in tables:
        rows = table.find_all("tr")
        if len(rows) < 2:
            continue

        headers = []
        header_row = rows[0]
        for th in header_row.find_all(["th", "td"]):
            headers.append(th.get_text(strip=True).lower())

        col_map = detect_columns(headers)
        if not col_map:
            continue

        for row in rows[1:]:
            cells = [td.get_text(strip=True) for td in row.find_all(["td", "th"])]
            if len(cells) < 2:
                continue

            record = {}
            for field, idx in col_map.items():
                if idx < len(cells):
                    record[field] = cells[idx]

            if "surplus_amount" in record:
                record["surplus_amount"] = parse_amount(record["surplus_amount"])

            if "sale_date" in record:
                record["sale_date"] = parse_date(record["sale_date"])

            records.append(record)

    logger.info(f"Extracted {len(records)} records from HTML table")
    return records

def detect_columns(headers):
    """Map column headers to field names."""
    col_map = {}
    for i, h in enumerate(headers):
        if any(k in h for k in ["address", "property", "location"]):
            col_map["property_address"] = i
        elif any(k in h for k in ["owner", "name", "taxpayer"]):
            col_map["owner_name"] = i
        elif any(k in h for k in ["surplus", "amount", "excess", "funds", "balance"]):
            col_map["surplus_amount"] = i
        elif any(k in h for k in ["parcel", "account", "id", "folio"]):
            col_map["parcel_id"] = i
        elif any(k in h for k in ["date", "sale"]):
            col_map["sale_date"] = i

    if "property_address" in col_map and "surplus_amount" in col_map:
        return col_map
    return None
