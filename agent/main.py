import os
import importlib
import inspect

from scrapers.base_scraper import BaseScraper

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

# STEP 2: RUN LOOP SECOND
for scraper in scrapers:
    print("Running", scraper.county_name)

    try:
        results = scraper.scrape()
        print(results)
    except Exception as e:
        print("Error:", scraper.county_name, e)
