from Date import fakeinheritence
from uuid import uuid4

class Feedback(fakeinheritence):

    def __init__(self, product_name, title, rating, fit, quality, description, create_by, create_date):
        super().__init__(create_date, create_by, "", "")
        self.__feedback_id = uuid4()
        self.__product_name = product_name
        self.__rating = rating
        self.__title = title
        self.__description = description
        self.__fit = fit
        self.__quality = quality

    def set_feedback_id(self, feedback_id):
        self.__feedback_id = feedback_id

    def set_product_name(self, product_name):
        self.__product_name = product_name

    def set_rating(self, rating):
        self.__rating = rating

    def set_title(self, title):
        self.__title = title

    def set_description(self, description):
        self.__description = description

    def set_fit(self, fit):
        self.__fit = fit

    def set_quality(self, quality):
        self.__quality = quality



    def get_feedback_id(self):
        return self.__feedback_id

    def get_product_name(self):
        return self.__product_name

    def get_rating(self):
        return self.__rating

    def get_title(self):
        return self.__title 

    def get_description(self):
        return self.__description

    def get_fit(self):
        return self.__fit

    def get_quality(self):
        return self.__quality