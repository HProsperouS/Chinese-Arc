from dis import dis
import Customer
import webbrowser
from Date import fakeinheritence
from uuid import uuid4

class CustOrder(Customer.Customer,fakeinheritence):
    count_id = 0



    def __init__(self, first_name, last_name, email, holder_name, card_type, card_num, cvv, city, postal_code, unit_number, create_date, modified_date, modified_by,status,total,discount ):
        super().__init__(first_name, last_name,"", "", city, postal_code,"", "", email)
        fakeinheritence.__init__(self,create_date,"", modified_date,modified_by)

        self.__custOrder_id = uuid4()  
        self.__holder_name = holder_name
        self.__card_type = card_type
        self.__card_num = card_num
        self.__cvv =cvv
        self.__city = city
        self.__postal_code = postal_code
        self.__unit_number = unit_number
        self.__status = status
        self.__total = total
        self.__discount = discount
  

    def get_custOrder_id(self):
        return self.__custOrder_id

    def get_holder_name(self):
            return self.__holder_name

    def get_card_type(self):
        return self.__card_type
    
    def get_card_num(self):
        return self.__card_num

    def get_cvv(self):
        return self.__cvv

    def get_city(self):
        return self.__city

    def get_postal_code(self):
        return self.__postal_code
    
    def get_unit_number(self):
        return self.__unit_number

    def get_total(self):
        return self.__total
    
    def get_discount(self):
        return self.__discount

    def get_status(self):
        
        return self.__status

    

    def set_holder_name(self,holder_name):
        self.__holder_name = holder_name

    def set_card_type(self, card_type):
        self.__card_type = card_type

    def set_card_num(self,card_num):
        self.__card_num = card_num

    def set_cvv(self, cvv):
        self.__cvv = cvv

    def set_city(self, city):
        self.__city = city

    def set_postal_code(self,postal_code):
        self.__postal_code = postal_code

    def set_unit_number(self, unit):
        self.__unit_number = unit
    
    def set_status(self, status):
        self.__status = status

    def set_total(self, total):
        self.__total = total
    
    def set_discount(self, discount):
        self.__discount = discount





