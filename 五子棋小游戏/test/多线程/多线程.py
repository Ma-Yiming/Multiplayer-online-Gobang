
import socket
import threading
import time

iswaiting = 0

def threadwait(i):
    global iswaiting
    if i == 1:
        while True:
            if iswaiting:
                while iswaiting:
                    print('我是子程序，主程序正在待机\n')
                    time.sleep(3)
            else:
                print('我是子程序,主程序在运行\n')
                time.sleep(3)
    else:
        while True:
            running = True
            while running:
                iswaiting = 0
                print("运行中......\n")
                time.sleep(3)
                iswaiting = 1
                print("等待中......\n")
                time.sleep(3)
def thread():
    for i in range(2):        
        t = threading.Thread(target=threadwait,args=(i,))
        t.start()
thread()
