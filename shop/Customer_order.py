class customer_order:
    def __init__(self, customer_id, order_id, order_quantity):
        self.__customer_id = customer_id
        self.__order_id = order_id
        self.__order_quantity = order_quantity

    def set_customer_id(self, customer_id):
        self.__customer_id = customer_id
    def set_order_id(self, order_id):
        self.__order_id = order_id
    def set_order_quantity(self, order_quantity):
        self.__order_quantity = order_quantity

    def get_customer_id(self):
        return self.__customer_id
    def get_order_id(self):
        return self.__order_id
    def get_order_quantity(self):
        return self.__order_quantity



