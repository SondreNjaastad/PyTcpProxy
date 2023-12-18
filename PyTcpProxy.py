import socket
import threading
import argparse
import datetime
from systemd import journal

LISTEN_PORT = 5000
TARGET_SERVER = None
TARGET_PORT = None
LOG_TO_TERMINAL = False
LOG_TO_SYSTEMD = False

def log(message):
    if LOG_TO_TERMINAL:
        print(message)
    if LOG_TO_SYSTEMD:
        journal.send(message)

def parse_args():
    global LISTEN_PORT, TARGET_SERVER, TARGET_PORT, LOG_TO_TERMINAL, LOG_TO_SYSTEMD

    parser = argparse.ArgumentParser(description="TCP Proxy")
    parser.add_argument("--listen-port", type=int, default=5000, help="Port to listen on")
    parser.add_argument("--target-server", type=str, required=True, help="Target server IP")
    parser.add_argument("--target-port", type=int, required=True, help="Target server port")
    parser.add_argument("--log-to-terminal", action='store_true', help="Enable logging to terminal")
    parser.add_argument("--log-to-systemd", action='store_true', help="Enable logging to systemd")
    
    args = parser.parse_args()
    LISTEN_PORT = args.listen_port
    TARGET_SERVER = args.target_server
    TARGET_PORT = args.target_port
    LOG_TO_TERMINAL = args.log_to_terminal
    LOG_TO_SYSTEMD = args.log_to_systemd

def log_data(session_id, direction, data):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(f"{session_id}.log", "a") as log_file:
        message = f"{timestamp} {direction} {data.hex()} | {data.decode('ascii', errors='replace')}"
        log(message)
        log_file.write(f"{message}\n")

def relay_data(source, destination, session_id, direction):
    while True:
        data = source.recv(4096)
        if not data:
            log(f"Session {session_id}: {direction} connection disconnected.")
            break
        destination.sendall(data)
        log_data(session_id, direction, data)

def handle_client(client_socket, session_id):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.connect((TARGET_SERVER, TARGET_PORT))

    client_thread = threading.Thread(target=relay_data, args=(client_socket, server_socket, session_id, "C->S"))
    server_thread = threading.Thread(target=relay_data, args=(server_socket, client_socket, session_id, "S->C"))

    client_thread.start()
    server_thread.start()

    client_thread.join()
    server_thread.join()

    client_socket.close()
    server_socket.close()

def main():
    parse_args()
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.bind(('', LISTEN_PORT))
    listener.listen(5)

    log(f"Listening on port {LISTEN_PORT}...")

    session_id = 0
    while True:
        client_socket, addr = listener.accept()
        log(f"Session {session_id}: Accepted connection from {addr}")
        session_id += 1
        threading.Thread(target=handle_client, args=(client_socket, session_id)).start()

if __name__ == "__main__":
    main()
