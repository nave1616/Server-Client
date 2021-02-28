import os
from pathlib import Path, PureWindowsPath
import time
import threading
import curses


def main_win(stdscr):
    return stdscr


def file_win(stdscr, socket):
    _, x = stdscr.getmaxyx()
    file_win = curses.newwin(4, 20, 1, x - 15)
    file_win.box()
    file_win.addstr(0, 3, 'File update')
    file_win.refresh()
    time.sleep(5)
    while True:
        updates = socket.recv(1024).decode('utf-8')
        if updates == 'Update finsh':
            break
        file_win.addstr(2, 4, updates)
        file_win.refresh()
    file_win.close()


def convert_bytes(num):
    step_unit = 1000.0  # 1024 bad the size
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < step_unit:
            return "%3.1f %s" % (num, x)
        num /= step_unit
    return num


def download_handler():
    pass


def file_handeler(socket, root_path, command):
    file_path = Path(command.split(' ')[-1])
    if file_path.exists():
        socket.send(bytes(str(command), 'utf-8'))  # msg /file path
        time.sleep(0.5)
        data_buffer = str(file_path.stat().st_size)
        socket.send(bytes(data_buffer, 'utf-8'))  # file size
        data = file_path.read_bytes()
        socket.send(data)  # file data
    else:
        return 'File not exsist'


def main_handeler(socket, command):
    root_path = Path(__file__).parent.absolute()  # work/Client/commands
    root_path = root_path / root_path.parents[0]  # work/Client/
    if '/file' in command:
        msg = file_handeler(socket, root_path /
                            'Download', command)
        return msg
    elif '/kick' in command:
        socket.send(bytes(command, 'utf-8'))
    else:
        com = command.split(' ')[0]
        if type(com) == str():
            return str(command) + ' not exsist '
        return str(com) + ' not exsist '
