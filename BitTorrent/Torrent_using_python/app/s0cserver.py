import socket
import struct

# Constants for message IDs
CHOKE = 0
UNCHOKE = 1
INTERESTED = 2
NOT_INTERESTED = 3
REQUEST = 6
PIECE = 7

def send_message(sock, message_id, payload=b''):
    """Send a message to the peer."""
    message = struct.pack('>I', len(payload) + 1) + struct.pack('B', message_id) + payload
    sock.sendall(message)

def handle_client_connection(client_socket):
    """Handle the connection from a client."""
    try:
        while True:
            # Read the length prefix
            length_prefix = recv_all(client_socket, 4)
            length = struct.unpack('>I', length_prefix)[0]
            
            # Read the message ID and payload
            message_id = recv_all(client_socket, 1)[0]
            payload = recv_all(client_socket, length - 1)
            
            print(f"Received message: Length: {length}, ID: {message_id}, Payload: {payload.hex()}")

            if message_id == REQUEST:
                # If the message ID is REQUEST, send an UNCHOKE message
                print("Received REQUEST message, sending UNCHOKE message")
                send_message(client_socket, UNCHOKE)
                
            elif message_id == INTERESTED:
                # Example: Handle INTERESTED message
                print("Received INTERESTED message")
                # You can implement additional logic here

    except (socket.timeout, ConnectionError) as e:
        print(f"Connection error: {e}")
    finally:
        client_socket.close()

def recv_all(sock, length):
    """Receive a specific amount of data from the socket."""
    data = b''
    while len(data) < length:
        chunk = sock.recv(length - len(data))
        if not chunk:
            raise ConnectionError("Failed to receive data")
        data += chunk
    return data

def start_server():
    """Start the server to listen for incoming connections."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((socket.gethostbyname(socket.gethostname()), 5050))
        server_socket.listen(5)
        print(f"Server listening on {socket.gethostbyname(socket.gethostname())}:{5050}")

        while True:
            client_socket, addr = server_socket.accept()
            print(f"Accepted connection from {addr}")
            handle_client_connection(client_socket)

if __name__ == "__main__":
    start_server()
