import socket
import pickle

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 10000)
print('connecting to %s port %s' % server_address)
sock.connect(server_address)


try:
    #Récupère la grille actuelle
    grille_actuelle=sock.recv(4096)
    grille_actuelle=pickle.loads(grille_actuelle)
    print(f'grille actuelle: {grille_actuelle}')
    
    a=int(input('Quel numéro de case voulez-vous modifier? '))
    message=grille_actuelle
    message[a]=1
    
    
    # Send data
    print('sending : %s' % message)
    sock.sendall(pickle.dumps(message))

    # Look for the response
    amount_received = 0
    amount_expected = 10
    
    while amount_received < amount_expected:
        data = sock.recv(4096)
        data=pickle.loads(data)
        amount_received += len(data)
        print ( 'received : %s' % data)

finally:
    print('closing socket')
    sock.close()