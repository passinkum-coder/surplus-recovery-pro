from scrapers.county_scrapers import (
    FultonScraper,
    GwinnettScraper,
    CobbScraper,
    DeKalbScraper,
    CherokeeScraper,
    ClaytonScraper
)


sscrapers = [
    FultonScraper(),
    GwinnettScraper(),
    CobbScraper(),
    DeKalbScraper(),
    CherokeeScraper(),
    ClaytonScraper()
]

for scraper in scrapers:
    print("Running", scraper.county_name)

    try:
        results = scraper.scrape()
        print(results)
    except Exception as e:
        print("Error:", scraper.county_name, e)
