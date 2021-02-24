import os


def file_handeler(conn, usr, path, command):
    chunk = ''
    file_name = path.split('/')[-1]
    file_buffer = conn.recv(1024).decode('utf-8')
    try:
        file_buffer = int(file_buffer)
    except ValueError:
        pass
    file_size = file_buffer * 1024**2
    while 1024 < file_buffer:
        file_buffer = file_buffer - 1024
        chunk += conn.recv(1024).decode('utf-8')
    chunk += conn.recv(file_buffer).decode('utf-8')
    with open(os.path.join(path, file_name), 'wb') as file_writer:
        file_writer.write(chunk)
    msg = 'Server File recv\nSender: ' + usr.name + \
        '\n File name: ' + file_name + '\nSize is:' + file_size
    return msg


def commands(conn, usr, command):
    action = command.split(' ')[-1]
    root_path = 'Server/Files'
    if '!file' in command:
        msg = file_handeler(conn, usr, root_path, action)
        return msg


class Login():

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

    def has_admin(self, user_name):
        return self.user_info[1].split(':')[-1].strip('\n')

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
    Log = Login()
