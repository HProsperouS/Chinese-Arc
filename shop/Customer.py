class Customer:
    count_id = 0

    def __init__(self, first_name, last_name,email,gender,birthdate,city,postal_code,address,password):
        Customer.count_id +=1
        self.__customer_id = Customer.count_id
        self.__first_name = first_name
        self.__last_name = last_name
        self.__email = email
        self.__gender = gender
        self.__birthdate = birthdate
        self.__city = city
        self.__postal_code = postal_code
        self.__address = address 
        self.__password = password

    def get_customer_id(self):
        return self.__customer_id

    def get_first_name(self):
        return self.__first_name

    def get_last_name(self):
        return self.__last_name
    
    def get_gender(self):
        return self.__gender

    def get_birthdate(self):
        return self.__birthdate

    def get_city(self):
        return self.__city

    def get_postal_code(self):
        return self.__postal_code

    def get_address(self):
        return self.__address
   
    def get_password(self):
        return self.__password

    def get_email(self):
        return self.__email


    def set_customer_id(self,customer_id):
        self.__customer_id = customer_id

    def set_first_name(self,first_name):
        self.__first_name = first_name

    def set_last_name(self,last_name):
        self.__last_name = last_name

    def set_email(self, email):
        self.__email = email

    def set_gender(self,gender):
        self.__gender = gender

    def set_birthdate(self,birthdate):
        self.__birthdate = birthdate

    def set_city(self,city):
        self.__city = city

    def set_postal_code(self,postal_code):
        self.__postal_code = postal_code

    def set_address(self,address):
        self.__address= address

    def set_password(self,password):
        self.__password = password
