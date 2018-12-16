from commons.database import Database
from models.product import Product
from models.web_functions import WebFunctions
from pprint import pprint


class Ulta(object):

    main_url = "https://www.ulta.com"
    sitemap_url = "/ulta/sitemap.jsp"

    database = Database()
    database.initialize()

    webfunctions = WebFunctions()
    session = WebFunctions.get_session()

    def get_category_links(self):
        url = self.main_url + self.sitemap_url
        soup = WebFunctions.make_soup(url=url, session=self.session)
        raw_links = soup.findAll("div", {"class": "secondLevelWrapper"})
        category_links = set()
        for link in raw_links:
            href = link.find("div", {"class": "rootCat"}).find("a")
            if href is not None:
                category_links.add(href.get("href"))
        return category_links

    def save_product(self, product):
        link = product.find("a", {"class": "product"}).get("href")
        image = product.find("img").get("src")
        try:
            site_product_id = link.split("?productId=xlsImpprod")[1]
        except IndexError:
            site_product_id = link.split("productId=")[1]
        brand = product.find("h4", {"class": "prod-title"}).text.strip()
        item_name = product.find("p", {"class": "prod-desc"}).text.strip()
        item_name = item_name.replace("Online Only ", "")
        try:
            price = product.find("span", {"class": "regPrice"})
        except AttributeError:
            price = product.find("span", {"class": "pro-new-price"})
        if price is not None:
            price = WebFunctions.only_digits(price.text)

        product = Product(site_name="ulta",
                          link=link,
                          image=image,
                          site_product_id=site_product_id,
                          brand=brand,
                          item_name=item_name,
                          price=price)
        product.add_product(self.database)

    def get_products(self, page_url):
        url = "https:" + page_url
        soup = WebFunctions.make_soup(url=url, session=self.session)
        try:
            prod_num = int(soup.find("span", {"class": "search-res-number"}).text)
        except AttributeError:
            return
        if prod_num < 96:
            new_url = url
        else:
            breakout = url.split("?")
            if len(breakout) == 2:
                new_url = breakout[0] + "?" + breakout[1] + "&Nrpp={0}".format(prod_num)
            else:
                new_url = breakout[0] + "?Nrpp={0}".format(prod_num)
            soup = WebFunctions.make_soup(url=new_url, session=self.session)
        print(new_url)
        products = soup.find("ul", {"id": "foo16"}).findAll("li")
        for product in products:
            self.save_product(product)


ulta = Ulta()
links = ulta.get_category_links()
# pprint(links)
for link in links:
    ulta.get_products(link)


