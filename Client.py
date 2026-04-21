import socket
import threading
import json

def recieve_messages(client_socket):
    while True:
        message = client_socket.recv(1024).decode('utf-8')
        print(message)
def send_messages(client_socket, username):
    while True:
        message = input()



#client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#client_socket.connect((host, port))
