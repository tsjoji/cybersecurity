
import socket
import ssl
import random
import base64

def encode(key, clear):
    word=''
    temp=list(clear)
    for i in range(len(temp)):
        word=word+chr(ord(temp[i])+key)
    return word

def decode(key, enc):
    word=''
    temp=list(enc)
    for i in range(len(temp)):
        word=word+chr(ord(temp[i])-key)
    print(word)
    return word



spinlocker2=0
def startKeyExchange(buffered):
    Shared_base = 8
    Shared_Prime = 19
    session = buffered[0:20]
    secret_key = random.randint(1, 10)
    friend_secret_key=-1
    if(str(buffered)[2]=='1'):
        while 1:
            buffer = b''
            data = conn.recv(4096)
            if data:
                buffer += data
            else:
                # this is going to be the friends list return part
                print("error")
            break;
        secret_num=(Shared_base**secret_key)%Shared_Prime
        number = str(secret_num)

        conn.send(number.encode())
        buffer=b''
        while 1:
            buffer = b''
            data = conn.recv(4096)
            if data:
                buffer += data
            else:
                # this is going to be the friends list return part
                print("error")
            break;
        SharedSecret=(int(buffer.decode()[2:-1]) ** secret_key) % Shared_Prime

        message="A Plan to Turn New York Into a Capital of Cybersecurity"
        enc=encode(SharedSecret,message)
        print(enc)
        conn.send(str(enc).encode())
    else:
        while 11:
            buffer = b''
            data = conn.recv(4096)
            if data:
                buffer += data
            else:
                # this is going to be the friends list return part
                print("error")
            break
        secret_num = (Shared_base ** secret_key) % Shared_Prime
        friend_secret_key = int(buffer.decode()[2:-1])
        print(str(friend_secret_key) + "is friend")
        SharedSecret = (friend_secret_key ** secret_key) % Shared_Prime
        number = str(secret_num)
        print(number)
        print(SharedSecret)
        conn.send(number.encode())
        while 1:
            buffer = b''
            data = conn.recv(4096)
            if data:
                buffer += data
            else:
                # this is going to be the friends list return part
                print("error")
            break
        print(buffer)
        while 1:
            buffer = b''
            data = conn.recv(4096)
            if data:
                buffer += data
            else:
                # this is going to be the friends list return part
                print("error")
            break
        decode(SharedSecret,buffer.decode())

addr = '127.0.0.1'
port = 8080
hostname = 'jbt8.com'
server_data = ssl.get_server_certificate(('localhost', 4443))
c_cert = 'client.crt'
c_key = 'client.key'
f=open('server.crt', 'w')
f.write(server_data)
f.close()
s_cert = 'server.crt'
context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile=s_cert)
context.load_cert_chain(certfile=c_cert, keyfile=c_key)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn = context.wrap_socket(s, server_side=False, server_hostname=hostname)
try:
    conn.connect((addr, port))
except:
    conn.connect((addr,port+1))
Username = input("Username ")
Password = input("Password ")
data = (Username+ ", "+Password)
conn.send(data.encode())
while 1:
    buffer = b''
    data = conn.recv(4096)
    if data:
        buffer += data
    else:
        # this is going to be the friends list return part
        break
    print(buffer)
    break
startKeyExchange(buffer)

print("Closing connection")
conn.close()