import socket
import threading

from .utils import *
from .request import *
from .response import *


class app:
    def __init__(self):
        self.pages = {}
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def page(self, route):
        def wrapper(pg) -> str:
            self.pages[route] = pg
            def inner(*args, **kwargs):
                return pg(*args, **kwargs)
            return inner
        return wrapper
    
    
    def connection(self, conn, addr):
        client_str = f'{addr[0]}:{addr[1]}'
        print(f'Connection received from {client_str}')
        while True:
            try:
                data = conn.recv(1024)
                if not data: break
            except ConnectionResetError:
                break
            
            res = self.process_packet(Request(addr[0], addr[1], data))
            for c in res.chunkify():
                conn.send(c)
            # print(f'{client_str}: {data.decode()}')
        print(f'{client_str} disconnected')
        conn.close()
    


    # Takes in raw client -> server packet and returns chunks to send back to client
    def process_packet(self, req: Request) -> Response:
        res = Response() # Will be passed into the page function
        res.opcode = req.get_opcode() # Set return opcode... hopefully it's valid :)

        if req.get_opcode() == 2: # Fetch request
            if req.route == None:
                res.error_code = 3
                res.data = 'You dun did it now! Error 3' # Probably only technical users (aspiring exploiters) could get this message
            else:
                req.print_action(req.route)
            
                try:
                    res.data = self.pages[req.route]()
                except KeyError:
                    res.data = 'Error 4'
                    res.error_code = 4
        else:
            res.error_code = 0
            res.data = 'You dun did it now! Error 0'
            # Maybe do some other stuff...
        return res

    
    def run(self, address: str = 'localhost', port: int = 4242):
        self.sock.bind((address, port))
        print('Listening')
        while True:
            self.sock.listen()
            conn, conn_addr = self.sock.accept()
            threading.Thread(target=self.connection,args=(conn, conn_addr), daemon=True).start()
        
        self.sock.close()

        