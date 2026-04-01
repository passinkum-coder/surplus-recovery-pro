from agent.sources.base_schema import BaseSchema

class StateAdapter:

    @staticmethod
    def normalize_list(raw_list, state_code):

        normalized = []

        for r in raw_list:

            try:
                normalized.append(
                    BaseSchema.normalize(r, state_code)
                )
            except Exception as e:
                print(f"⚠️ Skipped bad record in {state_code}: {e}")

        return normalized
