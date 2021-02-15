import socket
import os
import sys
import time
import threading


class server():
    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.S_ip = "0.0.0.0"
        self.S_port = 5050
        self.connections = []
        # Pathes
        self.server_dict = os.getcwd()  # /Server
        self.user_dict = os.path.join(
            self.server_dict, 'Users')  # /Server/User
        self.server.bind((self.S_ip, self.S_port))
        self.lock = threading.Lock()
        try:
            self.server.listen()
        except:
            print('error')
        self.client_Accept()

    def path(self, *args, **kwargs):
        path = os.path.join(*args, **kwargs)

        return path

    def client_handler(self, conn, adder, user_name):
        pass

    def user_login(self, conn, adder):
        conn.send(
            '!login [User name] for login\n!register [User name] for registeration')
        run = True
        while run:
            time.sleep(0.1)
            msg = conn.recv(1024).decode('utf-8')
            if '!register' in msg:
                user_name = msg.split(' ')[-1]
                if os.path.exists(self.path(self.user_dict, user_name)):
                    conn.send('User already exsist try another.')
                else:
                    with open(self.path(self.user_dict, user_name), 'a') as user:
                        conn.send('Enter password')
                        user.writelines(conn.recv(1024).decode('utf-8'))
                        conn.send('User %s successfully created', user_name)
                        self.client_handler(conn, adder, user_name)

            elif '!login' in msg:
                for ptry in range(3):
                    user_name = msg.split(' ')[-1]
                    if os.path.exists(self.path(self.user_dict, user_name)):
                        conn.send('Enter password: ')
                        passwd = conn.recv(1024).decode('utf-8')
                        with open(self.path(self.user_dict, user_name), 'a') as user:
                            fpasswd = user.readline(0)
                        if fpasswd == passwd:
                            self.client_handler(conn, adder, user_name)
                        else:
                            conn.send(
                                'User name/Password is wrong.\n!login [User_name] \n try - %d/3' % ptry+1)
                run = False

        return False

    def client_Accept(self):
        while True:
            time.sleep(0.1)
            (conn, adder) = self.server.accept()
            self.connections.append(conn)
            self.client = threading.Thread(
                target=self.user_login, args=(conn, adder))
            self.client.setDaemon(True)
            self.client.start()


server()
