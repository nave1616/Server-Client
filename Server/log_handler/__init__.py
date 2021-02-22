import logging
import os


def conn_log(msg):
    addr_logs.warning(msg)


def usr_log(msg):
    user_con_logs.warning(msg)


root_path = os.path.dirname(
    os.path.abspath(__file__))
addr_logs_path = os.path.join(root_path, 'log', 'address_con.log')
user_con_logs_path = os.path.join(root_path, 'log', 'user_con.log')

addr_logs = logging.getLogger(addr_logs_path)
user_con_logs = logging.getLogger(user_con_logs_path)
log_format = logging.Formatter(
    '%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
file_handler = logging.FileHandler(addr_logs_path)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(log_format)
addr_logs.addHandler(file_handler)
file_handler = logging.FileHandler(user_con_logs_path)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(log_format)
user_con_logs.addHandler(file_handler)
