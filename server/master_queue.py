from threading import Lock
queueObj = None

def log(string):
    print("[master_queue.py] " +string)

class MyQueue:
    def __init__(self):
        self.myQueue    = [] # List of (work_id,workObj) pairs
        self.inProgress = {} # map of work_id to (workObj,slave_id) pairs
        self.idCounter  = 0  
        self.complete   = {} # map of work_id to (results) pairs
        
        self.inProgressLock = Lock()
        self.completeLock   = Lock()
        self.queueLock      = Lock()
       
    def add(self,toAdd):
        self.idCounter += 1
        log("Creating work id <%d>" % self.idCounter)
        self.queueLock.acquire()
        self.myQueue.append((self.idCounter,toAdd))
        self.queueLock.release()
        return self.idCounter
    
    def getWork(self, slave_id):
        self.queueLock.acquire()
        
        if len(self.myQueue) > 0:
            temp = self.myQueue[0]
            
            self.inProgressLock.acquire()
            self.inProgress[temp[0]] = (temp[1],slave_id)
            self.inProgressLock.release()
            
            del self.myQueue[0]
            
           
            self.queueLock.release()
            log("Given work id <%d> to slave=<%d>" % (temp[0],slave_id))
            return temp
        else:
            self.queueLock.release()
            return None

    def saveResults(self,work_id,results):
        log("Saving <" + str(results) + "> for work_id = <%d>" % work_id)
        self.inProgressLock.acquire()
        self.completeLock.acquire()
        self.complete[work_id] = results
        
        del self.inProgress[work_id]
        
        self.inProgressLock.release()
        self.completeLock.release()
        
    def getResult(self,work_id,no_response):
        self.completeLock.acquire()
        
        temp = self.complete.get(work_id,no_response)
        
        self.completeLock.release()
        return temp
        
def getQueue():
    global queueObj

    if queueObj:
        return queueObj
    else:
        queueObj = MyQueue()
    return getQueue()