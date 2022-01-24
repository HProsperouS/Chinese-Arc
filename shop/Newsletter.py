from uuid import uuid4
from Date import fakeinheritence

class Newsletter(fakeinheritence):
 
    def __init__(self, newsletter_name, message, create_date, create_by):
        super().__init__(create_date, create_by, "", "")
        self.__newsletter_id = uuid4()
        # below are the private attributes
        self.__newsletter_name = newsletter_name
        self.__message = message
   
    def get_newsletter_id(self):
        return self.__newsletter_id
 
    def get_newsletter_name(self):
        return self.__newsletter_name
 
    def get_message(self):
        return self.__message

 
    def set_newsletter_id(self, newsletter_id):
        self.__newsletter_id = newsletter_id
 
    def set_newsletter_name(self, newsletter_name):
        self.__newsletter_name = newsletter_name
 
    def set_message(self, message):
        self.__message = message