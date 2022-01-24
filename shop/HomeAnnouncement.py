from Date import fakeinheritence

class HomeAnnouncement(fakeinheritence):
    count_id = 0
    def __init__(self,title,text,create_date,create_by,modified_date,modified_by):
        super().__init__(create_date,create_by,modified_date,modified_by)
        HomeAnnouncement.count_id += 1
        self.__id = HomeAnnouncement.count_id
        self.__title = title
        self.__text = text

    def set_id(self,id):
        self.__id = id

    def set_title(self,title):
        self.__title = title

    def set_text(self,text):
        self.__text = text

    def get_id(self):
        return self.__id

    def get_title(self):
        return self.__title

    def get_text(self):
        return self.__text