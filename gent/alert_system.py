from database.supabase_client import get_client
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

ALERT_THRESHOLD = 10000  # Alert when surplus >= $10,000


def check_and_create_alerts(records):
    """
    Check records for high value surplus and create alerts.
    Called after inserting records into surplus_funds table.
    """
    if not records:
        return

    high_value = [r for r in records if r.get("surplus_amount", 0) >= ALERT_THRESHOLD]

    if not high_value:
        return

    supabase = get_client()

    alerts = []
    for r in high_value:
        logger.info(f"HIGH SURPLUS FOUND: {r['county']} - {r['property_address']} - ${r['surplus_amount']:,.2f}")
        alerts.append({
            "state": r.get("state", "Unknown"),
            "county": r.get("county", "Unknown"),
            "property_address": r.get("property_address", ""),
            "surplus_amount": r.get("surplus_amount", 0),
            "source_url": r.get("source_url", ""),
            "status": "unread",
            "created_at": datetime.utcnow().isoformat()
        })

    try:
        supabase.table("alerts").insert(alerts).execute()
        logger.info(f"Created {len(alerts)} high-value alerts")
    except Exception as e:
        logger.error(f"Failed to create alerts: {e}")
