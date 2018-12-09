import uuid



class Product(object):
    def __init__(self, site_name, link, image, site_product_id, brand, item_name, price, _id=None):
        self.site_name = site_name
        self.link = link
        self.image = image
        self.site_product_id = site_product_id
        self.brand = brand
        self.item_name = item_name
        self.price = price
        self._id = uuid.uuid4().hex if _id is None else _id

    def add_product(self, database):
        database.insert("{}".format(self.site_name), self.json())
        print("Product added")

    def json(self):
        return {
            "site_name": self.site_name,
            "link": self.link,
            "image": self.image,
            "site_product_id": self.site_product_id,
            "brand": self.brand,
            "item_name": self.item_name,
            "price": self.price,
            "_id": self._id}

