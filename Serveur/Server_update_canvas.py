import socket
import threading
import hashlib
import time




clients = set()
clients_lock = threading.Lock()
host = '192.168.0.54'
port = 12345

s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((host,port))
s.listen(3)
th = []


def get_hash():
    # BUF_SIZE is totally arbitrary, change for your app!
    BUF_SIZE = 1024 # lets read stuff in 64kb chunks!
    md5 = hashlib.md5()
    
    with open('canvas.txt', 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            md5.update(data)
            
    return md5.hexdigest()





def listener(client, address):
    print("Accepted connection from: ", address)
    
    file=open('canvas.txt','r')
    read_file=file.read() 
    
    with clients_lock:
        clients.add(client)
    
    client.sendall(f'Grille initiale : {read_file.encode()}'.encode())
    file.close()
      
    
    try:
        
        while True:
            hash_initial=get_hash()
            while hash_initial != get_hash():
                time.sleep(0.1)
                print('DEBUG : Grille modifiée')
                file=open('canvas.txt','r')
                read_file=file.read() 
                with clients_lock:
                    for c in clients:
                        c.sendall(f'Grille modifiée : {read_file}'.encode())
                
                file.close()
                hash_initial=get_hash()
            
    finally:
        with clients_lock:
            clients.remove(client)
            client.close()



while True:
    print("Server is listening for connections...")
    client, address = s.accept()
    th.append(threading.Thread(target=listener, args = (client,address)).start())

s.close()