import socket
import threading


clients = set()
clients_lock = threading.Lock()
host = '192.168.246.226'
port = 12345

s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((host,port))
s.listen(3)
th = []


def listener(client, address):
    print("Accepted connection from: ", address)
    with clients_lock:
        clients.add(client)
    client.sendall('Grille initiale'.encode())
    file=open('canvas.txt','r')
    read_file=file.read() 
    compteur=0
    try:    
        while True:
            file2=open('canvas.txt','r')
            if file2.read()!=read_file:
                compteur+=1
                print(f'Changement [{compteur}] détecté : sending to client ...')
                with clients_lock:
                    for c in clients:
                        c.sendall('List updated'.encode())
            file=open('canvas.txt','r')
            read_file=file.read()
    finally:
        with clients_lock:
            clients.remove(client)
            client.close()



while True:
    print("Server is listening for connections...")
    client, address = s.accept()
    th.append(threading.Thread(target=listener, args = (client,address)).start())

s.close()