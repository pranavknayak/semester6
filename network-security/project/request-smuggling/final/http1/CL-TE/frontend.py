import socket

def start():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 8080))
    server_socket.listen(1)

    while True:
        client_socket, client_addr = server_socket.accept()
        data = client_socket.recv(4096)
        request = data.decode('utf-8')
        if not request.startswith('GET') and not request.startswith('POST'):
            client_socket.close()
            continue

        if 'Content-Length' in request:
            content_length = int(request.split('Content-Length: ')[1].split('\r\n')[0])
            first_pos = request.find("\r\n\r\n")
            last_pos = request.rfind("\r\n\r\n")
            payload = request[first_pos + len("\r\n\r\n"):last_pos]
            if content_length != len(payload):
                # print(content_length, payload, len(payload))
                print("request not forwarded")
                client_socket.close()
                continue
        print("request forwarded")
        # print(data)
        backend_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        backend_socket.connect(('localhost', 8081))
        backend_socket.sendall(data)

        data = backend_socket.recv(4096)
        client_socket.sendall(data)
        print("response forwarded")
        
        backend_socket.close()
        client_socket.close()

if __name__ == '__main__':
    start()