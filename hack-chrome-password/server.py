'''
Created on 20 Jun 2015
 
@author: Robyn Hode
'''
import socket
import time


HOST = '192.168.0.104'
PORT = 1991


def recvall(sock):
    BUFF_SIZE = 1024  # 1 KiB
    data = ""
    while True:
        part = sock.recv(BUFF_SIZE)
        data += part
        if part < BUFF_SIZE:
            # either 0 or end of data
            break
    return data


data = None
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(1)
    conn, addr = s.accept()

    try:
        with conn:
            print('Connected by: ', addr)

            # Receive data
            data = recvall(conn)
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
