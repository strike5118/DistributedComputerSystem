import time
import psutil

TIMEOUT_TIME                = 10 #Monitor the cpu usage every x seconds

WORK_AFTER_SECONDS_IDLE     = 100#60 * 5 #Work after this many seconds idle

MIN_IDLE_TO_WORK            = 50 #work if the idle cpu percentage is above this 

# start by assuming system under compete stress
cpu_usage = []

for i in range(int(WORK_AFTER_SECONDS_IDLE/TIMEOUT_TIME)):
    cpu_usage.append(100)

cacheAverage = None


def shouldWork():
    '''
    Returns true if the system can be used
    otherwise False
    '''
    log("Checking if we should work")
    global cacheAverage
    
    if not cacheAverage:
        sum = 0
        
        for i in cpu_usage:
            sum += i
        cacheAverage = sum/len(cpu_usage)
        
    log("Average cpu usage is "+str(cacheAverage) + "%")
    
    if (100 - cacheAverage) > MIN_IDLE_TO_WORK:
        return True
    else:
        return False

def monitor_loop():
    '''
    Function to put in a separate thread, never returns
    
    Monitors the system usage and stores in cpu_usage array
    
    '''
    i = 0
    while True:
        cpu_usage[i] = psutil.cpu_percent()
        
        log("Sampling cpu usage, percentage is "+ str(cpu_usage[i]) + "%")
        i = (i+1) % len(cpu_usage)
        
        time.sleep(TIMEOUT_TIME)
        
        #invalidate cache
        global cacheAverage
        cacheAverage = None
        
def log (string):
    print("[system_monitor.py] " +string)