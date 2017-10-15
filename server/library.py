import json
import master_queue
import uuid
import time

myQueue = master_queue.getQueue()

function_ids = {"identity":0,"det":1}

def log(string):
    print("[library.py] "+str(string))

def add(function,args):
    return myQueue.add(str(function) + " " + json.dumps(args))

def waitForResponse(work_id,timeout=60):
    
    guid = uuid.uuid4()
    while True:
        temp = myQueue.getResult(work_id,guid)
        
        if (temp != guid):
            return temp
        else:
            time.sleep(timeout)

def identity(args):
    '''
    Basic identity function, returns what was passed to it
    sends args to a client
    '''
    
    event = add(function_ids["identity"],args)
    
    return waitForResponse(event)

def wait_for_matrix(matrix,timeout=60):
    '''
    '''
    got = []
    guid = uuid.uuid4()
    for i in matrix:
        newList = []
        got.append(newList)
        for j in i:
            newList.append(False)
            
    finished = False
    while not finished:
        finished = True
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                if not got[i][j]:
                    temp = myQueue.getResult(matrix[i][j],guid)
                    if temp != guid:
                        log("temp is <"+str(temp)+">")
                        matrix[i][j] = temp
                        got[i][j] = True
                    else:
                        finished = False
        if not finished:
            time.sleep(timeout)
    return matrix
    
    
def inverse(matrix):
    '''
    '''
    det = waitForResponse(add(function_ids["det"],matrix),timeout=1)
    
    eventMatrix = []
    for i,row in enumerate(matrix):
        eventMatrix.append([])
        for j,value in enumerate(row):
            newMatrix = []
            
            
            
            for i2 in range(len(matrix)):
                if i2 != i:
                    newMatrix.append([])
                    for j2,value2 in enumerate(matrix[i2]):
                        if j2 != j:
                            newMatrix[-1].append(value2)
            
            eventMatrix[-1].append(add(function_ids["det"],newMatrix))
            
            
    wait_for_matrix(eventMatrix,timeout=5)
    inverse = []
    
    print(eventMatrix)
    
    
    for i,row in enumerate(eventMatrix):
        inverse.append([])
        for j,cell in enumerate(row):
            inverse[-1].append(-1)
    
    temp = 0
    for i,row in enumerate(eventMatrix):
        for j,cell in enumerate(row):
            if (i % 2 == 0 and j % 2 != 0) or (i % 2 != 0 and j % 2 == 0):
                inverse[j][i] = eventMatrix[i][j]/det
            else:
                inverse[j][i] = -eventMatrix[i][j]/det
            temp+=1
        
    return inverse
def main ():
    print("Entered main")
    
    temp = [[2,-43,1,3,4],[4,324,3,-3,2],[5,7,4,456,56],[9,254,675,7,0],[0,7,5,2,54]]
    
    result = inverse(temp)
    
    print("Result is: " + str(result))
    
    exit(0)