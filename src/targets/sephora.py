from pprint import pprint
import math
from commons.database import Database
from models.product import Product
from models.web_functions import WebFunctions


class Sephora(object):

    main_url = "https://www.sephora.com"
    departments_url = "/sitemap/departments/"

    database = Database()
    database.initialize()

    webfunctions = WebFunctions()
    session = WebFunctions.get_session()

    @staticmethod
    def only_digits(string):
        string = string.split("-")[0]
        num = float(''.join(i for i in string if any([i.isdigit(), i == "."])))
        return num

    def get_department_links(self):
        url = self.main_url + self.departments_url
        soup = WebFunctions.make_soup(url=url, session=self.session)
        raw_links = soup.find("div", {"class": "Sitemap u-bt u-bw2"}).findAll("h2")
        clean_links = set()
        for i in raw_links:
            clean_links.add(i.find("a").get("href"))
        # pprint(clean_links)
        return clean_links

    def get_category_links(self, page_url):
        url = self.main_url + page_url
        soup = WebFunctions.make_soup(url=url, session=self.session)
        raw_category_links = soup.findAll("a", {"data-at":"top_level_category"})
        clean_category_links = set()
        for i in raw_category_links:
            clean_category_links.add(i.get("href"))
            print(i.get("href"))
        return clean_category_links

    def get_all_category_links(self):
        departments = self.get_department_links()
        all_category_links = set()
        for department in departments:
            category_links = self.get_category_links(page_url=department)
            all_category_links = all_category_links | category_links
        # pprint(all_category_links)
        return all_category_links

    def get_subcategory_links(self, page_url):
        url = self.main_url + page_url
        soup = WebFunctions.make_soup(url=url, session=self.session)
        raw_subcategory_links = soup.findAll("a", {"data-at": "nth_level"})
        if len(raw_subcategory_links) == 0:
            raw_subcategory_links = soup.findAll("a", {"class": "SideNav-link"})
        clean_subcategory_links = set()
        for i in raw_subcategory_links :
            clean_subcategory_links.add(i.get("href"))
            print(i.get("href"))
        return clean_subcategory_links

    def get_all_subcategory_links(self):
        category_links = self.get_all_category_links()
        all_subcategory_links = set()
        count = 0
        for category in category_links:
            count += 1
            subcategory_links = self.get_subcategory_links(category)
            all_subcategory_links = all_subcategory_links | subcategory_links
            print(subcategory_links)
            print(count, len(category_links))
            print("Done {}/{}".format(count, len(category_links)))
        return all_subcategory_links

    @classmethod
    def get_pages(cls, soup):
        try:
            num_str = soup.find("span", {"data-at": "number_of_products"}).text
            num_of_products = cls.only_digits(num_str)
            pages_num = int(math.ceil(num_of_products / 12))
            pages_num += 1
            pages = [int(i) for i in range(1, pages_num)]
            return pages
        except AttributeError:
            return

    def save_product(self, product):
        link = product.find("a").get("href")
        image = product.find("img").get("src")
        site_product_id = product.find("button", {"data-comp": "ProductQuicklook"}).get("data-sku-number")
        brand = product.find("span", {"data-at": "sku_item_brand"}).text
        item_name = product.find("span", {"data-at": "sku_item_name"}).text
        price = sephora.only_digits(product.find("span", {"data-at": "sku_item_price_list"}).text)
        product = Product(site_name="sephora",
                          link=link,
                          image=image,
                          site_product_id=site_product_id,
                          brand=brand,
                          item_name=item_name,
                          price=price)
        product.add_product(self.database)

    def get_products(self, page_url):
        main_url = self.main_url + page_url
        print(page_url)
        soup = WebFunctions.make_soup(url=main_url, session=self.session)
        pages = self.get_pages(soup)
        if pages is None:
            return
        for page in pages:
            url = main_url + "?pageSize=12" + "&currentPage={}".format(page)
            print(url)
            soup = WebFunctions.make_soup(url=url, session=self.session)
            products = soup.findAll("div", {"class": "css-12egk0t"})
            for product in products:
                self.save_product(product)
