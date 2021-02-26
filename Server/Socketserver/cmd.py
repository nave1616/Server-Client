import os


def convert_bytes(num):
    """
    this function will convert bytes to MB.... GB... etc
    """
    step_unit = 1000.0  # 1024 bad the size

    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < step_unit:
            return "%3.1f %s" % (num, x)
        num /= step_unit
    return num


def file_handeler(conn, usr, root_path, file_path):
    print('Reciving file from', usr.user_name)
    chunk = b''
    file_name = file_path.split('/')[-1]
    try:
        buffer_size = conn.recv(4096).decode('utf-8')
    except UnicodeDecodeError:
        buffer_size = conn.recv(4096)
        return 'Error occurred'
    try:
        file_buffer = int(buffer_size)
    except ValueError:
        return 'Error occurred'
    file_size = convert_bytes(file_buffer)
    while 4096 < file_buffer:
        file_buffer = file_buffer - 4096
        chunk += conn.recv(4096)
    chunk += conn.recv(file_buffer)
    with open(os.path.join(root_path, file_name), 'wb') as file_writer:
        file_writer.write(chunk)
    msg = 'Server file recv\nSender: ' + usr.user_name + \
        '\nFile name: ' + file_name + '\nFile size is:' + str(file_size)
    return msg


def main_handeler(conn, usr, command):
    action = command.split(' ')[-1]
    com = command.split(' ')[0:-1]
    root_path = '/home/vegi/Desktop/work/Server/Files'
    if '/file' in command:
        msg = file_handeler(conn, usr, root_path, action)
        return msg
    else:
        return str(com) + ' not exsist '
