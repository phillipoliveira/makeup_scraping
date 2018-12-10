from targets.sephora import Sephora
from pprint import pprint


def scrape_sephora():
    sephora = Sephora()
    subcategories = sephora.get_all_subcategory_links()
    pprint(subcategories)
    for subcategory in subcategories:
        sephora.get_products(subcategory)

scrape_sephora()