import socket

def pack_str(string: str):
    return len(string).to_bytes(2, 'little') + string.encode() # Might want to change to big



sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.connect(('localhost', 4545))


while True:
    sdata = b'\x01\x0Bcomputer.jt' #input('> ')
    if sdata == 'quit': break
    # sock.send(b'\x02'+pack_str(sdata)+b'\x00\x00')
    sock.send(sdata)

    data = sock.recv(1024)
    if not data: break
    print('<', data)
    break

sock.close()