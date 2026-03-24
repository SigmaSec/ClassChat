import socket
import threading
import json

host = "0.0.0.0"
port = 5555
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((host, port))
server_socket.listen()

users = {}
rooms = {}
locked = threading.Lock()

def handle_client(client_socket):
    data = client_socket.recv(1024).decode('utf-8')
    message = json.loads(data)
    username = message["sender"]
    with locked:
        users[username] = client_socket
    while True:
        data = client_socket.recv(1024).decode('utf-8')
        message = json.loads(data)
        recipient = message["reciever"]
        if recipient in users:
            users[recipient].send(f"This room is private(?)".encode('utf-8'))
        else:
            client_socket.send("User not found".encode('utf-8'))
        elif message["status"] == "group":
            room_name = message["receiver"]
            if room_name in rooms:
                for member in rooms[room_name]:
                    users[member].send(f"{message['sender']} [{room_name}]: {message['text']}".encode('utf-8'))
            else:
                client_socket.send("Room unable to create")
        elif message["status"] == "create":
            room_name = message["receiver"]
            if room_name not in rooms:
                with locked: 
                    rooms[room_name] = [username]
                client_socket.send("Room created sucessfully".encode('utf-8'))
            else:
                client_socket.send("Room already exists".encode('utf-8'))
        elif message["status"] == "join":
            room_name = message["receiver"]
            if room_name in rooms:
                with locked:
                    rooms[room_name].append(username)
                client_socket.send("Joined room sucessfully".encode('utf-8'))
            else:
                client_socket.send("Failed to join room".encode('utf-8'))
        elif message["status"] == "quit":
            with locked:
                del users[username]
            break

def start_server():
    print(f"listening for connection on port {port}")
    while True:
        client_socket, address = server_socket.accept()
        thread = threading.Thread(target=handle_client, args=(client_socket,))
        thread.start()