'''
Created on 20 Jun 2015
 
@author: Robyn Hode
'''
import socket
import time


HOST = '192.168.0.109'
PORT = 1991

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(1)
    conn, addr = s.accept()

    data = None
    try:
        with conn:
            print('Connected by: ', addr)

            # Receive data
            while True:
                data = conn.recv(1048576)
                if not data:
                    break

                # Write data
                filename = str(addr) + "passwords.db"
                with open(filename, "wb") as f:
                    f.write(data)
                    f.flush()

                conn.send(b'success')
    except Exception as e:
        print(e)


while True:
    try:
        with open(filename, 'rb') as f:
            print(f.read())
            break
    except IOError:
        time.sleep(2)
