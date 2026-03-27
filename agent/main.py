from scrapers.county_scrapers import FultonScraper

scraper = FultonScraper()

print("Running Fulton scraper...")

try:
    results = scraper.scrape()
    print(results)
except Exception as e:
    print("Error:", e)
