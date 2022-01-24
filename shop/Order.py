from Date import fakeinheritence

class fake(fakeinheritence):
    def __init__(self, name,email, total, status,create_date):
        super().__init__(create_date)
        self.__email = email
        self.__name = name
        self.__total = total
        self.__status = status
        self.__date = create_date
        
   

    def get_name(self):
        return self.__name

    def get_email(self):
        return self.__email

    def get_total(self):
        return self.__total

    def get_status(self):
        return self.__status

    def get_date(self):
        return self.__date

    

    def set_name(self, name):
        self.__name = name

    def set_email(self, email):
        self.__email = email

    def set_total(self, total):
        self.__total = total

    def set_status(self,status):
        self.__status = status

    def set_date(self,date):
        self.__date = date




class Order(fake):
    count_id = 0

    def __init__(self, name,email, total, status,create_date):
        super().__init__(name,email, total, status,create_date)
        Order.count_id += 1
        self.__order_id = Order.count_id
       
        
    def get_order_id(self):
        return self.__order_id


    def set_order_id(self, order_id):
        self.__order_id = order_id


