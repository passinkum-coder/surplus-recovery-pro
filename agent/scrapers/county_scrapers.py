from scrapers.universal_scraper import UniversalScraper


def load_scrapers():
    """
    SINGLE SOURCE OF TRUTH
    - prevents duplicates
    - guarantees one scraper per county
    - no external registry conflicts
    """

    COUNTY_SOURCES = [
        ("Miami-Dade", "FL", "https://www.miamidade.gov/Apps/PA/PAClaims/Home/UnclaimedProperty"),
        ("Broward", "FL", "PUT_BROWARD_URL_HERE"),
        ("Palm Beach", "FL", "PUT_PALM_BEACH_URL_HERE"),
        ("Hillsborough", "FL", "PUT_HILLSBOROUGH_URL_HERE"),
        ("Orange", "FL", "PUT_ORANGE_URL_HERE"),

        ("Fulton", "GA", "PUT_FULTON_URL_HERE"),
        ("Cobb", "GA", "PUT_COBB_URL_HERE"),
        ("Cherokee", "GA", "PUT_CHEROKEE_URL_HERE"),

        ("Harris", "TX", "PUT_HARRIS_URL_HERE"),
        ("Dallas", "TX", "PUT_DALLAS_URL_HERE"),
    ]

    scrapers = []

    seen = set()  # 🔥 HARD GUARANTEE AGAINST DUPLICATES

    for county, state, url in COUNTY_SOURCES:

        key = f"{county}-{state}"

        if key in seen:
            continue  # prevents duplicates safely

        seen.add(key)

        scrapers.append(
            UniversalScraper(
                county_name=county,
                state=state,
                url=url
            )
        )

    return scrapers
