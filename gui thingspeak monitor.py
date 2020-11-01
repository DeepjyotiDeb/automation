import tkinter as tk
import threading
import urllib.request as urllib2
import json
from tkinter import BOTTOM, TOP, LEFT, RIGHT, BOTH, X, Y, SUNKEN, W, E

##lock=1
##oopen=0
##
##def valve_close():
##    data=urllib2.urlopen("https://dweet.io/dweet/for/control?open-or-close="+str(lock))
##    data.close()
##    print("close command has been sent")
##def close_thread():
##    cthread=threading.Thread(target=valve_close)
##    cthread.start()
##def valve_open():
##    data=urllib2.urlopen("https://dweet.io/dweet/for/control?open-or-close="+str(oopen))
##    data.close()
##    print("open command has been sent")
##def open_thread():
##    cthread=threading.Thread(target=valve_open)
##    cthread.start()
##    
##def T3(b):
##    TS=urllib2.urlopen("https://api.thingspeak.com/channels/920146/fields/1.json?results=2")
##    response = TS.read()
##    data=json.loads(response)
##    print(json.dumps(data,indent=4,sort_keys=True))
##    b= data['feeds'][0]['field1']
##    return b
##def t1():
##    t2=threading.Thread(target=T3)
##    t2.start()


class Monitor(tk.Frame):

    def __init__(self,master):
        tk.Frame.__init__(self,master)
        
        self.Level = tk.IntVar()
        
        tk.Label(self, textvariable = self.Level, font="Arial 30", width=10).pack()
        self.TimerInterval=1000
        bt=tk.Button(self, text='close valve', command=self.close_thread, font=15, fg="black",bg="red").pack(fill=BOTH, expand=1)
        bt1=tk.Button(self, text='open valve', command=self.open_thread, font=15, fg="black",bg="light green").pack(fill=BOTH, expand=1)
        bt=tk.Button(master, text='close', command=master.destroy, font="bold 20", bg="#ff8949").pack(side=BOTTOM, fill=X)
        # variable for dummy Getlevel
        self.Temp = 0
##        self.b=0
        self.lock=1
        self.open=0
        self.b=0
        # call Get level which will call itself after a delay
        self.GetLev()
        
    def valve_close(self):
        data=urllib2.urlopen("https://dweet.io/dweet/for/control?open-or-close="+str(self.lock))
        data.close()
        print("close command has been sent")
    def close_thread(self):
        cthread=threading.Thread(target=self.valve_close)
        cthread.start()
    def valve_open(self):
        data=urllib2.urlopen("https://dweet.io/dweet/for/control?open-or-close="+str(self.open))
        data.close()
        print("open command has been sent")
    def open_thread(self):
        cthread=threading.Thread(target=self.valve_open)
        cthread.start()
        
    def T3(self):
        TS=urllib2.urlopen("https://api.thingspeak.com/channels/920146/fields/1.json?results=2")
        response = TS.read()
        data=json.loads(response)
        print(json.dumps(data,indent=4,sort_keys=True))
        self.b= data['feeds'][0]['field1']
    def t1(self):
        t2=threading.Thread(target=self.T3)
        t2.start()
    
    def GetLev(self):
##        T3(b)
##        print (T3(b))
        self.t1()
##        t1()
        self.b=float(self.b)
        self.Level.set(self.b)
##        self.Level.set(float(b))
        self.after(self.TimerInterval,self.GetLev)
   
class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
               
     
        self.title('monitor gui')
        
        self.geometry('300x200')
      
   
        Monitor(self).pack()
        
    
        self.mainloop()
                    

App()
