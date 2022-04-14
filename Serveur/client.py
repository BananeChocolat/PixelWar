import socket
ClientMultiSocket = socket.socket()
host = '192.168.0.54'
port = 12345
print('Waiting for connection response')
try:
    ClientMultiSocket.connect((host, port))
except socket.error as e:
    print(str(e))
res = ClientMultiSocket.recv(1024)
print('Grille initiale: ' + res.decode())
while True:
    
    res = ClientMultiSocket.recv(1024)
    print(res.decode('utf-8'))
    Input = input('Hey there: ')
    ClientMultiSocket.send(str.encode(Input))
ClientMultiSocket.close()