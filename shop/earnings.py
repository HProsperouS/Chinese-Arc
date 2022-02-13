class Revenue:

    def __init__(self, earnings):
        self.__earnings = earnings

    def get_total_earnings(self):
        self.__earnings += self.__earnings
        return self.__earnings

   


    def set_total_earnings(self,earnings):
       self.__earnings = earnings
 

    