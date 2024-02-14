import http.server
import socketserver
import os

if __name__ == "__main__":
    # Define the directory you want to serve files from
    directory_to_serve = 'files'

    # Change the current working directory to the directory you want to serve files from
    os.chdir(directory_to_serve)

    # Create a Handler object using http.server.SimpleHTTPRequestHandler
    Handler = http.server.SimpleHTTPRequestHandler

    # Define the server address and port
    server_address = ('', 8009)  # Serve on all addresses, port

    # Create a TCPServer object
    httpd = socketserver.TCPServer(server_address, Handler)

    # Start the server
    print(f"Serving files from the directory {directory_to_serve} at http://localhost:8009")
    httpd.serve_forever()