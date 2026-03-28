from scrapers.county_scrapers import (
    FultonScraper,
    GwinnettScraper,
    CobbScraper,
    DeKalbScraper,
    CherokeeScraper,
    ClaytonScraper,
    HenryScraper,
    ForsythScraper,
    HallScraper,
    RichmondScraper,

 )

# STEP 1: CREATE LIST FIRST (IMPORTANT)
scrapers = [
    FultonScraper(),
    GwinnettScraper(),
    CobbScraper(),
    DeKalbScraper(),
    CherokeeScraper(),
    ClaytonScraper(),
    HenryScraper(),
    ForsythScraper(),
    HallScraper(),
    RichmondScraper()

    ]

# STEP 2: RUN LOOP SECOND
for scraper in scrapers:
    print("Running", scraper.county_name)

    try:
        results = scraper.scrape()
        print(results)
    except Exception as e:
        print("Error:", scraper.county_name, e)
