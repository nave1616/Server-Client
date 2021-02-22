import socket
import threading
from sys import argv


class Server(socket.socket):

    def __init__(self):
        socket.socket.__init__(self, socket.AF_INET, socket.SOCK_STREAM)
        self.ip = '0.0.0.0'
        self.port = 5050
        self.s_run = True
        self.bind((self.ip, self.port))
        self.listen()
        print('Server listening on', self.port)

    def accept_connection(self, arg):
        print('*Server is running')
        while self.s_run:
            (conn, adder) = self.accept()
            Client = threading.Thread(target=arg, args=(conn, adder))
            Client.setDaemon(True)
            Client.start()


if __name__ == '__main__':
    s = Server()
    s.accept_connection(argv[1])
