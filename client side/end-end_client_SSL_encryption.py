
import socket
import ssl

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
conn.connect((addr, port))
Username = input("Username")
Password = input("Password")
data = (Username+ ", "+Password)
conn.send(data.encode())



print("Closing connection")
conn.close()