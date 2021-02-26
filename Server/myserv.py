from Socketserver import Server
from User import Login
from User import commands
import log_handler as logging
import os
import time

connections = []
usr = {}


def log(conn, adder):
    logging.conn_log(adder[0] + ' is logged in to the server.')
    log_in = False
    try:
        conn.send(bytes(
            ' type /login [user_name] For login\nor type/register [user_name] For register\n', 'utf-8'))
    except:
        conn.close()
        # to be - Disconnected message
    while not log_in:
        try:
            l_msg = conn.recv(1024).decode('utf-8')
        except:
            conn.close()
            break
        if not l_msg:
            # to be - Disconnected message
            conn.close()
            break
        elif '/login' in l_msg and len(l_msg) > 7:
            u_msg = l_msg.split(' ')[-1]
            try:
                conn.send(bytes(str('enter your password ' + u_msg), 'utf-8'))
                p_msg = conn.recv(1024).decode('utf-8')
            except:
                conn.close()
                # to be - Disconnected message
                break
            if logs.login(u_msg, p_msg):
                conn.send(bytes('Succssefully logged in', 'utf-8'))
                connections.append(conn)
                usr[u_msg] = logs.get_obj()
                print(usr[u_msg].admin)
                print(u_msg, 'Logged in')
                logging.usr_log(u_msg + ' is logged in to the server.')
                chat(conn, adder, u_msg)
            elif logs.logged_in(u_msg):
                conn.send(
                    bytes('User_name allready connected to server.', 'utf-8'))
            else:
                try:
                    print(logs.user_info[0].split(':')[-1])
                except IndexError:
                    pass
                conn.send(
                    bytes('User_name/Password are Dont exsist/Wrong!.', 'utf-8'))
        elif '/register' in l_msg:
            conn.send(bytes('Enter password: ', 'utf-8'))
            try:
                p_msg = conn.recv(1024).decode('utf-8')
            except:
                conn.close()
                # to be - Disconnected message
                break
            if logs.register(u_msg, p_msg):
                conn.send(bytes('   Succssefully logged in   ', 'utf-8'))
                connections.append(conn)
                print(u_msg, 'Logged in')
                logging.usr_log(u_msg + ' is logged in to the server.')
                chat(conn, adder, u_msg)
            elif logs.exsist(u_msg):
                conn.send(
                    bytes('User_name not aviailable.', 'utf-8'))
        elif '/login' in l_msg and len(l_msg) <= 7:
            conn.send(bytes('No user name enterd!', 'utf-8'))
        else:
            conn.send(bytes('Wrong comand!', 'utf-8'))


def notify_all(conn, user_name, msg):
    for con in connections:
        if con != conn:
            msg_all = user_name + ' - ' + msg
            con.send(bytes(msg_all, 'utf-8'))
        elif con == conn:
            msg_you = 'You - ' + msg
            con.send(bytes(msg_you, 'utf-8'))


def notify_conn(conn, msg):
    conn.send(bytes(msg, 'utf-8'))


def is_admin(user_name):
    return logs.has_admin(user_name)


def welcome(conn, user_name):
    conn.send(bytes(user_name + ' - Welcome! to the server\n', 'utf-8'))
    for con in connections:
        if con != conn:
            mesg = user_name + ' Connected to the server'
            con.send(bytes(mesg, 'utf-8'))


def file_handler(conn, user_name, file_buffer, file_name, file_size):
    chunk = ''
    while file_buffer > 1024:
        chunk += conn.recv(1024).decode('utf-8')
        file_buffer = file_buffer - 1024
    chunk += conn.recv(1024).decode('utf-8')
    with open(os.path.join(root_path, 'Files', file_name), 'wb') as file:
        file.write(chunk)
    msg = 'Server recived file\nsender: ' + user_name + \
        '\nfile name: ' + file_name + '\nsize: ' + file_size
    notify_all(conn, user_name, msg)


def chat(conn, adder, user_name):
    welcome(conn, user_name)
    while True:
        time.sleep(0.1)
        msg = conn.recv(1024).decode('utf-8')
        if not msg:
            break
        elif '/' in msg[0]:
            commands(conn, usr[user_name], msg)
        else:
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
