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
        # print(buffer)
        # print("0")

        if not buffer.startswith('GET') and not buffer.startswith('POST'):
            # print(buffer)
            # print("a")
            response = b'HTTP/1.1 400 Bad Request\r\n'
            response += b'Content-Length: 0\r\n'
            response += b'\r\n'
            client_socket.sendall(response)
            client_socket.close()

        if 'Transfer-Encoding: chunked' in buffer:
            headers = buffer.split('\r\n\r\n')[0]
            buffer = buffer[len(headers) + len('\r\n\r\n'):]
            # print(buffer)
            # print("b")
            while True:
                chunk_length = int(buffer.split('\r\n')[0])
                if chunk_length == 0:
                    chunk = buffer.split('\r\n')[1]
                    if chunk_length == len(chunk):
                        # print(buffer)
                        # print("c")
                        buffer = buffer[len(str(chunk_length)) + 2*len('\r\n') + chunk_length:]
                        response = b'HTTP/1.1 200 OK\r\n'
                        response += b'Content-Length: 13\r\n'
                        response += b'Content-Type: text/plain\r\n'
                        response += b'\r\n'
                        response += b'Hello, World!\r\n'
                        response += b'\r\n'
                        client_socket.sendall(response)
                        client_socket.close()
                        break
                    else:
                        # print(buffer)
                        # print("d")
                        response = b'HTTP/1.1 400 Bad Request\r\n'
                        response += b'Content-Length: 0\r\n'
                        response += b'\r\n'
                        client_socket.sendall(response)
                        client_socket.close()
                        buffer = ''
                        break

                else:
                    chunk = buffer.split('\r\n')[1]
                    if chunk_length == len(chunk):
                        # print(buffer)
                        # print("e")
                        buffer = buffer[len(str(chunk_length)) + 2*len('\r\n') + chunk_length:]
                    else:
                        # print(buffer)
                        # print("f")
                        response = b'HTTP/1.1 400 Bad Request\r\n'
                        response += b'Content-Length: 0\r\n'
                        response += b'\r\n'
                        client_socket.sendall(response)
                        client_socket.close()
                        buffer = ''
                        break
        else:
            response = b'HTTP/1.1 200 OK\r\n'
            response += b'Content-Length: 13\r\n'
            response += b'Content-Type: text/plain\r\n'
            response += b'\r\n'
            response += b'Hello, World!\r\n'
            response += b'\r\n'
            client_socket.sendall(response)
            client_socket.close()
            
if __name__ == '__main__':
    start()