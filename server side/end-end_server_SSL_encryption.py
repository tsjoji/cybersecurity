from socket import AF_INET, SOCK_STREAM, SO_REUSEADDR, SOL_SOCKET, SHUT_RDWR
import ssl, hashlib, binascii, os, socket
from typing import Dict
from collections import defaultdict

def check_password(stored_pass, provided_pass):

    salt = stored_pass[:64]
    stored_pass = stored_pass[64:]
    hash = hashlib.pbkdf2_hmac('sha512',provided_pass.encode('utf-8'),salt.encode('ascii'),987654)
    hash = binascii.hexlify(hash).decode('ascii')
    return hash == stored_pass


DB = defaultdict(list)
addr = '127.0.0.1'
port = 8080
server_cert = 'server.crt'
server_key = 'server.key'
f=open('db.txt', 'r')
for line in f:
    data= line.split(",")
    DB[str(data[0])]= str(data[1])


options = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)#this is my key agreement protocol (ciphers are choosen through this) if you comment this line out you will see what i mean
#options.verify_mode = ssl.CERT_REQUIRED #this makes my self written SSL fail the check so I can't have it on
options.load_cert_chain(certfile=server_cert, keyfile=server_key)

sock = socket.socket()
sock.bind((addr, port))
sock.listen(1)
newsocket, fromaddr = sock.accept()
conn = options.wrap_socket(newsocket, server_side=True)

while True:
    buffer = b''
    try:
            data = conn.recv(4096)
            if data:
                buffer += data
            else:
                #this is going to be the friends list return part
                break
    except:
        print('error occured')
        continue
    data = buffer.decode("utf-8").split(", ")
    name= (DB.get(data[0]))[:-1]
    wrong ="username and password mismatch"
    right =("welcome "+ data[0])
    if name is not None :
        if check_password(name, data[1]):#correct username is Jorge Teixeira and password is 1234, other correct username is Hello World and password is abcd
            print(b"welcome "+ data[0].encode('utf-8'))
            conn.send(right.encode())
        else:
            conn.send(wrong.encode())
            print("username and password mismatch")
    else:
        conn.send(wrong.encode())
        print("username and password mismatch")



conn.shutdown(socket.SHUT_RDWR)
conn.close()