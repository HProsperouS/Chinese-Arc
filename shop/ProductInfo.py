# Classes, Objects & Methods
from Date import fakeinheritence
class ProductInfo(fakeinheritence):
    def __init__(self,product_image,product_name,product_category,
                 product_price,product_description,product_stock,create_date,create_by,modified_date,modified_by): # who create product!!!
        fakeinheritence.__init__(self,create_date,create_by,modified_date,modified_by)
        self.__product_id = 0
        self.__product_image = product_image
        self.__product_name = product_name
        self.__product_category = product_category
        self.__product_price = product_price
        self.__product_description = product_description
        self.__product_stock = product_stock
        self.__status = None

    def set_product_id(self,product_id):
        self.__product_id = product_id

    def set_product_image(self,product_image):
        self.__product_image = product_image

    def set_product_name(self,product_name):
        self.__product_name = product_name

    def set_product_category(self,product_category):
        self.__product_category = product_category

    def set_product_price(self,product_price):
        self.__product_price = product_price

    def set_product_description(self,product_description):
        self.__product_description = product_description

    def set_product_stock(self,product_stock):
        self.__product_stock = product_stock

    def set_status(self, status):
        self.__status = status

    def get_product_id(self):
        return self.__product_id

    def get_product_image(self):
        return self.__product_image

    def get_product_name(self):
        return self.__product_name

    def get_product_category(self):
        return self.__product_category

    def get_product_price(self):
        return self.__product_price

    def get_product_description(self):
        return self.__product_description

    def get_product_stock(self):
        return self.__product_stock

    def get_status(self):
        if self.__product_stock >= 20:
            self.__status = 'Sufficient'
        elif self.__product_stock < 20:
            self.__status = 'Low Stock'
        elif self.__product_stock == 0:
            self.__status = 'Out Of Stock'
        return self.__status
