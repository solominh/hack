'''
Created on 20 Jun 2015
 
@author: Robyn Hode
'''
import socket

host = '192.168.0.104'
port = 1991

try:
    serversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversock.bind((host, port))
    serversock.listen(1)

    conn, addr = serversock.accept()
    print('Connected by: ', addr)

    # Receive data
    data = conn.recv(999999999)

    # Write data
    with open("passwords.db", "wb") as filesave:
        filesave.write(data)

except Exception as e:
    print(e)
finally:
    serversock.close()
