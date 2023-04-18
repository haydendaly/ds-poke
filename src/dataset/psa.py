from src.scrape.psa import PSAPopScraper


def get_psa_pop_df():
    return PSAPopScraper().get_cards_df()
