import os


def file_handeler(conn, usr, path, command):
    chunk = ''
    file_name = path.split('/')[-1]
    file_buffer = conn.recv(1024).decode('utf-8')
    try:
        file_buffer = int(file_buffer)
    except ValueError:
        return 'Error'
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


def main_handeler(conn, usr, command):
    action = command.split(' ')[-1]
    root_path = 'Server/Files'
    if '!file' in command:
        msg = file_handeler(conn, usr, root_path, action)
        return msg
