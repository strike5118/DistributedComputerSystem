import socket
import client_handler
from threading import Thread

def log(string):
    print("[server.py]: "+string)
   
def loop():   
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    serversocket.bind(("127.0.0.1", 6969))
    log("Creating server on %s:%d" % ("127.0.0.1",6969))
    serversocket.listen(5)

    while True:
        (clientsocket, address) = serversocket.accept()
        
        log("Client has connected from %s:%d" % (address[0],address[1]))
        
        thread = Thread(target = newClient,args=(clientsocket, address))
        thread.daemon = True
        thread.start()
        

def newClient(soc,address):
    client_handler.ClientHandler(soc)
    
thread = Thread(target = loop)
thread.daemon = True
thread.start()

import library
library.main()