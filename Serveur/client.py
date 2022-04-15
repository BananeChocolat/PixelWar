import socket
from threading import Timer
timeout = 10

ClientMultiSocket = socket.socket()
host = '192.168.246.226' #ip à connecter
port = 12345
print('Waiting for initiate connection')
prompt = "You have %d s to edit \n >> " % timeout

try:
    ClientMultiSocket.connect((host, port))
except socket.error as e:
    print(str(e))

res = ClientMultiSocket.recv(1024)
print('Grille initiale: ' + res.decode())

while True:
    t = Timer(timeout, print, ['Grille non-modifiée ...'])
    t.start()
    answer = input(prompt)
    t.cancel

    if t!=None:
        print(t)
        ClientMultiSocket.send(str.encode(answer))


    res = ClientMultiSocket.recv(1024)
    print(res.decode('utf-8'))
    

ClientMultiSocket.close()