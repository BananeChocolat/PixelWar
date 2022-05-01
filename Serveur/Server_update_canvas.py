import socket
import threading
import hashlib
import time




clients = []

clients_lock = threading.Lock()
host = '192.168.0.54'
port = 12345

s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((host,port))
s.listen(3)
th = []


def get_hash():
    
    BUF_SIZE = 1024 #taille du buffer -> arbitraire
    md5 = hashlib.md5()
    
    with open('canvas.txt', 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            md5.update(data)
            
    return md5.hexdigest()

client_count=0

def listener(client, address):
    
    global client_count
    
    print("Accepted connection from: ", address)
    
    file=open('canvas.txt','r')
    read_file=file.read() 
    
    with clients_lock:
        clients.append(client)
        client_count+=1
    
    # client.sendall(f'Grille initiale : {read_file}'.encode())
    client.sendall(f'{read_file}'.encode())
    file.close()
      
    
    try:
        while True:
            
            
            hash_initial=get_hash()
            time.sleep(0.1)
            #print(f'[DEBUG] : [hash_initial] : {hash_initial} | [hash_actuel] : {get_hash()}')
            while hash_initial != get_hash():
                
                
                file=open('canvas.txt','r')
                read_file=file.read() 
                with clients_lock:
                    for i in range(client_count):
            
                        # print(f'[DEBUG] : sending to {c}')
                        # clients[i].sendall(f'Grille modifiée : {read_file} | Clients : {client_count}'.encode())
                        clients[i].sendall(f'{read_file}'.encode())
                        
                file.close()
                hash_initial=get_hash()
            
    finally:
        with clients_lock:
            clients.pop(client)
            client.close()
            client_count-=1
            



while True:
    print("Server is listening for connections...")
    client, address = s.accept()
    th.append(threading.Thread(target=listener, args = (client,address)).start())

s.close()