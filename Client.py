import socket
import threading
import json

def recieve_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            print(message)
        except:
            print("Disconnected from server")
            break
def send_messages(client_socket, username):
    while True:
        try:
            message = input()
            parts = message.split()
            if len(parts) == 0:
                continue
            if parts[0] == "/private":
                data = {
                    "status": "private",
                    "sender": username,
                    "receiver": parts[1],
                    "text": " ".join(parts[2:])
                }
                client_socket.send(json.dumps(data).encode('utf-8'))
            elif parts[0] == "/group":
                data = {
                    "status": "group",
                    "sender": username,
                    "receiver": parts[1],
                    "text" : " ".join(parts[2:])
                }
                client_socket.send(json.dumps(data).encode('utf-8'))
            elif parts[0] == "/create":
                data = {
                    "status": "create",
                    "sender": username,
                    "receiver": parts[1],
                    "text": " "
                }
                client_socket.send(json.dumps(data).encode('utf-8'))
            elif parts[0] == "/join":
                data = {
                    "status": "join",
                    "sender": username,
                    "receiver": parts[1],
                    "text":" "
                }
                client_socket.send(json.dumps(data).encode('utf-8'))
            elif parts[0] == "/quit":
                data = {
                    "status": "quit",
                    "sender": username,
                    "receiver": "",
                    "text": ""
                }
                client_socket.send(json.dumps(data).encode('utf-8'))
                client_socket.close()
                break
        except:
            print("Error sending message")
            break
def start_client():
    host = "127.0.0.1"
    port = 5555
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    username = input("Enter your username: ")
    registration = {
        "status": "register",
        "sender": username,
        "receiver": "",
        "text":""
    }
    client_socket.send(json.dumps(registration).encode('utf-8'))
    recieve_thread = threading.Thread(target=recieve_messages, args=(client_socket,))
    recieve_thread.start()
    send_thread = threading.Thread(target=send_messages, args=(client_socket, username))
    send_thread.start()
if __name__ == "__main__":
    start_client()