import pdfplumber
import requests
import re
import logging

logger = logging.getLogger(__name__)

def parse_amount(value):
    """Convert a string like '$1,234.56' to float 1234.56"""
    if not value:
        return None
    cleaned = re.sub(r'[^\d.]', '', str(value))
    try:
        amount = float(cleaned)
        return amount if amount > 0 else None
    except:
        return None

def parse_date(value):
    """Try to parse a date string into YYYY-MM-DD format."""
    if not value:
        return None
    from dateutil import parser as dateparser
    try:
        return dateparser.parse(str(value)).strftime("%Y-%m-%d")
    except:
        return None

def extract_pdf(url, county_name):
    """Download and extract surplus records from a PDF."""
    logger.info(f"Downloading PDF from {url}")
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
    except Exception as e:
        logger.error(f"Failed to download PDF: {e}")
        return []

    pdf_path = f"/tmp/{county_name.lower()}_surplus.pdf"
    with open(pdf_path, "wb") as f:
        f.write(response.content)

    records = []
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                tables = page.extract_tables()
                for table in tables:
                    for row in table:
                        if not row:
                            continue
                        row_text = " ".join(str(c) for c in row if c).lower()
                        if any(h in row_text for h in ["address", "owner", "amount", "parcel"]):
                            continue
                        record = extract_row_fields(row)
                        if record:
                            records.append(record)
    except Exception as e:
        logger.error(f"PDF parse error: {e}")

    logger.info(f"Extracted {len(records)} records from PDF")
    return records

def extract_row_fields(row):
    """
    Attempt to extract fields from a table row.
    Columns vary by county — we detect amounts by looking for dollar values.
    """
    row = [str(c).strip() if c else "" for c in row]
    if len(row) < 2:
        return None

    amount = None
    amount_idx = -1
    for i, cell in enumerate(row):
        parsed = parse_amount(cell)
        if parsed and parsed > 10:
            amount = parsed
            amount_idx = i
            break

    if not amount:
        return None

    candidates = [c for c in row[:amount_idx] if c]
    property_address = candidates[0] if len(candidates) > 0 else None
    owner_name = candidates[1] if len(candidates) > 1 else None

    return {
        "property_address": property_address,
        "owner_name": owner_name,
        "surplus_amount": amount
    }
