import os


class User(object):

    def __init__(self):
        self.root_path = os.path.dirname(
            os.path.abspath(__file__))  # /User
        self.user_dict = os.path.join(
            self.root_path, 'Users')  # /login/User
        self.user_name = None
        self.user_info = []
        self.users = []
        self.admin = None

    def get_obj(self):
        return usr(self.user_name, self.admin)

    def login(self, username, password):
        try_user_name = username
        if os.path.exists(os.path.join(self.user_dict, try_user_name + '.txt')) and try_user_name not in self.users:
            with open(os.path.join(self.user_dict, try_user_name + '.txt'), 'r') as user_file:
                for line in user_file:
                    self.user_info.append(line)
            if self.user_info[0].split(':')[-1].strip('\n') == password:
                self.user_name = try_user_name
                self.users.append(self.user_name)
                self.admin = self.user_info[1].split(':')[-1].strip('\n')
                return True
            else:
                return False
        else:
            return False

    def register(self, username, password):
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
    def __init__(self, user_name, admin):
        self.user_name = user_name
        self.admin = admin


if __name__ == '__main__':
    Log = User()

__all__ = ['User', 'usr']
