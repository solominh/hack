'''
Created on 20 Jun 2015
 
@author: Robyn Hode
'''
import socket
import time


HOST = '192.168.0.104'
PORT = 1991

data = None
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(1)
    conn, addr = s.accept()

    try:
        with conn:
            print('Connected by: ', addr)

            # Receive data
            data = conn.recv(51200)
            conn.send(b'success')
    except Exception as e:
        print(e)


if data:
    # Write data
    filename = str(addr) + "passwords.db"
    with open(filename, "wb") as f:
        f.write(data)
        f.flush()
    while True:
        try:
            with open(filename, 'rb') as f:
                print(f.read())
                break
        except IOError:
            time.sleep(2)
