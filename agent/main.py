import os
import importlib
import inspect

from scrapers.base_scraper import BaseScraper
from database.supabase_client import upsert_records


def load_scrapers():
    scrapers = []

    folder = os.path.join(os.path.dirname(__file__), "scrapers")

    for file in os.listdir(folder):
        if file.endswith(".py") and file != "base_scraper.py" and file != "__init__.py":

            module_name = f"scrapers.{file[:-3]}"
            module = importlib.import_module(module_name)

            for name, obj in inspect.getmembers(module, inspect.isclass):
                if issubclass(obj, BaseScraper) and obj is not BaseScraper:
                    scrapers.append(obj())

    return scrapers


scrapers = load_scrapers()

for scraper in scrapers:
    print("Running", scraper.county_name)

    try:
        records = scraper.scrape()

        print("-----")
        print("COUNTY:", scraper.county_name)
        print("RECORDS:", records)
        print("COUNT:", len(records) if records else 0)
        print("-----")

        if records:
            upsert_records(records)

    except Exception as e:
        print("Error:", scraper.county_name, e)
