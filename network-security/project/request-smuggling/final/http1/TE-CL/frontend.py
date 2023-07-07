import socket

def start():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 8080))
    server_socket.listen(1)

    while True:
        client_socket, client_addr = server_socket.accept()
        data = client_socket.recv(4096)
        # print(data)
        request = data.decode('utf-8')
        if not request.startswith('GET') and not request.startswith('POST'):
            client_socket.close()
            continue

        if 'Transfer-Encoding: chunked' in request:
            first_pos = request.find("\r\n\r\n")
            payload = request[first_pos + len("\r\n\r\n"):]
            while True:
                chunk_length = int(payload.split('\r\n')[0])
                if chunk_length == 0:
                    chunk = payload.split('\r\n')[1]
                    if chunk_length == len(chunk):
                        payload = payload[len(str(chunk_length)) + 2*len('\r\n') + chunk_length:]
                        backend_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        backend_socket.connect(('localhost', 8081))
                        backend_socket.sendall(data)
                        print("request forwarded")
                        res_data = backend_socket.recv(4096)
                        client_socket.sendall(res_data)
                        print("response forwarded")
                        client_socket.close()
                        break
                    else:
                        print("request not forwarded")
                        client_socket.close()
                        break
                else:
                    chunk = payload.split('\r\n')[1]
                    if chunk_length == len(chunk):
                        payload = payload[len(str(chunk_length)) + 2*len('\r\n') + chunk_length:]
                    else:
                        print("request not forwarded")
                        client_socket.close()
                        break
        else:
            print("request forwarded")
            backend_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            backend_socket.connect(('localhost', 8081))
            backend_socket.sendall(data)
            res_data = backend_socket.recv(4096)
            client_socket.sendall(res_data)
            print("response forwarded")
            client_socket.close()

if __name__ == '__main__':
    start()