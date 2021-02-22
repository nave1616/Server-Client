import socket
import threading
import time
import stdiomask
import select
import sys
import curses


class user():
    def __init__(self):
        self.ip = '0.0.0.0'
        self.port = 5050
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.connect((self.ip, self.port))
        self.username = None
        self.text = []
        self.admin = None
        self.login()

    def login(self):
        while True:
            time.sleep(0.1)
            self.msg = self.server.recv(1024).decode('utf-8')
            if not self.msg:
                break
            elif 'wrong' in self.msg or 'exsist' in self.msg or '/login' in self.msg or '/register' in self.msg:
                print(self.msg)
                ans = input('Enter command: ')
                self.server.send(bytes(ans, 'utf-8'))
            elif 'password' in self.msg:
                ans = stdiomask.getpass(prompt=self.msg.rstrip('\n')+': ')
                self.server.send(bytes(ans, 'utf-8'))
            elif 'Succssefully' in self.msg:
                break
        curses.wrapper(self.chat)

    def draw_msg(self, curr_y, text, window):
        window.addstr(curr_y, 0, text)

    def chat(self, stdscr):
        stdscr.refresh()
        curses.noecho
        curses.cbreak()
        stdscr.nodelay(1)
        stdscr.keypad(True)
        max_y, max_X = stdscr.getmaxyx()
        msg_current_print_y = 0
        msg_current_y = 0
        height = 3
        width = max_X-1
        input_begin_x = 0
        input_begin_y = int(max_y-3)
        step_y = 0
        step_X = 16
        show = msg_current_y
        pad = curses.newpad(200, 200)
        pad.scrollok(True)
        win = curses.newwin(height, width, input_begin_y, input_begin_x)
        win.keypad(True)
        win.clear()
        win.box()
        win.refresh()

        def mypad_refresh(): return pad.refresh(
            msg_current_y, 0, msg_current_print_y, 0, 20, 40)
        inp = ''
        self.draw_msg(msg_current_y, self.msg, pad)
        mypad_refresh()
        msg_current_print_y += 2
        msg_current_y += 2
        win.box()
        win.addstr(step_y+1, 1, 'Enter message:')
        win.refresh()
        while True:
            time.sleep(0.1)
            self.inputs = [self.server, sys.stdin]
            ready_r, _, _ = select.select(self.inputs, [], [])
            win.box()
            win.addstr(step_y+1, 1, 'Enter message:')
            win.refresh()
            for ready in ready_r:
                if ready == self.server:
                    g_msg = self.server.recv(1024).decode('utf-8')
                    if not g_msg:
                        break
                    else:
                        if msg_current_print_y != 18:
                            self.draw_msg(msg_current_y, g_msg, pad)
                            mypad_refresh()
                            msg_current_print_y += 1
                            msg_current_y += 1
                        else:
                            self.draw_msg(msg_current_y, g_msg, pad)
                            mypad_refresh()
                            msg_current_print_y = 0
                            msg_current_y += 1
                        win.refresh()
                        show = msg_current_y
                else:
                    get = win.getch()
                    win.move(step_y+1, step_X)
                    if get != ord('\n') and get != curses.KEY_UP and get != curses.KEY_DOWN:
                        inp = inp+chr(get)
                        win.addch(step_y+1, step_X, chr(get))
                        step_X += 1
                        win.refresh()
                    elif get == curses.KEY_UP and show > 0:
                        show -= 1
                        pad.refresh(show, 0,
                                    msg_current_print_y-1, 0, 20, 40)
                        win.refresh()
                    elif get == curses.KEY_DOWN and show < msg_current_y:
                        show += 1
                        pad.refresh(show, 0,
                                    msg_current_print_y+1, 0, 20, 40)
                        win.refresh()
                    else:
                        self.server.send(bytes(inp, 'utf-8'))
                        inp = ''
                        step_X = 16
                        win.clear()
                        win.box()
                        win.addstr(step_y+1, 1, 'Enter message:')
                        win.refresh()


user()
