from uuid import uuid4
from Date import fakeinheritence
from uuid import uuid4

class FAQ(fakeinheritence):
    count_id = 0
    def __init__(self,question,answer, create_date):
        super().__init__(create_date,"", "", "")
        FAQ.count_id += 1
        self.__id = uuid4()
        self.__count_id = FAQ.count_id
        self.__question = question
        self.__answer = answer

    def set_id(self,id):
        self.__id = id
    
    def set_count_id(self,count_id):
        self.__count_id = count_id

    def set_question(self,question):
        self.__question = question

    def set_answer(self,answer):
        self.__answer = answer

    def get_id(self):
        return self.__id

    def get_question(self):
        return self.__question

    def get_answer(self):
        return self.__answer    

    def get_count_id(self):
        return self.__count_id    