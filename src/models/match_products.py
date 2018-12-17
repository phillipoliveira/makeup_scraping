from commons.database import Database
from models.product import Product
from pprint import pprint
import jellyfish
import re, string


class MatchProducts(object):

    database = Database()
    database.initialize()

    def get_products_by_site(self, site_name):
        products = Product.get_products(database=self.database,
                                        collection=site_name,
                                        query={'site_name': '{0}'.format(site_name)})
        return products

    @staticmethod
    def clean_names(text):
        text = re.sub('[^a-zA-Z0-9]', '', text).lower().replace("\n", "")
        return text

    def check_matches(self, ulta, sephora):
        ulta = self.clean_names(ulta['name'])
        sephora = self.clean_names(sephora['name'])
        result = jellyfish.jaro_distance(ulta, sephora)
        return result

    def format_names(self, site_name):
        clean_products = list()
        products = self.get_products_by_site(site_name=site_name)
        for product in products:
            brand = self.clean_names(product.brand)
            brand = brand.replace(" cosmetics", "")
            item_name = self.clean_names(product.item_name)
            name = brand + " " + item_name
            clean_products.append({"name": name, "image": product.image, "link": product.link, "price": product.price})
        return clean_products

    def get_matches(self):
        sephora = self.format_names("sephora")
        ulta = self.format_names("ulta")
        for u_product in ulta:
            for s_product in sephora:
                if self.check_matches(s_product, u_product) > 0.95:
                    print("Match! {0}, {1}".format(s_product, u_product))
                    self.database.insert("matches", data=({"sephora": s_product, "ulta": u_product}))


