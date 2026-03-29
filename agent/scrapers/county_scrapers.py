from scrapers.universal_scraper import UniversalScraper


def load_scrapers():

    COUNTY_SOURCES = [
        {
            "county": "Miami-Dade",
            "state": "FL",
            "url": "https://www.miamidade.gov/Apps/PA/PAClaims/Home/UnclaimedProperty"
        },

        {
            "county": "Broward",
            "state": "FL",
            "url": "PUT_BROWARD_URL_HERE"
        },

        {
            "county": "Palm Beach",
            "state": "FL",
            "url": "PUT_PALM_BEACH_URL_HERE"
        },

        {
            "county": "Hillsborough",
            "state": "FL",
            "url": "PUT_HILLSBOROUGH_URL_HERE"
        },

        {
            "county": "Orange",
            "state": "FL",
            "url": "PUT_ORANGE_FL_URL_HERE"
        },

        {
            "county": "Cherokee",
            "state": "GA",
            "url": "PUT_CHEROKEE_GA_URL_HERE"
        },

        {
            "county": "Fulton",
            "state": "GA",
            "url": "PUT_FULTON_GA_URL_HERE"
        },

        {
            "county": "Cobb",
            "state": "GA",
            "url": "PUT_COBB_GA_URL_HERE"
        },

        {
            "county": "Dallas",
            "state": "TX",
            "url": "PUT_DALLAS_TX_URL_HERE"
        },

        {
            "county": "Harris",
            "state": "TX",
            "url": "PUT_HARRIS_TX_URL_HERE"
        }
    ]

    scrapers = []

    for county in COUNTY_SOURCES:
        scrapers.append(
            UniversalScraper(
                county_name=county["county"],
                state=county["state"],
                url=county["url"]
            )
        )

    return scrapers
