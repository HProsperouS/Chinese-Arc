from uuid import uuid4

class Subscriptions:
 
    def __init__(self, first_name, last_name, email):
        self.__subscriptions_id = uuid4()
        # below are the private attributes
        self.__first_name = first_name
        self.__last_name = last_name
        self.__email = email
   
    def get_subscriptions_id(self):
        return self.__subscriptions_id
 
    def get_first_name(self):
        return self.__first_name
 
    def get_last_name(self):
        return self.__last_name
 
    def get_email(self):
        return self.__email
 
 
    def set_subscriptions_id(self, subscriptions_id):
        self.__subscriptions_id = subscriptions_id
 
    def set_first_name(self, first_name):
        self.__first_name = first_name
 
    def set_last_name(self, last_name):
        self.__last_name = last_name
 
    def set_email(self, email):
        self.__email = email
