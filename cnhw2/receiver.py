import socket
from ctypes import *
from util import header, Packet

class Receiver:
    def __init__(self, ip, port, agentIP, agentPort, sendIP, sendPort, filename="result"):
        self.ip = ip
        self.port = port
        self.bufferSize = 32
        self.buffer = []
        self.f = open(filename, "wb") 
        self.agent = (agentIP, agentPort)
        self.sender = (sendIP, sendPort)
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.bind((self.ip, self.port))

    def sendPacket(self, curr_recv=0, fin=False):
        if fin:
            h = header(0,0,0,1,0,1)
        else:
            h = header(0, 0, curr_recv, 0, 0, 1)
            print("send ack #%s" % curr_recv)
        packet = Packet(h, (c_ubyte*1000)(*(b'')))
        self.s.sendto(packet, self.agent)

    def flush(self):
        for data in self.buffer:
            #print(bytearray(data))
            self.f.write(data)
        self.buffer = [] 

    def recv(self):
        curr_recv = 0
        
        while True:   
            p = Packet.from_buffer_copy(self.s.recvfrom(1024)[0])
            start = True
            #print("recv data #%s" %p.head.seqNumber)
            #print(p.head.length, p.head.seqNumber, p.head.ackNumber, p.head.fin, p.head.syn, p.head.ack)
            if p.head.fin == 1:
                print("recv fin")
                self.sendPacket(fin=True)
                print("send finack")
                self.flush()
                print("flush")
                break
            
            if len(self.buffer) == self.bufferSize:
                print("drop data #%s" % p.head.seqNumber)
                self.sendPacket(curr_recv)
                self.flush()
                print("flush")
                continue

            if p.head.seqNumber == curr_recv + 1:
                print("recv data #%s" % p.head.seqNumber)
                self.buffer.append(bytearray(p.data)[:p.head.length])
                curr_recv += 1
            else:
                print("drop data #%s" % p.head.seqNumber)
            self.sendPacket(curr_recv=curr_recv)
        
        self.f.close()
        

if __name__ == "__main__":
    r = Receiver("localhost", 8889, "localhost", 8888, "localhost", 8887)
    print("Start receiving packets...")
    r.recv()