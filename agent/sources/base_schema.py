class BaseSchema:

    @staticmethod
    def normalize(record, state):

        return {
            "property_id": record.get("property_id", ""),
            "owner_name": record.get("owner_name", ""),
            "address": record.get("address", ""),
            "city": record.get("city", ""),
            "state": state.upper(),
            "zip": record.get("zip", ""),
            "county": record.get("county", ""),
            "amount": float(record.get("amount", 0) or 0),
            "property_type": record.get("property_type", ""),
            "year_reported": int(record.get("year_reported", 0) or 0)
        }
