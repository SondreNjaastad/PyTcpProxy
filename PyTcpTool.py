import socket
import threading
import argparse
import datetime

def parse_args():
    parser = argparse.ArgumentParser(description="TCP Proxy")
    parser.add_argument("--listen-port", type=int, default=5000, help="Port to listen on")
    parser.add_argument("--target-server", type=str, required=True, help="Target server IP")
    parser.add_argument("--target-port", type=int, required=True, help="Target server port")
    return parser.parse_args()

def log_data(session_id, direction, data):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(f"{session_id}.log", "a") as log_file:
        log_file.write(f"{timestamp} {direction} {data.hex()} | {data.decode('ascii', errors='replace')}\n")

def relay_data(source, destination, session_id, direction):
    while True:
        data = source.recv(4096)
        if not data:
            break
        destination.sendall(data)
        log_data(session_id, direction, data)

def handle_client(client_socket, args, session_id):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.connect((args.target_server, args.target_port))

    client_thread = threading.Thread(target=relay_data, args=(client_socket, server_socket, session_id, "C->S"))
    server_thread = threading.Thread(target=relay_data, args=(server_socket, client_socket, session_id, "S->C"))

    client_thread.start()
    server_thread.start()

    client_thread.join()
    server_thread.join()

    client_socket.close()
    server_socket.close()

def main():
    args = parse_args()
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.bind(('', args.listen_port))
    listener.listen(5)

    print(f"Listening on port {args.listen_port}...")

    session_id = 0
    while True:
        client_socket, addr = listener.accept()
        print(f"Accepted connection from {addr}")
        session_id += 1
        threading.Thread(target=handle_client, args=(client_socket, args, session_id)).start()

if __name__ == "__main__":
    main()
