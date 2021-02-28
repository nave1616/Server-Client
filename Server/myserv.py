from Socketserver import Server
from Socketserver import cmd
from User import User
import log_handler as logging
import os
import time
import concurrent.futures

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
            if logs.login(u_msg, p_msg, conn):
                conn.send(bytes('2Succssefully logged in', 'utf-8'))
                connections.append(conn)
                usr[u_msg] = logs.get_obj()
                print(u_msg, 'Logged in')
                logging.usr_log(u_msg + ' is logged in to the server.')
                chat(conn, adder, u_msg)
            elif logs.logged_in(u_msg):
                conn.send(
                    bytes('3User_name allready connected to server.', 'utf-8'))
            else:
                try:
                    print(logs.user_info[0].split(':')[-1])
                except IndexError:
                    pass
                conn.send(
                    bytes('3User_name/Password are Dont exsist/Wrong!.', 'utf-8'))
        elif '/register' in l_msg:
            conn.send(bytes('Enter password: ', 'utf-8'))
            try:
                p_msg = conn.recv(1024).decode('utf-8')
            except:
                conn.close()
                # to be - Disconnected message
                break
            if logs.register(u_msg, p_msg, conn):
                conn.send(bytes('2   Succssefully logged in   ', 'utf-8'))
                connections.append(conn)
                print(u_msg, 'Logged in')
                logging.usr_log(u_msg + ' is logged in to the server.')
                chat(conn, adder, u_msg)
            elif logs.exsist(u_msg):
                conn.send(
                    bytes('3User_name not aviailable.', 'utf-8'))
        elif '/login' in l_msg and len(l_msg) <= 7:
            conn.send(bytes('3No user name enterd!', 'utf-8'))
        else:
            conn.send(bytes('3Wrong comand!', 'utf-8'))


def notify_all(msg, conn=None, user_name='Server'):
    for con in connections:
        if con != conn:
            msg_all = user_name + ' - ' + msg
            con.send(bytes(msg_all, 'utf-8'))
        elif con == conn:
            msg_you = 'You - ' + msg
            con.send(bytes(msg_you, 'utf-8'))


def color_msg(msg, conn=None, user_name='Server', color_attr=1):
    for con in connections:
        if con != conn:
            msg_all = str(color_attr) + user_name + ' - ' + msg
            con.send(bytes(msg_all, 'utf-8'))
        elif con == conn:
            msg_you = str(color_attr) + 'You - ' + msg
            con.send(bytes(msg_you, 'utf-8'))


def welcome(conn, user_name):
    conn.send(bytes(user_name + ' - Welcome! to the server\n', 'utf-8'))
    for con in connections:
        if con != conn:
            mesg = str(3) + user_name + ' Connected to the server'
            con.send(bytes(mesg, 'utf-8'))


def chat(conn, adder, user_name):
    connected = True
    welcome(conn, user_name)
    while connected:
        try:
            msg = conn.recv(1024).decode('utf-8')
        except OSError:
            connected = False
            break
        if not msg:
            connected = False
            break
        elif '/' in msg[0] and connected:
            with concurrent.futures.ProcessPoolExecutor() as executor:
                command_handeler = executor.submit(
                    cmd.main_handeler, conn, usr, msg, user_name, connections)
                return_value = command_handeler.result()
                if return_value != None:
                    print('Server notify', '-', return_value)
                    notify_all(return_value)
        elif connected and '/' not in msg[0]:
            print(user_name, '-', msg)
            notify_all(msg, conn, user_name)
    conn.close()
    print('*', user_name, 'Discconected from server*')
    if user_name in logs.users:
        logs.users.remove(user_name)  # /User name list
    if conn in connections:
        connections.remove(conn)  # Connections list
    color_msg(user_name + ' disconnected from server', color_attr=3)


root_path = os.path.dirname(
    os.path.abspath(__file__))
logs = User()
server = Server()
server.accept_connection(log)
