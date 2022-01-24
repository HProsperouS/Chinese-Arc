
class DeliveryFeedback():
    count_id = 0
    def __init__(self, email_address, product, rating, 
                message1, message2, message3,message4, remarks,create_date):
        DeliveryFeedback.count_id += 1
        self.__id = DeliveryFeedback.count_id
        self.__email_address = email_address
        self.__product = product
        self.__rating = rating
        self.__message1 = message1
        self.__message2 = message2
        self.__message3 = message3
        self.__message4 = message4
        self.__remarks = remarks
        self.__create_date = create_date
    
    def set_id(self,id):
        self.__id = id

    def set_email_address(self,email_address):
        self.__email_address = email_address

    def set_product(self, product):
        self.__product = product

    def set_rating(self, rating):
        self.__rating = rating
    
    def set_message1(self, message1):
        self.__message1 = message1

    def set_message2(self, message2):
        self.__message2 = message2  

    def set_message3(self, message3):
        self.__message3 = message3

    def set_message4(self, message4):
        self.__message4 = message4

    def set_remarks(self, remarks):
        self.__remarks = remarks

    def set_create_date(self, create_date):
        self.__create_date = create_date

    def get_id(self):
        return self.__id

    def get_email_address(self):
        return self.__email_address
    
    def get_product(self):
        return self.__product

    def get_rating(self):
        return self.__rating

    def get_message1(self):
        return self.__message1

    def get_message2(self):
        return self.__message2

    def get_message3(self):
        return self.__message3

    def get_message4(self):
        return self.__message4

    def get_remarks(self):
        return self.__remarks

    def get_create_date(self):
        return self.__create_date