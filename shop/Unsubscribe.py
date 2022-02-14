from re import sub
from uuid import uuid4

class Unsubscribe:
 
    def __init__(self, sub_id, email, reason):
        self.__unsubscribe_id = uuid4()
        # below are the private attributes
        self.__sub_id = sub_id
        self.__email = email
        self.__reason = reason
   
    def get_unsubscribe_id(self):
        return self.__unsubscribe_id

    def get_sub_id(self):
        return self.__sub_id
 
    def get_email(self):
        return self.__email

    def get_reason(self):
        return self.__reason
 
 
    def set_unsubscribe_id(self, unsubscribe_id):
        self.__unsubscribe_id = unsubscribe_id

    def set_sub_id(self, sub_id):
        self.__sub_id = sub_id
 
    def set_email(self, email):
        self.__email = email

    def set_reason(self, reason):
        self.__reason = reason