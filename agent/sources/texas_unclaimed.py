import os

try:
    from supabase import create_client
except ImportError:
    raise Exception("Supabase library not installed. Run pip install supabase")


class SupabaseDB:

    def __init__(self):

        self.url = os.getenv("SUPABASE_URL")
        self.key = os.getenv("SUPABASE_KEY")

        if not self.url or not self.key:
            raise Exception("Missing SUPABASE_URL or SUPABASE_KEY")

        self.client = create_client(self.url, self.key)

        print("🟢 Supabase connected")

    def upsert_records(self, table_name, records):

        if not records:
            print("⚠️ No records to insert")
            return

        cleaned_records = [
            r for r in records
            if isinstance(r, dict) and "property_id" in r
        ]

        print(f"📦 Attempting insert into {table_name}")
        print(f"📊 Records count: {len(cleaned_records)}")

        if not cleaned_records:
            print("⚠️ No valid records after cleaning")
            return

        try:
            response = (
                self.client
                .table(table_name)
                .upsert(cleaned_records, on_conflict="property_id")
                .execute()
            )

            print(f"💾 Upserted {len(cleaned_records)} records into {table_name}")

            return response

        except Exception as e:
            print(f"❌ Supabase insert failed: {e}")
            return None
