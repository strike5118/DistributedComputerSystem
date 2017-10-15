workLookUpTable = {0:"identity(work[1])",1:"det(work[1])"}


def doWork(work):
    log("Doing work... with "+str(work))
    
    workToDo = workLookUpTable[work[0]]
    
    try:
        result = eval(workToDo)
        log("Result is: " + str(result))
        return result
    except:
        log("Failed to do work")
        

def identity(args):
    return args
    
def det(args):
    print("det called with arguments" + str(args))
    if len(args) == 1:
        log("det returning: "+str(args[0][0]))
        return args[0][0]
    else:
        #recursively call to get det
        value = 0
        for i,cell in enumerate(args[0]): # for each column
            newMatrix = []
            for rowIndex in range(1,len(args)): # get matrix without given col and row
                newMatrix.append([])
                for j,cell2 in enumerate(args[rowIndex]):
                    if j != i:
                        newMatrix[-1].append(cell2)

            if i % 2 == 0:
                value -=  cell*det(newMatrix)
            else:
                value += cell*det(newMatrix)

        log("det returning: "+str(value))
        return value
        
def log(string):
    print("[workhorse.py] " + str(string))