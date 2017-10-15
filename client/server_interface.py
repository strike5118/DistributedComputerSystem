import socket 
import json

#config variables
masterIP            = "127.0.0.1"
masterPort          = 6969
slaveID             = 0
encoding            = "UTF-8"

#common string
END_MESSAGE         = "EOM"
RESULTS_STR         = "RESULTS" 

#client commands
NEED_WORK_COMMAND   = bytes("NEED_WORK"                + END_MESSAGE ,encoding)
IDENTIFY_SLAVE      = bytes("MY_ID "    + str(slaveID) + END_MESSAGE ,encoding)

#server responses
NO_WORK_COMMAND     = "NO_WORK"


mySocket = None


def getMessage(mySocket):
    message = ""
    while True:
        try:
            temp = mySocket.recv(1).decode(encoding)
        except:
            log("Failed to read from server")
            return None
            
        message += temp
        
        if temp == END_MESSAGE[-1] and END_MESSAGE in message:
            message = message[:-len(END_MESSAGE)]
            log("Message received from client: <" + message + ">")
            return message

def connect():
    global mySocket
    
    mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    log("Attempting to connect to %s:%d" % (masterIP,masterPort))
    mySocket.connect((masterIP,masterPort))
    
    mySocket.send(IDENTIFY_SLAVE)
    getMessage(mySocket)
    
def getWork():
    global mySocket
    
    if not mySocket: # connect if not connected
        try:
            connect()
        except Exception as e:
            log("Failed to connect to master node: <" + str(e)+">")
            mySocket = None #force reconnect next time we try to connect
            return None
    
    try:
        err = mySocket.send(NEED_WORK_COMMAND)
    except:
        log("Failed to send info to server")
        mySocket = None #force reconnect next time we try to connect
        return None
    
    temp = getMessage(mySocket)
    
    if temp == None: 
        mySocket = None #force reconnect next time we try to connect
        return None
    
    try:
        recieved = temp.split(' ')

        if recieved[0] == NO_WORK_COMMAND:
            return None
        else:
            function = int(recieved[0])

            args     = json.loads(" ".join(recieved[1:])) # re join rest of list 
            
            return (function,args)
    except Exception as e:
        log("Failed to parse arguments from server: <"+str(e) + ">")
        mySocket = None #force reconnect next time we try to connect
        return None
            
    
def reportResults(results):
    global mySocket
    toReport = json.dumps(results)
    try:
        mySocket.send(bytes(RESULTS_STR + " " + toReport + END_MESSAGE ,encoding))
    except:
        mySocket = None #force reconnect next time we try to connect
        log("Failed to send results to server")
        
def log(string):
    print("[server_interface.py]: " + string)