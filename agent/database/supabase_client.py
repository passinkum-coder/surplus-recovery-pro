
from supabase import create_client
import os
from dotenv import load_dotenv
import logging

load_dotenv()
logger = logging.getLogger(__name__)

def get_client():
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_SERVICE_KEY")
    if not url or not key:
        raise ValueError("Missing SUPABASE_URL or SUPABASE_SERVICE_KEY in environment")
    return create_client(url, key)

def upsert_records(records):
    if not records:
        logger.info("No records to insert.")
        return 0

    supabase = get_client()

    try:
        result = supabase.table("surplus_funds").upsert(
            records,
            on_conflict="county,property_address,sale_date"
        ).execute()
        logger.info(f"Upserted {len(records)} records successfully.")
        return len(records)
    except Exception as e:
        logger.error(f"Supabase upsert error: {e}")
        raise

def get_record_count(county=None):
    """Utility to check how many records exist."""
    supabase = get_client()
    query = supabase.table("surplus_funds").select("id", count="exact")
    if county:
        query = query.eq("county", county)
    result = query.execute()
    return result.count
