from targets.sephora import Sephora
from pprint import pprint
import time


def scrape_sephora():
    t1 = time.time()
    sephora = Sephora()
    subcategories = sephora.get_all_subcategory_links()
    pprint(subcategories)
    for subcategory in subcategories:
        sephora.get_products(subcategory)
    t2 = time.time()
    print("This took  {} seconds".format(t2-t1))

scrape_sephora()
