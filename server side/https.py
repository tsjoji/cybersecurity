import http.server
import ssl

site = http.server.HTTPServer(('127.0.0.1', 4443), http.server.SimpleHTTPRequestHandler)

site.socket = ssl.wrap_socket (site.socket, certfile='server.pem', server_side=True)

site.serve_forever()