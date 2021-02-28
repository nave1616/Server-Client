import os
from pathlib import Path


class User(object):

    def __init__(self):
        self.root_path = Path(__file__).parent.absolute()  # /User
        self.user_dict = self.root_path / 'Users'  # /login/Users
        self.user_name = None
        self.user_info = []
        self.users = []
        self.admin = None
        self.con = None

    def bool_convert(self, value):
        if value == 'True':
            return True
        else:
            return False

    def get_obj(self):
        return usr(self.user_name, self.admin, self.con)

    def login(self, username, password, conn):
        try_user_name = username
        if os.path.exists(os.path.join(self.user_dict, try_user_name + '.txt')) and try_user_name not in self.users:
            with open(os.path.join(self.user_dict, try_user_name + '.txt'), 'r') as user_file:
                for line in user_file:
                    if 'admin' in line:
                        self.admin = self.bool_convert(
                            line.split(':')[-1].strip('\n'))
                    elif 'password' in line:
                        passw = line.split(':')[-1].strip('\n')
            if passw == password:
                self.user_name = try_user_name
                self.con = conn
                self.users.append(self.user_name)
                return True
            else:
                return False
        else:
            return False

    def register(self, username, password, conn):
        try_user_name = username
        with open(os.path.join(self.user_dict, try_user_name + '.txt'), 'a') as user_file:
            user_file.writelines(password)
            self.user_name = try_user_name
            self.users.append(self.user_name)
            return True

    def exsist(self, username):
        try_user_name = username
        if os.path.isfile(os.path.join(self.user_dict, try_user_name + '.txt')):
            return True
        else:
            return False

    def logged_in(self, username):
        if username in self.users:
            return True
        else:
            return False


class usr():
    def __init__(self, user_name, admin, con):
        self.user_name = user_name
        self.admin = admin
        self.con = con


if __name__ == '__main__':
    Log = User()

__all__ = ['User', 'usr']
