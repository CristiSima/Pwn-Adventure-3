import struct
import socket
import os
def ID(data)->hex:
    return struct.unpack(">H", data[0:2])[0]
def trs(data)->hex:    
    return data.hex()
def sb(b):
    S=""
    p=128
    for i in range(8):
        v=str(int(b/p))
        #print(v)
        S+=str(v)
        if(b//p==1):
            b-=p
        p/=2
    return S
def b2(b):
    S=""
    for bi in b:
        S+=sb(bi)
    return S
client=None
O=None
class interpret():
    def pos(data):#20
        #print(trs(data))
        #return
        X,Y,Z=struct.unpack("fff", data[0:3*4])
        data=data[12:]
        
        #Camera
        data=data[4:]

        #?
        data=data[2:]



        #dir
        data=data[2:]
        
        SHOW=False
        #SHOW=True
        if SHOW:
            print("{:.2f} {:.2f} {:.2f}".format(X,Y,Z))
        
        if(client==None):
            print("Client!!!!")
        return data

    def jmp(data):
        J=data[1]
        data=data[1:]
        return data
    def selh(data):
        j=data[1]
        data=data[1:]
        return data
    def spell(data):#WIP
        ln,s1=struct.unpack("BB", data[:2])
        data=data[2:]

        
        txt=data[:ln]
        txt=str(txt)[2:-1]
        data=data[ln:]
        
        
        pos=data[:12]
        pos=trs(pos)
        data=data[12:]

        #print("{}:{}| {}".format(txt,s1,pos))
        return data
    def walk(data):
        j=data[1]
        data=data[1:]
        return data
    def RPDAME(data):
        return []
    def MOB(data):
        ID,X,Y,Z=struct.unpack("Ifff", data[:4*4])
        #print()
        #print("{:d} : {:.2f} , {:.2f} , {:.2f}".format(ID,X,Y,Z))
        #'''
        #if(ID==582 or ID== 608):
        #print(trs(data[:28]))
        #'''
        return data[28:]
    def GOL(data):
        return []
    def EntA1(data):
        return data[10:]
    def ACT(data):#INIT
        ID,s1,s2,s3,a,ln,s4=struct.unpack("H"+"HHH"+"BB"+"B",data[:11])
        data=data[11:]
        
        #print(ln)
        txt=str(data[:ln])
        txt=txt[2:-1]
        data=data[ln:]
        X,Y,Z,s5,s6,s7=struct.unpack("fff"+"iiH",data[:22])
        data=data[22:]
        print("{:x} | {}  {} : {:.2f} {:.2f} {:.2f}".format(ID,a,txt,X,Y,Z))
        #print(s1,"|",s2,"|",s3,"|",s4,"|",s5,"|",s6,"|",s7)
        if("Drop" in txt):
            pickup = struct.pack("=HI", 0x6565, ID)
            client.S.sendall(pickup)
        return data
    def E_HP(data):
        ID=struct.unpack("I",data[:4])[0]
        data=data[4:]
        HP_s=struct.unpack("I",data[:4])[0]
        HP_u=struct.unpack("i",data[:4])[0]
        print("{} : {} | {}".format(ID,HP_s,HP_u))
        data=data[4:]
        return data
    def state(data):
        ID,ln=struct.unpack("IH", data[:6])
        data=data[6:]
        #print(ln)
        name=data[:ln]
        name=str(name)
        name=name[2:-1]
        data=data[ln:]
        s=trs(data[:2])
        s=struct.unpack("H", data[:2])[0]
        data=data[2:]
        #print("{} -> {}: {}".format(ID,s,name))
        return data
    def beam(data):
        data=data[1:]
        return data
    def reload(data):
        return data
    def pickdrop(data):
        data=data[4:]
        return data
    def blocky(data):
        #print(trs(data))
        '''
        info=data[:7]
        data=data[7:]

        L=struct.unpack("b",data[:1])[0]
        L=int(L)
        L%=16
        data=data[1:]

        IN=data[:4]
        data=data[4:]
        IN=b2(IN)

        
        if(O=="Client"):
            return data
        OUT=data[:3]
        data=data[3:]
        OUT=b2(OUT)
        print("L:{} | {} -> {}".format(L,IN,OUT))
        '''

        ln=struct.unpack("H",data[:2])[0]
        data=data[2:]
        txt=str(data[:ln])[2:-1]
        data=data[ln:]

        IN=data[:4]
        data=data[4:]
        IN=b2(IN)

        if(O=="Client" or txt !="FinalStage"):
            return data
        
        OUT=data[:24]
        data=data[24:]
        OUT=b2(OUT)

        
        print("{} :  {} -> {}".format(txt,IN,OUT))
        return data
        
    def unk1(data):#not done
        data=data[4:]
        return data
    def unk2(data):
        data=data[4:]
        return data
    def unk3(data):
        data=data[4:]
        return data
    def unk4(data):
        data=data[4:]
        return data
        
        

    ls={
     0x6d76: pos,
     0x6a70: jmp,
     0x733d: selh,
     0x2a69: spell,
     0x726e: walk,
     0x1703: RPDAME,
     0x7073: MOB,
     0x0000: GOL,
     0x7374: EntA1,
     0x6d6b: ACT,
     0x2b2b: E_HP,
     0x7472: state,
     0x6672: beam,
     0x726c: reload,
     0x3031: blocky,
     0x6d61: unk1,
     0xabf0: unk2,
     0x7878: unk3,
     0x6c61: unk4
    }
        
    
def prel(data,port,origin,C):# C=clent class
    af=""

    #print(sb(255))
    #print(b2(struct.pack("b",0)))
    
    global client
    global O
    O=origin    
    client=C
    
    
    #print(data)
    if(origin=="Client"):
        #return 
        af+="Client -> Server"

    else:
        #return 
        af+="Server -> Client"

        
    pk=trs(data)
    
    af+=" "
    if(pk=="0x0"):
        return
    #print(ID(data))
    #print("------------------------")
    #print(trs(data))
    while len(data)>=2:
        if ID(data) in interpret.ls:
            #print(trs(data))
            data=interpret.ls[ID(data)](data[2:])
            #print(trs(data))
        else:
            break
    #print(trs(data))

    if(len(data)!=0):
        af+=trs(data)
        print (af)#+"|"+pk)
    else:
        None
        #print(trs(data))
        #print("Done")
    #print(pk[2:])
    
    #print("------------------------")
