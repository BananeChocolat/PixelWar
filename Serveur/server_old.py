import socket
import pickle




original=[0,0,0,0,0,0,0,0,0,0]
updated= [0,0,0,0,0,0,0,0,0,0]

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('localhost', 10000)
print('starting up ')
sock.bind(server_address)


sock.listen(1)

while True:
   
    print('waiting for a connection')
    connection, client_address = sock.accept()
    
    try:
        print('connection from', client_address)
        connection.sendall(pickle.dumps(updated))

        # Receive the data in small chunks and retransmit it
        while True:
            data = connection.recv(4096)
            data2= pickle.loads(data)
            updated=data2
            print(f'update is now {updated}')
            print('received "%s"' % data2)
            if data:
                # updated=updated
                print('sending data back to the client')
                connection.sendall(pickle.dumps(updated))
                break
            else:
                print ('no more data from', client_address)
                break
    finally:
        
        connection.close()