"""
Docstring for server

- This is a simple HTTPS server using Python's built-in http.server module.
- It serves files from the current directory over HTTPS.
- Make sure to have a valid SSL certificate (server.pem) in the same directory.

- To run the server, execute this script. Access it via a web browser at:
  https://<server_ip>:<port> (e.g., https://192.168.1.209:8000)
  It is used to run the frontend of the application.

  To run it locally in your terminal, use:
    python3 -m server_fe.py
"""


# Import livraries
import http.server
import ssl


#server_address =('0.0.0.0', 5000)
server_address =('192.168.1.209', 8000)
httpd = http.server.HTTPServer(server_address, http.server.SimpleHTTPRequestHandler)

# Create SSL context
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain('server.pem') 

# Wrap the socket
httpd.socket = context.wrap_socket(httpd.socket, server_side=True)

print(f"Serving on https://{server_address[0]}:{server_address[1]}")
httpd.serve_forever()
