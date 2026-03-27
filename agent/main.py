from scrapers.county_scrapers import FultonScraper, GwinnettScraper

scrapers = [
    FultonScraper(),
    GwinnettScraper()
]

print("Running Fulton scraper...")

try:
    results = scraper.scrape()
  for scraper in scrapers:
    print("Running", scraper.county_name)

    try:
        results = scraper.scrape()
        print(results)
    except Exception as e:
        print("Error:", scraper.county_name, e)
