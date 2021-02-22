from Socketserver import Server
from Login import Login
import log_handler as logging
import os
import time

connections = []


def log(conn, adder):
    logging.conn_log(adder[0]+' is logged in to the server.')
    log_in = False
    while not log_in:
        try:
            conn.send(bytes(
                'type /login [user_name] For login\nor type/register [user_name] For register\n', 'utf-8'))
            l_msg = conn.recv(1024).decode('utf-8')
        except:
            conn.close()
            # to be - Disconnected message
            break
        u_msg = l_msg.split(' ')[-1]
        if '/login' in l_msg:
            try:
                conn.send(bytes('Enter password: ', 'utf-8'))
                p_msg = conn.recv(1024).decode('utf-8')
            except:
                conn.close()
                # to be - Disconnected message
                break
            if logs.login(u_msg, p_msg):
                conn.send(bytes('Succssefully logged in\n', 'utf-8'))
                connections.append(conn)
                print(u_msg, 'Logged in')
                logging.usr_log(u_msg+' is logged in to the server.')
                chat(conn, adder, u_msg)
            elif logs.exsist(u_msg):
                conn.send(
                    bytes('\nUser_name allready connected to server.\n\n', 'utf-8'))
            else:
                conn.send(
                    bytes('\nUser_name/Password are Dont exsist/Wrong!.\n\n', 'utf-8'))
        elif '/register' in l_msg:
            conn.send(bytes('Enter password: ', 'utf-8'))
            try:
                p_msg = conn.recv(1024).decode('utf-8')
            except:
                conn.close()
                # to be - Disconnected message
                break
            if logs.register(u_msg, p_msg):
                conn.send(bytes('Succssefully logged in\n', 'utf-8'))
                connections.append(conn)
                print(u_msg, 'Logged in')
                logging.usr_log(u_msg+' is logged in to the server.')
                chat(conn, adder, u_msg)
            elif logs.exsist(u_msg):
                conn.send(
                    bytes('\nUser_name not aviailable.\n\n', 'utf-8'))
        else:
            conn.send(bytes('Wrong comand!\n', 'utf-8'))


def notify_all(conn, user_name, msg):
    for con in connections:
        if con != conn:
            mesg = user_name+' - '+msg
            con.send(bytes(mesg, 'utf-8'))
        else:
            msg = 'You - '+msg
            conn.send(bytes(msg, 'utf-8'))


def notify_conn(conn, msg):
    conn.send(bytes(msg, 'utf-8'))


def welcome(conn, user_name):
    conn.send(bytes(user_name+' - Welcome! to the server\n', 'utf-8'))
    for con in connections:
        if con != conn:
            mesg = user_name+' Connected to the server'
            con.send(bytes(mesg, 'utf-8'))


def file_handler(conn, user_name, file_buffer, file_name, file_size):
    chunk = ''
    while file_buffer > 1024:
        chunk += conn.recv(1024).decode('utf-8')
        file_buffer = file_buffer-1024
    chunk += conn.recv(1024).decode('utf-8')
    with open(os.path.join(root_path, 'Files', file_name), 'wb') as file:
        file.write(chunk)
    msg = 'Server recived file\nsender: '+user_name + \
        '\nfile name: '+file_name+'\nsize: '+file_size
    notify_all(conn, user_name, msg)


def chat(conn, adder, user_name):
    welcome(conn, user_name)
    while True:
        time.sleep(0.1)
        msg = conn.recv(1024).decode('utf-8')
        if not msg:
            break
        if '/file' in msg[:5]:
            file_name = msg.split('\\')[-1]
            try:
                file_buffer = int(conn.recv(1024).decode('utf-8'))
            except:
                pass
            file_size = file_buffer**1024
            file_handler(conn, user_name, file_buffer, file_name, file_size)
        print(user_name, '-', msg)
        notify_all(conn, user_name, msg)
    conn.close()
    print('*', user_name, 'Discconected from server*')
    logs.users.remove(user_name)
    connections.remove(conn)


root_path = os.path.dirname(
    os.path.abspath(__file__))
logs = Login()
server = Server()
server.accept_connection(log)
