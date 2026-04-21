import socket
import threading
import json

def recieve_messages(client_socket):
    while True:
        message = client_socket.recv(1024).decode('utf-8')
        parts = message.split()

        if parts[0] == "/private":
            data = {
                "status": "private"
                "sender": username
                "receiver": parts[1]
                "text": " ".join(parts[2:])
            }
            client_socket.send(json.dumps(data).encode('utf-8'))
        if parts[1] == "/group":
            data = {
                "status":
            }
        if parts[2] == "/create":
        if parts[3] == "/join":
        if parts[4] == "/quit":
        print(message)
def send_messages(client_socket, username):
    while True:
        message = input()
