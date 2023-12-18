# PyTcpProxy

`PyTcpProxy` is a lightweight, Python-based TCP proxy tool designed for debugging and monitoring TCP traffic. It allows users to listen to a specified port, forward traffic to a target server, and log the traffic in a human-readable format. The tool is especially useful for developers and network administrators who need to debug or analyze the communication between a client and a server.

## Features

- **Configurable Listening Port**: Set up a listening port as a startup parameter.
- **Target Server and Port Specification**: Forward traffic to a specified server and port.
- **Traffic Logging**: Log both the raw bytes and ASCII interpretation of the traffic.
- **Separate Log Files**: Option to create individual log files for each connection.
- **Timestamps and Traffic Direction**: Each log entry includes a timestamp and the direction of the traffic.

## Installation

To use `PyTcpProxy`, you need Python installed on your system. Clone this repository to your local machine using:

```bash
git clone https://github.com/SondreNjaastad/PyTcpProxy.git
```

Navigate to the cloned directory:

```bash
cd PyTcpProxy
```

## Usage

Run `PyTcpProxy` with the following command:

```bash
python tcp_proxy.py --listen-port [LISTEN_PORT] --target-server [TARGET_SERVER_IP] --target-port [TARGET_SERVER_PORT]
```

- Replace `[LISTEN_PORT]` with the port you want to listen on.
- Replace `[TARGET_SERVER_IP]` with the IP address of the target server.
- Replace `[TARGET_SERVER_PORT]` with the port of the target server.

## Configuration

You can configure `PyTcpProxy` using command-line arguments:

- `--listen-port`: Port to listen on (default: 5000).
- `--target-server`: IP address of the target server.
- `--target-port`: Port number of the target server.

## Logs

Logs are stored in the same directory as the script, with each connection's log saved in a separate file named with the session ID.

## Contributions

Contributions to `PyTcpProxy` are welcome. Please ensure that your code adheres to the project's style and quality standards.

## License

This project is licensed under the [MIT License](LICENSE).