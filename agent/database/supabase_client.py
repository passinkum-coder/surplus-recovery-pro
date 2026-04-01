from supabase import create_client
import os


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

        try:
            response = (
                self.client
                .table(table_name)
                .upsert(records, on_conflict="property_id")
                .execute()
            )

            print(f"💾 Upserted {len(records)} records into {table_name}")

            return response

        except Exception as e:
            print(f"❌ Supabase insert failed: {e}")
            return None
