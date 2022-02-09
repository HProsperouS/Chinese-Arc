from uuid import uuid4

class Contact:
    def __init__(self, first_name, last_name, email, subject, message):
        self.__contact_id = uuid4()
        # below are the private attributes
        self.__first_name = first_name
        self.__last_name = last_name
        self.__email = email
        self.__subject = subject
        self.__message = message
   
    def get_contact_id(self):
        return self.__contact_id
 
    def get_first_name(self):
        return self.__first_name
 
    def get_last_name(self):
        return self.__last_name
 
    def get_email(self):
        return self.__email

    def get_subject(self):
        return self.__subject

    def get_message(self):
        return self.__message
 
 
    def set_contact_id(self, contact_id):
        self.__contact_id = contact_id
 
    def set_first_name(self, first_name):
        self.__first_name = first_name
 
    def set_last_name(self, last_name):
        self.__last_name = last_name
 
    def set_email(self, email):
        self.__email = email

    def set_subject(self, subject):
        self.__subject = subject
    
    def set_message(self, message):
        self.__message = message
