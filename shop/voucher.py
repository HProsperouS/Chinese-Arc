from calendar import c
from Date import fakeinheritence
import random
class Voucher(fakeinheritence):
    count_id = 0
    
    def __init__(self, voucher_name,voucher_desc,voucher_type,voucher_secret,voucher_code, voucher_limit, voucher_status,voucher_date,voucher_end_date,create_date,create_by,modified_date,modified_by):
        super().__init__(create_date,create_by,modified_date,modified_by)
        Voucher.count_id += 1
        self.__voucher_id = Voucher.count_id
        self.__voucher_name = voucher_name
        self.__voucher_desc = voucher_desc
        self.__voucher_type = voucher_type
        self.__voucher_secret = voucher_secret
        self.__voucher_code = voucher_code
        self.__voucher_limit = voucher_limit
        self.__voucher_status = voucher_status
        self.__voucher_date = voucher_date
        self.__voucher_end_date = voucher_end_date
        

        
        
    def get_voucher_id(self):
        return self.__voucher_id
    
    def get_voucher_name(self):

        return self.__voucher_name
    def get_voucher_secret(self):
        return self.__voucher_secret
    def get_voucher_code(self):
     
        return self.__voucher_code

    def get_voucher_desc(self):
        return self.__voucher_desc

    def get_voucher_type(self):
        return self.__voucher_type

    def get_voucher_total(self):
        return self.__voucher_limit

    def get_voucher_status(self):
        return self.__voucher_status

    def get_voucher_date(self):
        return self.__voucher_date
    def get_voucher_end_date(self):
        return self.__voucher_end_date

    

    def set_voucher_id(self, order_id):
        self.__voucher_id = order_id

    def set_name(self, voucher_name):
        self.__voucher_name = voucher_name

    def set_desc(self, desc):
        self.__voucher_desc = desc

    def set_type(self, voucher_type):
        self.__voucher_type = voucher_type

    def set_code(self,code):
        self.__voucher_code = code

    def set_secret(self,secret):
        self.__voucher_secret = secret
        
    def set_total(self, voucher_limit):
        self.__voucher_limit = voucher_limit

    def set_status(self,voucher_status):
        self.__voucher_status = voucher_status

    def set_date(self,voucher_date):
        self.__voucher_date = voucher_date

    def set_end_date(self,voucher_end_date):
        self.__voucher_end_date = voucher_end_date

    

