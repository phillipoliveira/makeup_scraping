from targets.sephora import Sephora
from targets.ulta import Ulta
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
    print("This took  {0} seconds".format(t2-t1))


def scrape_ulta():
    t1 = time.time()
    ulta = Ulta()
    links = ulta.get_category_links()
    # pprint(links)
    for link in links:
        ulta.get_products(link)
    t2 = time.time()
    print("This took  {0} seconds".format(t2-t1))


scrape_ulta()
scrape_sephora()
