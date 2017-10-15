import time
import system_monitor
import server_interface
import workhourse
from threading import Thread

quit = False

timeout = 5

def log(string):
    print ("[main.py] "+string)

def loop():
    global timeout
    
    while True:
        log("Sleeping for %d seconds..." % timeout)
        time.sleep(timeout)

        if shouldQuit():
            log("Quitting...")
            return
        elif system_monitor.shouldWork():
            workToDo = server_interface.getWork()
            
            if (workToDo == None):
                log("No work to do")
            else:
                server_interface.reportResults(workhourse.doWork(workToDo))
        else:
            log("System under use - not doing work.")

def shouldQuit():
    log("Checking if we should quit...")
    global quit
    return quit

def exit():
    global quit
    quit = True

thread = Thread(target=system_monitor.monitor_loop)
thread.daemon = True
thread.start()
loop()