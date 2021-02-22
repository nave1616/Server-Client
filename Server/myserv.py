from Socketserver import Server
from Login import Login
connections = []


def log(conn, adder):
    log_in = False
    while not log_in:
        conn.send(bytes(
            'type /login [user_name] For login\nor type/register [user_name] For register\n', 'utf-8'))
        l_msg = conn.recv(1024).decode('utf-8')
        if '/login' in l_msg:
            conn.send(bytes('Enter password: ', 'utf-8'))
            p_msg = conn.recv(1024).decode('utf-8')
            u_msg = l_msg.split(' ')[-1]
            if logs.login(u_msg, p_msg):
                conn.send(bytes('Succssefully logged in\n', 'utf-8'))
                connections.append(conn)
                print(u_msg, 'Logged in')
                break
            elif u_msg in logs.users:
                conn.send(
                    bytes('\nUser_name allready connected to server.\n\n', 'utf-8'))
            else:
                conn.send(
                    bytes('\nUser_name/Password are Dont exsist/Wrong!.\n\n', 'utf-8'))
        elif '/register' in l_msg:
            pass
        else:
            conn.send(bytes('Wrong comand!\n', 'utf-8'))
    chat(conn, adder, u_msg)


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
    conn.send(bytes(user_name+'Welcome! to the server\n', 'utf-8'))
    for con in connections:
        if con != conn:
            mesg = user_name+' Connected to the server'
            con.send(bytes(mesg, 'utf-8'))


def chat(conn, adder, user_name):
    welcome(conn, user_name)
    while True:
        msg = conn.recv(1024).decode('utf-8')
        if not msg:
            break
        print(user_name, '-', msg)
        notify_all(conn, user_name, msg)
    conn.close()
    print('*', user_name, 'Discconected from server*')
    logs.users.remove(user_name)
    connections.remove(conn)


logs = Login()
server = Server()
server.accept_connection(log)
