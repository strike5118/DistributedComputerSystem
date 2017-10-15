import master_queue
import json
#config variables
encoding            = "UTF-8"

#common string
END_MESSAGE         = "EOM"

#client commands
NEED_WORK_COMMAND   = "NEED_WORK"
IDENTIFY_SLAVE      = "MY_ID"
RESULTS_STR         = "RESULTS"

#server responses
NO_WORK_COMMAND     = bytes("NO_WORK"  + END_MESSAGE, encoding)
ACCEPTED_COMMAND    = bytes("ACCEPTED" + END_MESSAGE, encoding)

def log(string):
    print("[client_handler.py] "+string)

def getMessage(mySocket):
    message = ""
    while True:
        temp = mySocket.recv(1).decode(encoding)
        
        message += temp
        
        if temp == END_MESSAGE[-1] and END_MESSAGE in message:
            message = message[:-len(END_MESSAGE)]
            log("Message received from client: <" + message + ">")
            return message

class ClientHandler:
    
    def __init__(self,socket):
        self.mySocket = socket
        
        message = getMessage(self.mySocket)
        
        temp = message.split(" ")
        
        if (temp[0] == IDENTIFY_SLAVE):
            try:
                self.id = int(temp[1])
                self.log("Client connected with ID: "+temp[1])
            except:
                self.log("Failed to parse slave id, got=%s" % temp[1])
                raise Exception("Failed to parse slave id, got=%s" % temp[1])
        else:
            self.log("Handshake failed, expected <%s> got <%s>"        % (IDENTIFY_SLAVE,temp[0]))
            raise Exception("Handshake failed, expected <%s> got <%s>" % (IDENTIFY_SLAVE,temp[0]))
        
        self.mySocket.send(ACCEPTED_COMMAND)
        
        self.queueObj = master_queue.getQueue()
        
        self.loop()
        
    def loop(self):
        while True:
            temp = getMessage(self.mySocket)
            
            self.log("Received: " + temp)
            
            message = temp.split(" ")
            
            if message[0] == NEED_WORK_COMMAND:
                work = self.queueObj.getWork(self.id)
                
                if work == None:
                    self.mySocket.send(NO_WORK_COMMAND)
                else:
                    self.working_on = work[0]
                    log("Sending " +str(work[1] + END_MESSAGE))
                    self.mySocket.send(bytes(work[1] + END_MESSAGE,encoding))
            elif message[0] == RESULTS_STR:
                self.queueObj.saveResults(self.working_on,json.loads(message[1]))
                
    def log(self, string):
        print("[ClientHandler] ID="+str(self.id) + ": " +string)