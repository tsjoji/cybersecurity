from socket import AF_INET, SOCK_STREAM, SO_REUSEADDR, SOL_SOCKET, SHUT_RDWR
import ssl, hashlib, binascii, os, socket
from typing import Dict
from collections import defaultdict
import random
import string
import _thread

def client_enters(conn, fromaddr):
    buffer = b''
    try:
            data = conn.recv(4096)
            if data:
                buffer += data
            else:
                return
    except:
        print('error occured')
        return
    data = buffer.decode("utf-8").split(", ")
    name= (DB.get(data[0]))[:-1]
    wrong ="username and password mismatch"
    if(len(Currently_online)==0):
        right =("nobody is currently online")
    else:
        right=str(Currently_online)
    if name is not None:
        if check_password(name, data[1]):#correct username is Jorge Teixeira and password is 1234, other correct username is Hello World and password is abcd
            session = randomString()
            Currently_online.append([data[0], session])
            print("current people online")
            print(Currently_online)

            conn.send(session.encode()+right.encode())
        else:
            conn.send(wrong.encode())
            print("username and password mismatch")
    else:
        conn.send(wrong.encode())
        print("username and password mismatch")

    while Currently_online!=3:
        a=1+1

def check_password(stored_pass, provided_pass):

    salt = stored_pass[:64]
    stored_pass = stored_pass[64:]
    hash = hashlib.pbkdf2_hmac('sha512',provided_pass.encode('utf-8'),salt.encode('ascii'),987654)
    hash = binascii.hexlify(hash).decode('ascii')
    return hash == stored_pass

def randomString(stringLength=20):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

DB = defaultdict(list)
Currently_online=[]
Full_friendslist= dict()
addr = '127.0.0.1'
port = 8080
server_cert = 'server.crt'
server_key = 'server.key'
f=open('db.txt', 'r')
for line in f:
    data= line.split(",")
    DB[str(data[0])]= str(data[1])
f.close()
k=open('friendslist.txt','r')
for line in k:
    data = line.split("|")
    Full_friendslist[data[0]]= data[1][:-1]
k.close()


options = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)#this is my key agreement protocol (ciphers are choosen through this) if you comment this line out you will see what i mean
options.load_cert_chain(certfile=server_cert, keyfile=server_key)

sock = socket.socket()
sock.bind((addr, port))
sock.listen(1)



while True:
    newsocket, fromaddr = sock.accept()
    conn = options.wrap_socket(newsocket, server_side=True)
    _thread.start_new_thread(client_enters,(conn, fromaddr))

conn.shutdown(socket.SHUT_RDWR)
conn.close()