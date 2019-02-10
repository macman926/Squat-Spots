#!/usr/bin/python3

import http.server
import socketserver
import ssl

#ssl_ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
#ssl_ctx.load_cert_chain('cert.crt', 'cert.pem')

PORT = 65432
handler = http.server.SimpleHTTPRequestHandler

httpd = socketserver.TCPServer(('', PORT), handler)
sock = httpd.socket
#SSLCertificateFile      /etc/letsencrypt/live/www.squatspots.org/fullchain.pem
#SSLCertificateKeyFile /etc/letsencrypt/live/www.squatspots.org/privkey.pem

ssl_sock = ssl.wrap_socket(sock,
                           certfile='/etc/letsencrypt/live/www.squatspots.org/fullchain.pem',
                           keyfile ='/etc/letsencrypt/live/www.squatspots.org/privkey.pem',
                           server_side=True, cert_reqs=ssl.CERT_NONE)
httpd.socket = ssl_sock

print('Serving at', PORT)
httpd.serve_forever()
