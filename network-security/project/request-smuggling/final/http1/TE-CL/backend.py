import socket
def start():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 8081))
    server_socket.listen(1)

    buffer = ''

    while True:
        client_socket, client_addr = server_socket.accept()
        print("received request")
        data = client_socket.recv(4096)
        request = data.decode('utf-8')
        buffer += request
        
        if not buffer.startswith('GET') and not buffer.startswith('POST'):
            response = b'HTTP/1.1 400 Bad Request\r\n'
            response += b'Content-Length: 0\r\n'
            response += b'\r\n'
            client_socket.sendall(response)
            client_socket.close()
            continue

        if 'Content-Length' in request:
            headers = buffer.split('\r\n\r\n')[0]
            buffer = buffer[len(headers) + len('\r\n\r\n'):]
            content_length = int(request.split('Content-Length: ')[1].split('\r\n')[0])
            buffer = buffer[content_length:]
            response = b'HTTP/1.1 200 OK\r\n'
            response += b'Content-Length: 13\r\n'
            response += b'Content-Type: text/plain\r\n'
            response += b'\r\n'
            response += b'Hello, World!\r\n'
            response += b'\r\n'
            client_socket.sendall(response)
            client_socket.close()
            continue
        else:
            response = b'HTTP/1.1 200 OK\r\n'
            response += b'Content-Length: 13\r\n'
            response += b'Content-Type: text/plain\r\n'
            response += b'\r\n'
            response += b'Hello, World!\r\n'
            response += b'\r\n'
            client_socket.sendall(response)
            client_socket.close()
            continue


if __name__ == '__main__':
    start()