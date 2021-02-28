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
        self.ip = None

    def bool_convert(self, value):
        if value == 'True':
            return True
        else:
            return False

    def get_obj(self):
        return usr(self.user_name, self.admin, self.con)

    def login(self, username, password, conn, adder):
        if self.exsist(username):
            passw, admin = self.read_user_file(username)
            if passw == password:
                self.update_user_ip(username, adder)
                self.user_name = username
                self.con = conn
                self.ip = adder
                self.admin = admin
                self.users.append(self.user_name)
                return True
            else:
                return False
        else:
            return False

    def register(self, username, password, conn, adder):
        if not self.exsist(username):
            with open(os.path.join(self.user_dict, username + '.txt'), 'a') as user_file:
                user_file.write('password:' + str(password) +
                                '\nadmin:False\nip:' + str(adder[0]))
                self.user_name = username
                self.ip = adder
                self.admin = False
                self.users.append(self.user_name)
                return True
        else:
            return False

    def read_user_file(self, username):
        with open(os.path.join(self.user_dict, username + '.txt'), 'r') as user_file:
            for line in user_file:
                if 'admin' in line:
                    admin = self.bool_convert(
                        line.split(':')[-1].strip('\n'))
                elif 'password' in line:
                    passw = line.split(':')[-1].strip('\n')
        return (passw, admin)

    def update_user_ip(self, username, adder):
        password, admin = self.read_user_file(username)
        with open(os.path.join(self.user_dict, username + '.txt'), 'w') as user_file:
            user_file.write('password:' + str(password) +
                            '\nadmin:' + str(admin) + '\nip:' + str(adder[0]))

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
