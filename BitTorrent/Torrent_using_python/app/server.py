import socket

Port = 5050
HOST = socket.gethostbyname(socket.gethostname())
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, Port))
server.listen(5)

while True:
    comm, addr = server.accept()
    print(f"connectec to {addr}")
    message = comm.recv(1024) 
    print(f"Message from client: {message}")
    comm.send("Thank you for connecting".encode('utf-8'))
    comm.close()
    print(f"communication ended with {addr}")
              