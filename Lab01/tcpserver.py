#Korpos Botond 522

from socket import *

serverPort = 3000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)
print("SERVER: Ready to receive")

while True:
    connectionSocket, addr = serverSocket.accept()
    sentence = connectionSocket.recv(1024).decode()
    if sentence == "exit":
        print("SERVER: Closed")
        connectionSocket.close()
        break
    capitalizedSentence = sentence.upper()
    connectionSocket.send(capitalizedSentence.encode())
    connectionSocket.close()