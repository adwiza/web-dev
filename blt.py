import os
import socket

REQUEST = b"""\
GET / HTTP/1.1
Host: localhost:5000
"""


def load_test(max_clients, max_conns):
    for client_num in range(max_clients):
        pid = os.fork()
        if pid == 0:
            for connection_num in range(max_conns):
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect(('localhost', 9090))
                sock.sendall(REQUEST)


# os._exit(0)
load_test(49, 100)
