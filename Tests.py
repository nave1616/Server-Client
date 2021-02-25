import socket
import threading
import time
import stdiomask
import curses
from os import system, path


class user():

    def __init__(self):
        self.ip = '0.0.0.0'
        self.port = 5050
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.connect((self.ip, self.port))
        self.username = None
        self.text = []
        self.run = False
        self.realease = False
        self.admin = None

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

        curses.init_pair(2, curses.COLOR_YELLOW,
                         curses.COLOR_CYAN)
        curses.init_pair(3, curses.COLOR_WHITE,
                         curses.COLOR_RED)
        self.login_window(stdscr)
        msg_win_thread = threading.Thread(target=self.recv_m, args=(stdscr,))
        msg_win_thread.setDaemon(True)
        msg_win_thread.start()
        self.send_m(stdscr)

    def login_window(self, stdscr):
        max_y, max_x = stdscr.getmaxyx()
        # login_window
        login_win = curses.newwin(max_y - 3, max_x, 0, 0)
        # input windows
        height, width = 3, 80
        input_begin_x, input_begin_y = 0, 21
        step_y = 1
        step_X = 16
        inp = ''
        input_win = curses.newwin(height, width, input_begin_y, input_begin_x)
        while True:
            time.sleep(0.1)
            self.msg = self.server.recv(1024).decode('utf-8')
            if not self.msg:
                return False
            elif 'wrong' in self.msg or 'exsist' in self.msg or '/login' in self.msg or '/register' in self.msg:
                pass
            elif 'password' in self.msg:
                ans = stdiomask.getpass(prompt=self.msg.rstrip('\n') + ': ')
                self.server.send(bytes(ans, 'utf-8'))
            elif 'Succssefully' in self.msg:
                self.run = True
                curses.endwin()
                return True
            login_win.addstr(self.msg)
            input_win.addstr('Enter command:')
            login_win.refresh()
            input_win.refresh()

    def draw_msg(self, curr_y, text, window, color_atter=1):
        window.addstr(curr_y, 1, text, curses.color_pair(color_atter))

    def recv_m(self, stdscr):

        # self.pad//
        self.page = 0
        self.show = 0
        _, max_x = stdscr.getmaxyx()
        self.msg_current_print_y = 0
        self.msg_current_y = 0
        self.pad = curses.newpad(200, 200)
        self.pad.scrollok(True)
        self.pad.bkgd(' ', curses.color_pair(1))

        mypad_refresh = lambda: self.pad.refresh(
            self.msg_current_y, 0, self.msg_current_print_y, 0, 20, max_x - 1)

        self.draw_msg(self.msg_current_y, self.msg, self.pad, 2)
        mypad_refresh()
        self.msg_current_print_y += 3
        self.msg_current_y += 3
        self.realease = True
        while self.run:
            g_msg = self.server.recv(1024).decode('utf-8')
            if not g_msg:
                self.run = False
            else:
                curses.curs_set(0)
                if 18 >= self.msg_current_print_y >= 0:
                    self.draw_msg(self.msg_current_y, g_msg, self.pad)
                    mypad_refresh()
                    self.msg_current_print_y += 1
                    self.msg_current_y += 1
                else:
                    self.draw_msg(self.msg_current_y, g_msg, self.pad)
                    mypad_refresh()
                    self.msg_current_print_y = 0
                    self.msg_current_y += 1
                    self.page = int(self.msg_current_y / 18)
                self.show = self.msg_current_y
        curses.endwin()
        self.server.close()
        print('**   Disconnected from server    **')
        time.sleep(3)

    def send_m(self, stdscr):

        height, width = 3, 80
        input_begin_x, input_begin_y = 0, 21
        step_y = 1
        step_X = 16
        inp = ''

        while not self.realease:
            time.sleep(0.1)
        self.win = curses.newwin(
            height, width, input_begin_y, input_begin_x)
        self.win.keypad(True)
        self.win.bkgd(' ', curses.color_pair(1))
        curses.curs_set(1)
        while self.run:
            self.win.clrtoeol()
            self.win.box()
            self.win.addstr(step_y, 1, 'Enter message:')
            self.win.move(step_y, step_X)
            self.win.refresh()
            get = self.win.getch()
            if get != ord('\n') and get != curses.KEY_UP and get != curses.KEY_DOWN:
                inp = inp + chr(get)
                self.win.addch(step_y, step_X, chr(get))
                step_X += 1
            elif get == curses.KEY_UP and self.show > 0 and self.page > 0:
                self.show -= 1
                self.pad.refresh(self.show, 0,
                                 0, 0, 20, 40)
                self.win.refresh()
            elif get == curses.KEY_DOWN and self.show < self.msg_current_y:
                self.show += 1
                self.pad.refresh(self.show, 0,
                                 self.msg_current_print_y + 1, 0, 20, 40)
                self.win.refresh()
            else:
                if self.run and inp[0] != '/':
                    self.win.clrtoeol()
                    self.win.refresh()
                    self.server.send(bytes(inp, 'utf-8'))
                    inp = ''
                    step_X = 16
                else:
                    path = inp.strip(' ')[-1]
                    self.server.send(bytes(path, 'utf-8'))
                    path = inp.strip(' ')[-1]
                    with open(path, 'rb') as file:
                        data = file.read()
                    self.server.send(bytes(len(data), 'utf-8'))
                    self.server.send(data)
        self.server.close()


server_init = user()
main_win = curses.wrapper(server_init.window)
connect = main_win.login_window()
if not connect:
    print('Cant connect server\n*Disconnected from server')
    time.sleep(3)
else:
    curses.wrapper(main_win.window)
