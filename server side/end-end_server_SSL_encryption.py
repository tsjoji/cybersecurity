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

def hash_password(password):
    """Hash a password for storing."""
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'),
                                salt, 987654)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')

DB = defaultdict(list)
addr = '127.0.0.1'
port = 8080
server_cert = 'server.crt'
server_key = 'server.key'
f=open('db.txt', 'r')
for line in f:
    data= line.split(",")
    DB[str(data[0])]= str(data[1])

# = {"Jorge Teixeira": "0cb1234d09e9235d9c2245dba65734d27273d0540dd9806baeecef0d6c0ab2c6bdcae722bab71a646e20cf8bea550f2b9479585ab3f70eef0a83a506e69bd8ab2d8ecdc37ce0d9f8267c4eb5692ad4795f7597cc92af249c0e29690282b5760c"
#}

options = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)#this is my key agreement protocol (ciphers are choosen through this) if you comment this line out you will see what i mean
#options.verify_mode = ssl.CERT_REQUIRED #this makes my self written SSL fail the check so I can't have it on
options.load_cert_chain(certfile=server_cert, keyfile=server_key)

sock = socket.socket()
sock.bind((addr, port))
sock.listen(10)

while True:
    newsocket, fromaddr = sock.accept()
    conn = options.wrap_socket(newsocket, server_side=True)
    buffer = b''
    try:
        while True:

            data = conn.recv(4096)
            if data:
                buffer += data
            else:
                #this is going to be the friends list return part
                break
    finally:

        data = buffer.decode("utf-8").split(", ")
        name= (DB.get(data[0]))[:-1]
        print("hello"+name+"world")
        print("hello"+data[0] + "world")
        print(hash_password(data[1]))
        if name is not None :
            if check_password(name, data[1]):#correct username is Jorge Teixeira and password is 1234, other correct username is Hello World and password is abcd

                print(b"welcome "+ data[0].encode('utf-8'))
            else:
                print("username and password mismatch")
        else:
                print("username and password mismatch")



conn.shutdown(socket.SHUT_RDWR)
conn.close()