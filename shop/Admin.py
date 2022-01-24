class Admin:
    count_id = 0

    def __init__(self, user_name,first_name, last_name,gender,email,password,roles):
        Admin.count_id +=1
        self.admin_id = Admin.count_id
        self.user_name = user_name
        self.first_name = first_name
        self.last_name = last_name
        self.gender = gender
        self.email = email
        self.password = password
        self.roles = roles

    def get_admin_id(self):
        return self.admin_id

    def get_user_name(self):
        return self.user_name

    def get_first_name(self):
        return self.first_name

    def get_last_name(self):
        return self.last_name

    def get_gender(self):
        return self.gender

    def get_email(self):
        return self.email

    def get_password(self):
        return self.password

    def get_roles(self):
        return self.roles

    def set_admin_id(self,admin_id):
        self.admin_id = admin_id

    def set_user_name(self,user_name):
        self.user_name = user_name

    def set_first_name(self,first_name):
        self.first_name = first_name

    def set_last_name(self,last_name):
        self.last_name = last_name

    def set_gender(self,gender):
        self.gender = gender

    def set_email(self, email):
        self.email = email

    def set_password(self,password):
        self.password = password

    def set_password(self,roles):
        self.roles = roles
