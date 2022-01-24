class fakeinheritence:
    def __init__(self,create_date,create_by,modified_date,modified_by):
        self.__create_date = create_date
        self.__create_by = create_by
        self.__modified_date = modified_date
        self.__modified_by = modified_by

    def set_create_date(self,create_date):
        self.__create_date = create_date

    def set_create_by(self,create_by):
        self.__create_by = create_by

    def set_modified_date(self,modified_date):
        self.__modified_date = modified_date

    def set_modified_by(self,modified_by):
        self.__modified_by = modified_by

    def get_create_date(self):
        return self.__create_date
        
    def get_create_by(self):
        return self.__create_by

    def get_modified_date(self):
        return self.__modified_date

    def get_modified_by(self):
        return self.__modified_by

    