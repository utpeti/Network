#Korpos Botond 522

import socket
import threading
import os

FILES_PATH = os.path.abspath(os.getcwd())

HOST = "localhost"
PORT = 3000
BUFFER_SIZE = 1024
TIMEOUT = 5.0

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.listen(5)

def log_with_thread_id(message):
    thread_id = threading.get_ident()
    print(f"[Thread {thread_id}] {message}")

def get_mime_type(filename):
    if filename.endswith(".html"):
        return "text/html"
    elif filename.endswith(".css"):
        return "text/css"
    elif filename.endswith(".jpg") or filename.endswith(".jpeg"):
        return "image/jpeg"
    elif filename.endswith(".png"):
        return "image/png"
    else:
        return "application/octet-stream"

def handle_client(client_socket):
    print("Connection opened on " + str(threading.get_ident()) + "\n\n")
    run = True
    client_socket.settimeout(5.0)

    while run:
        try:            
            request = client_socket.recv(BUFFER_SIZE).decode()

            if (len(request) == 0):
                run = False

            request_lines = request.split("\n")
            request_type, file_path, _ = request_lines[0].split(" ")

            if request_type == "GET" and "HTTP/1.1" in request_lines[0]:
                filename = file_path.strip("/").replace("/", "\\")
                file_path = os.path.join(FILES_PATH, filename)
                file_path = os.path.join(FILES_PATH, filename)

                log_with_thread_id("Received request: " + filename)

                if os.path.exists(file_path):
                    with open(file_path, "rb") as file:
                        content = file.read()
                    mime_type = get_mime_type(file_path)
                    response = f"HTTP/1.1 200 OK\nContent-Type: {mime_type}\nContent-Length: {len(content)}\nConnection: keep-alive\n\n".encode() + content
                else:
                    response = "HTTP/1.1 404 Not Found\nContent-Length: 14\nConnection: close\n\nFile not found".encode()
                    run = False

            client_socket.sendall(response)

            if "Connection: close" in request:
                run = False
            
        except TimeoutError:
            run = False
        
    client_socket.close()
    print("Connection closed on " + str(threading.get_ident()) + "\n\n")
        

print(f"Server listening on {HOST}:{PORT}")

try:
    while True:
        client_socket, address = server_socket.accept()
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()
except KeyboardInterrupt:
    print("Server shutdown.")
finally:
    server_socket.close()
