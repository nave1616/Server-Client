import socket
import threading
import time
import stdiomask
import curses
import os
from commands import main_handeler
from pathlib import Path


class Terminal():

    def __init__(self, socket):
        self.socket = socket
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

    def draw_msg(self, spaces, text, color_attr=1):
        self.pad.addstr(self.msg_current_y, 1, text, curses.color_pair(
            color_attr))
        self.mypad_refresh()
        if 17 >= (self.msg_current_print_y + spaces) >= 0:
            self.msg_current_print_y += spaces
            self.msg_current_y += spaces
        else:
            self.msg_current_print_y = 0
            self.msg_current_y += spaces
            self.page = int(self.msg_current_y / 18)
        self.show = self.msg_current_y

    def announce(self, text, color_attr=1):
        # To fix
        for i in range(len(text)):
            for j in range(200):
                lett_pos = (i + j - 1) % len(text)
                self.pad.addstr(self.msg_current_y, ((self.max_x // 2) - len(text) + 10) + i, text[lett_pos],
                                curses.color_pair(color_attr))
                self.pad.refresh(self.msg_current_y, 0,
                                 self.msg_current_y, 0, 20, self.max_x - 1)
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
            color = 1
            if self.g_msg[0].isdigit():
                color = int(self.g_msg[0])
                self.g_msg = self.g_msg[1:]
            if not self.g_msg:
                self.run = False
                self.draw_msg(1, '**Server is closed**', color_attr=color)
            if 'Succssefully' in self.g_msg and not self.connected:
                self.connected = True
            spaces = self.g_msg.count('\n') + 1
            self.draw_msg(spaces, self.g_msg, color_attr=color)
        self.socket.close()
        time.sleep(5)
        curses.endwin()

    def scroll(self, scroll_val):
        if scroll_val == 'down':
            self.show += 1
            self.pad.refresh(self.show, 0,
                             0, 0, 20, 40)
        else:
            self.show -= 1
            self.pad.refresh(self.show, 0,
                             0, 0, 20, 40)

    def erase(self, inp, step_X, step_y, win):
        if step_X - 1 > 15:
            step_X -= 1
            win.move(step_y, step_X)
            win.clrtoeol()
            win.refresh()
            inp = inp[0:len(inp) - 1]
        return (step_X, inp)

    def input(self, inp, step_X, step_y, win, get):
        if 'password' in self.g_msg and self.connected == False:
            win.addstr(step_y, 1, 'Enter password:')
            inp = inp + chr(get)
            win.addch(step_y, step_X + 1, '*')
            step_X += 1
        else:
            if self.connected == False:
                win.addstr(step_y, 1, 'Enter command: ')
            else:
                win.addstr(step_y, 1, 'Enter message: ')
            inp = inp + chr(get)
            win.addch(step_y, step_X, chr(get))
            step_X += 1
        return (step_X, inp)

    def enter_pressed(self, inp, step_y, win):
        win.move(step_y, 16)
        win.clrtoeol()
        win.refresh()
        if self.run and inp[0] != '/':
            self.socket.send(bytes(inp, 'utf-8'))
        elif self.run and inp[0] == '/' and self.connected == False:
            self.socket.send(bytes(inp, 'utf-8'))
        elif self.run and inp[0] == '/' and self.connected == True:
            msg = main_handeler(self.socket, inp)
            if msg != None:
                self.draw_msg(1, msg, color_attr=2)
        inp = ''
        win.refresh()
        return inp

    def send_m(self, stdscr):
        height, width = 3, 80
        input_begin_x, input_begin_y = 0, 21
        step_y = 1
        step_X = 16
        inp = ''
        win = curses.newwin(
            height, width, input_begin_y, input_begin_x)
        win.keypad(True)
        win.bkgd(' ', curses.color_pair(1))
        while not self.realease:
            time.sleep(0.01)
        win.addstr(step_y, 1, 'Enter command: ')
        while self.run:
            win.box()
            win.move(step_y, step_X)
            get = win.getch()
            if self.realease:
                if get != ord('\n') and get != curses.KEY_UP and get != curses.KEY_DOWN and get != curses.KEY_BACKSPACE:
                    step_X, inp = self.input(inp, step_X, step_y, win, get)
                elif get == curses.KEY_UP and self.show > 0 and self.page > 0:
                    self.scroll('up')
                elif get == curses.KEY_DOWN and self.show < self.msg_current_y:
                    # Need fix
                    self.scroll('down')
                elif get == curses.KEY_BACKSPACE:
                    step_X, inp = self.erase(inp, step_X, step_y, win)
                elif get == ord('\n') and inp != '':
                    step_X = 16
                    inp = self.enter_pressed(inp, step_y, win)
                win.refresh()
            else:
                time.sleep(0.01)
        self.socket.close()


ip = '0.0.0.0'
port = 5050
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect((ip, port))
server_init = Terminal(server)
main_win = curses.wrapper(server_init.window)
