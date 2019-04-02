from importlib import reload
from threading import Thread
import socket
import time

#My parser "library"
import ld
def preluc(data,PORT,org,C):
    try:
        reload(ld)
        ld.prel(data,PORT,org,C)
    except Exception as e:
        print(e)

####################################################
class Client(Thread):
    def __init__(self,IP,PORT,Serv):
        super(Client, self).__init__()
        self.setName("Client on "+str(PORT))
        print("Client Opening on ",str(PORT))
        self.PORT=PORT
        self.S=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.S.connect((IP,PORT))
        self.ON=True
        self.Serv=Serv
    def run(self):
        print("Client Started on ",str(self.PORT))
        while self.ON:
            try:
                data=self.S.recv(4096)
            except ConnectionAbortedError:
                self.ON=False
                data=None
            if data:
                preluc(data,self.PORT,"Server",self)
                try:
                    self.Serv.sendall(data)
                except:
                    self.ON=False
        
        print("Client Stoped on ",str(self.PORT))
####################################################################3        
class Server(Thread):
    def __init__(self,targhet,PORT):
        super(Server, self).__init__()
        print("Server Opening on ",str(PORT))
        self.setName("Server on "+str(PORT))
        self.PORT=PORT
        self.targhet=targhet
        self.S=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.S.bind(("0.0.0.0",PORT))
        self.C=None
        self.ON=True
    def run(self):
        print("Server Started on ",str(self.PORT))
        while self.ON:
            self.S.listen(1)
            self.con, addr = self.S.accept()
            while self.ON :
                try:
                    data=self.con.recv(4096)
                except: #ConnectionAbortedError ConnectionResetError:
                    self.C=None
                    data=None
                    #self.ON=False
                    break
                if data:
                    if self.C==None:
                        self.C=Client(self.targhet,self.PORT,self.con)
                        self.C.start()
                    preluc(data,self.PORT,"Client",self.C)
                    self.C.S.sendall(data)
                    
            self.con.close()
            self.C=None
        try:
            self.C.ON=False
        except:
            None
        print("Server Closed on ",str(self.PORT))
    def STOP(self):
        self.ON=False
        try:
            self.C.ON=False
        except:
            None
#######################################################################
class Proxy():
    def __init__(self,HOST,PORT,CL):
        self.HOST=HOST
        self.PORT=PORT
        self.CL=CL
        self.M=Server(HOST,PORT)
        self.M.start()
        self.GS=[]
        time.sleep(0.05)
        for i in range(CL):
            time.sleep(0.05)
            self.GS.append(Server(HOST,3000+i))
            self.GS[i].start()
    def STOP(self):
        self.M.STOP()
        for i in range(self.CL):
            time.sleep(0.05)
            self.GS[i].STOP()

#CHANGE ME!!!
IP="0.0.0.0"#Server's IP
P=Proxy(IP,3333,4)
time.sleep(1)
ON=True
print("JOB Done")
try:
    while ON:
        ON=ON
        #print ("3")
except KeyboardInterrupt:
    print("Stoping....")
    P.STOP()
    time.sleep(1)
    print("Stoped")
