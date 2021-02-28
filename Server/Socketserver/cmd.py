import os
from pathlib import Path
import time
import threading


def notify_conn(conn, msg):
    conn.send(bytes(msg, 'utf-8'))


def update_conn(conn):
    conn.send(bytes('File upload start', 'utf-8'))
    while not finish:
        conn.send(bytes(update_info, 'utf-8'))
        time.sleep(10)
    conn.send(bytes('Upload Finsh', 'utf-8'))

# ban
# setadmin


def kick_user(conn, usr, command, user_name, connections):
    user_tokick_name = command.split(' ')[-1]
    print(type(usr[user_name].admin), usr[user_name].admin)
    if usr[user_name].admin:
        try:
            notify_conn(usr[user_tokick_name].con,
                        '3Admin had kick you from the server')
            usr[user_tokick_name].con.close()
            connections.remove(usr[user_tokick_name].con)
            return '3Admin ' + user_name + ' is kicked ' + user_tokick_name + ' from the server.'
        except:
            notify_conn(
                conn, str(3) + user_tokick_name + ' not exsist')
    else:
        notify_conn(conn, '3You are not admin')


def convert_bytes(num):
    step_unit = 1000.0  # 1024 bad the size

    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < step_unit:
            return "%3.1f %s" % (num, x)
        num /= step_unit
    return num


def file_handeler(conn, user_name, root_path, file_path):
    global finish
    global update_info
    print('Reciving file from', user_name)
    chunk = b''
    file_name = Path(file_path).name
    try:
        buffer_size = conn.recv(4096).decode('utf-8')
    except UnicodeDecodeError:
        notify_conn(conn, '3Error occurred')
        return
    try:
        file_buffer = int(buffer_size)
    except ValueError:
        notify_conn(conn, '3Error occurred')
        return
    file_size = convert_bytes(file_buffer)
    getnow = 0
    if file_buffer > 10000000:  # 10MB
        update = threading.Thread(target=update_conn, args=(conn,))
        update.setDaemon(True)
        update.start()
    else:
        notify_conn(conn, 'File upload is started')
    while 4096 < file_buffer:
        file_buffer = file_buffer - 4096
        getnow += 4096
        update_info = 'File recive ' + \
            convert_bytes(getnow) + ' from ' + file_size
        print(update_info, end='\r', flush=True)
        chunk += conn.recv(4096)
    chunk += conn.recv(file_buffer)
    print('')
    finish = True
    with open(root_path / file_name, 'wb') as file_writer:
        file_writer.write(chunk)
    msg = 'Server file recv\n Sender: ' + user_name + '\n File name: ' + \
        file_name + '\n File size is:' + str(file_size)
    return msg


def main_handeler(conn, usr, command, user_name, connections):
    action = command.split(' ')[-1]
    com = command.split(' ')[0: -1]
    # /home/vegi/Desktop/work/Server/Socketserver/
    root_path = Path(__file__).parent.absolute()
    # /home/vegi/Desktop/work/Server/
    root_path = root_path / root_path.parents[0]
    if '/file' in command:
        msg = file_handeler(conn, user_name, root_path / 'Files', action)
        return msg
    elif '/kick' in command:
        msg = kick_user(conn, usr, command, user_name, connections)
        return msg
    else:
        if type(com) is str:
            notify_conn(conn, str(3) + command + ' not exsist')
        notify_conn(conn, str(3) + str(com) + ' not exsist ')


getnow = 0

finish = False
