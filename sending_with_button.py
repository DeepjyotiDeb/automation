import threading
import tkinter as tk
from tkinter import BOTTOM, TOP, LEFT, RIGHT, BOTH, X, Y, SUNKEN, W, E
import time
import smtplib
import http.client
import urllib.request as urllib2
import json

def Remergency_lock(): #place valve close mechanism
        
        print("valve closed")

class Prime(tk.Frame):
    def __init__(self,hello):
        tk.Frame.__init__(self,hello)

        self.level=tk.IntVar()
        self.us_level=tk.IntVar()
        self.i=tk.IntVar()
        self.a=tk.IntVar()
        self.status=tk.StringVar()
        self.a_status=tk.StringVar()

        tk.Label(self, text="this is the current oil level").pack()
        tk.Label(self,textvariable=self.level,bg="#b8b8bd",fg="black").pack(fill=X)#level status
        
        self.E1=tk.Entry(self,text=self.us_level)#user entry box
        self.E1.pack()
        self.E1.focus()

        btn3=tk.Button(self, text="Enter the limit", command=self.specify_level,bg="light blue",fg="black")
##        self.tk.bind('<Return>',self.specify_level)
        btn3.pack(fill=X)
        btn=tk.Button(self, text="press to send msg to supplier",command=self.t2,bg="violet",fg="black").pack(side=LEFT, fill=Y)
        btn2=tk.Button(self, text="press for emergency lock", command=self.emergency_lock,fg="black",bg="red")
        btn2.pack(fill=BOTH, expand=1)
        btn2=tk.Button(self, text="press to release", command=self.release,fg="black",bg="light green")
        btn2.pack(fill=BOTH, expand=1)
        btn1=tk.Button(self, text="press to close application",command=hello.destroy,bg="black",fg="white")
        btn1.pack(fill=X)
        
        l1=tk.Label(hello, textvariable=self.status,bd=1,relief=SUNKEN,anchor=W)#
        l1.pack(side=BOTTOM, fill=X)

        l2=tk.Label(hello, textvariable=self.a_status,bd=1,relief=SUNKEN,anchor=E)#
        l2.pack(side=BOTTOM, fill=X)
        
        self.TimerInterval=5000 ##delay before printing every value
        self.v_level=0  ##variable to store the oil level
        self.v_i=1 ##variable for sending every 5th value
        self.us_level=0 ## variable that receives user defined value
        self.v_a=0
        self.c=0
        
        self.Getv_level()

    def emergency_lock(self):#valve close mechanism
        self.a.set(self.v_a)
        self.v_a=1
        self.c=1
        self.status.set("closed")
        print("Valve closed")
        
    def release(self):#valve release mechanism
        self.a.set(self.v_a)
        self.v_a=0
        self.c=0
        self.status.set("released")
        print("valve released")

    def specify_level(self):
            self.status.set("user limit set")
            self.us_level=self.E1.get()

    def thingspeak(self):
        self.i.set(self.v_i)
        self.v_i+=1
        if self.v_i%10==0:
                data=urllib2.urlopen("https://api.thingspeak.com/update?api_key=K13USAWQYIS3ZLPP&field1="+str(round(self.v_level,2)))
                data.close()
                print("data has been sent")
        else:
                return
    def t2(self): #sending mail is an io task that can halt main execution, thread created for stability
        t3=threading.Thread(target=self.send_mail)
        t3.start()
    def send_mail(self):
        print("sending mail")
        self.status.set("sending mail")
        s=smtplib.SMTP('smtp.gmail.com',587)
        s.starttls()
        s.login("finalproject.2024@gmail.com","project@2024")
        s.sendmail("finalproject.2024@gmail.com","gouravdeb@gmail.com","\n Oil level low and the current level is: - "+str(self.v_level))
        s.quit()
        self.status.set("mail sent")
        print("sent mail")

    def close_read(self):
##        TS=urllib2.urlopen("https://dweet.io/get/latest/dweet/for/control")
        TS=urllib2.urlopen("https://api.thingspeak.com/channels/920146/fields/2.json?results=2")
        response = TS.read()
        data=json.loads(response)
        print(json.dumps(data,indent=4,sort_keys=True))
        time.sleep(20)
        b=data['channel']['feeds'][0]['field2']
        b=json.dumps(b)
        b=int(b)
        if b==1:
                self.emergency_lock()
                print("msg from client")
        else:
                self.release()
        
    def Getv_level(self):

        self.level.set(self.v_level)
        self.v_level+=1.01111
        self.v_level=round(self.v_level,2)
        t1=threading.Thread(target=self.thingspeak)#placing thingspeak data in thread to improve stability
        t1.start()
        closing_thread=threading.Thread(target=self.close_read)
        closing_thread.start()
        
        print(self.v_level)

        if int(self.us_level)<=int(self.v_level) and self.us_level!=0:
                Remergency_lock()
        elif self.c==1:
                self.emergency_lock()
        else:
                self.release()
                print("all safe")
      
        self.a_status.set("reading sensor data now...")
        
        self.after(self.TimerInterval,self.Getv_level)


class Application(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        self.title("oil level checker")
        self.geometry("300x250")
        
        Prime(self).pack()  
        self.mainloop()

Application()
