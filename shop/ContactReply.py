from uuid import uuid4
from Date import fakeinheritence

class ContactReply(fakeinheritence):
    def __init__(self, subject, recipient, reply, create_by, create_date):
        super().__init__(create_date, create_by, "", "")
        self.__contactReply_id = uuid4()
        self.__subject = subject
        self.__recipient = recipient
        self.__reply = reply
   
    def get_contactReply_id(self):
        return self.__contactReply_id

    def get_subject(self):
        return self.__subject

    def get_recipient(self):
        return self.__recipient

    def get_reply(self):
        return self.__reply
 
 
    def set_contactReply_id(self, contactReply_id):
        self.__contactReply_id = contactReply_id

    def set_subject(self, subject):
        self.__subject = subject
    
    def set_recipient(self, recipient):
        self.__recipient = recipient

    def set_reply(self, reply):
        self.__reply = reply