import socket


ClientMultiSocket = socket.socket()
host = '192.168.0.54' #ip à connecter
port = 12345
print('Waiting for initiate connection')


try:
    ClientMultiSocket.connect((host, port))
except socket.error as e:
    print(str(e))



while True:

    res = ClientMultiSocket.recv(1024)      
    print(res.decode('utf-8'))
    

ClientMultiSocket.close()