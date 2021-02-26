import socket
import threading
import time
import stdiomask
import curses
import os
from pathlib import Path


class Terminal():

    def __init__(self, socket):
        self.socket = socket

        self.username = None
        self.text = []
        self.run = True
        self.realease = False
        self.connected = False

    def window(self, stdscr):
        stdscr.refresh()
        curses.noecho()
        curses.cbreak()
        stdscr.nodelay(1)
        stdscr.keypad(True)
        curses.start_color()
        # 1 - bg=CAYAN,TEXT=WHITE
        # 2 - bg=CAYAN,TEXT=YELLOW
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_CYAN)

        curses.init_pair(2, curses.COLOR_WHITE,
                         curses.COLOR_GREEN)
        curses.init_pair(3, curses.COLOR_RED,
                         curses.COLOR_CYAN)
        msg_win_thread = threading.Thread(target=self.recv_m, args=(stdscr,))
        msg_win_thread.setDaemon(True)
        msg_win_thread.start()
        self.send_m(stdscr)

    def draw_msg(self, curr_y, text, window, color_atter=1):
        if color_atter != 1:
            window.addstr(curr_y, 1, text, curses.color_pair(
                color_atter) | curses.A_BOLD)
        else:
            window.addstr(curr_y, 1, text, curses.color_pair(
                color_atter))

    def announce(self, curr_y, text, window, color_atter=1):
        for i in range(len(text)):
            for j in range(200):
                lett_pos = (i + j - 1) % len(text)
                window.addstr(curr_y, ((self.max_x // 2) - len(text) + 10) + i, text[lett_pos],
                              curses.color_pair(color_atter))
                self.pad.refresh(curr_y, 0,
                                 curr_y, 0, 20, self.max_x - 1)
            time.sleep(0.1)

    def recv_m(self, stdscr):

        # self.pad//
        self.page = 0
        self.show = 0
        _, self.max_x = stdscr.getmaxyx()
        self.msg_current_print_y = 0
        self.msg_current_y = 0
        self.pad = curses.newpad(4000, 200)
        self.pad.scrollok(True)
        self.pad.bkgd(' ', curses.color_pair(1))

        self.mypad_refresh = lambda: self.pad.refresh(
            self.msg_current_y, 0, self.msg_current_print_y, 0, 20, self.max_x - 1)
        self.mypad_refresh()
        while self.run:
            self.realease = True
            self.g_msg = self.socket.recv(1024).decode('utf-8')
            self.realease = False
            curses.curs_set(0)
            if not self.g_msg:
                self.run = False
                self.draw_msg(self.msg_current_y,
                              '**Server is closed**', self.pad)
                self.mypad_refresh()
            else:
                spaces = self.g_msg.count('\n') + 1
                if 'Succssefully' in self.g_msg and not self.connected:
                    self.connected = True
                    self.announce(self.msg_current_y,
                                  self.g_msg, self.pad, color_atter=2)
                elif 'Wrong' in self.g_msg or 'allready connected' in self.g_msg or 'No' in self.g_msg and not self.connected:
                    self.draw_msg(self.msg_current_y,
                                  self.g_msg, self.pad, color_atter=3)
                else:
                    self.draw_msg(self.msg_current_y, self.g_msg, self.pad)
                self.mypad_refresh()
                if 17 >= (self.msg_current_print_y + spaces) >= 0:
                    self.msg_current_print_y += spaces
                    self.msg_current_y += spaces
                else:
                    self.msg_current_print_y = 0
                    self.msg_current_y += spaces
                    self.page = int(self.msg_current_y / 18)
                self.show = self.msg_current_y
        self.socket.close()
        time.sleep(5)
        curses.endwin()

    def send_m(self, stdscr):

        height, width = 3, 80
        input_begin_x, input_begin_y = 0, 21
        step_y = 1
        step_X = 16
        inp = ''
        win = curses.newwin(
            height, width, input_begin_y, input_begin_x)
        while not self.realease:
            time.sleep(0.01)
        win.keypad(True)
        win.bkgd(' ', curses.color_pair(1))
        while self.run:
            time.sleep(0.01)
            win.box()
            if self.connected == False:
                if 'password' in self.g_msg:
                    win.addstr(step_y, 1, 'Enter password:')
                else:
                    win.addstr(step_y, 1, 'Enter command: ')
            elif self.connected == True:
                win.addstr(step_y, 1, 'Enter message: ')
            win.move(step_y, step_X)
            win.refresh()
            get = win.getch()
            if self.realease:
                curses.curs_set(1)
                if get != ord('\n') and get != curses.KEY_UP and get != curses.KEY_DOWN and get != curses.KEY_BACKSPACE:
                    if 'password' in self.g_msg and self.connected == False:
                        inp = inp + chr(get)
                        win.addch(step_y, step_X + 1, '*')
                        step_X += 1
                    else:
                        inp = inp + chr(get)
                        win.addch(step_y, step_X, chr(get))
                        step_X += 1
                elif get == curses.KEY_UP and self.show > 0 and self.page > 0:
                    self.show -= 1
                    self.pad.refresh(self.show, 0,
                                     0, 0, 20, 40)
                    win.refresh()
                elif get == curses.KEY_DOWN and self.show < self.msg_current_y:
                    self.show += 1
                    self.pad.refresh(self.show, 0,
                                     self.msg_current_print_y + 1, 0, 20, 40)
                    win.refresh()
                elif get == curses.KEY_BACKSPACE:
                    if step_X - 1 > 15:
                        step_X -= 1
                        win.move(step_y, step_X)
                        win.clrtoeol()
                        win.refresh()
                        inp = inp[0:len(inp) - 1]
                elif get == ord('\n') and inp != '':
                    step_X = 16
                    win.move(step_y, step_X)
                    win.clrtoeol()
                    win.refresh()
                    if self.run and inp[0] != '/':
                        self.socket.send(bytes(inp, 'utf-8'))
                    elif self.run and inp[0] == '/' and self.connected == False:
                        self.socket.send(bytes(inp, 'utf-8'))
                    elif self.run and inp[0] == '/' and self.connected == True:
                        inp = str(inp)
                        file_path = inp.split(' ')[-1]
                        self.socket.send(bytes(str(inp), 'utf-8')
                                         )  # msg /file path
                        time.sleep(0.5)
                        try:
                            data_buffer = str(Path(file_path).stat().st_size)
                        except FileNotFoundError:
                            # To do error file not exist
                            pass
                        self.socket.send(
                            bytes(data_buffer, 'utf-8'))  # file size
                        data = Path(file_path).read_bytes()
                        self.socket.send(data)  # file data
                    inp = ''
                    win.refresh()
            else:
                continue
        self.socket.close()


ip = '0.0.0.0'
port = 5050
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect((ip, port))
lock = threading.Lock()
server_init = Terminal(server)
main_win = curses.wrapper(server_init.window)
