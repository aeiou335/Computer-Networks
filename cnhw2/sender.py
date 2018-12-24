import socket
import logging
from ctypes import *
from util import header, Packet
"""
typedef struct {
	int length;
	int seqNumber;
	int ackNumber;
	int fin;
	int syn;
	int ack;
} header;
"""
class Sender:
    def __init__(self, ip, port, agentIP, agentPort, recvIP, recvPort, timeout=0.5):
        self.ip = ip
        self.port = port
        self.packetSize = 1000
        self.threshold = 16
        self.windowSize = 1
        self.agent = (agentIP, agentPort)
        self.receiver = (recvIP, recvPort)
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.bind((self.ip, self.port))
        self.s.settimeout(timeout)
    
    def sendPacket(self, packet):
        self.s.sendto(packet, self.agent)

    def createPackets(self, _file):
        packets = []
        count = 1
        with open(_file, "rb") as f:
            while True:
                data = f.read(1000)
                #print("ori data:",data)
                h = header(len(data),count,0,0,0,0)
                packet = Packet(h, (c_ubyte*1000)(*data))
                #print("data:", packet.data)
                if not data:
                    break
                packets.append(packet)
                count += 1
        return packets

    def checkACK(self, curr_ack, expect_ack_end):
        success = False
        while True:
            try:
                p = Packet.from_buffer_copy(self.s.recvfrom(1024)[0])
                print("recv ack #%s" %p.head.ackNumber)
                if p.head.ack == 1 and p.head.ackNumber == curr_ack+1:
                    curr_ack += 1
                if curr_ack == expect_ack_end:
                    success = True
                    break
            except socket.timeout:
                self.threshold = max(self.windowSize // 2, 1)
                print("time out      threshold = ", self.threshold)
                break
        #print(success, curr_ack)
        return success, curr_ack

    def send(self, _file):
        packets = self.createPackets(_file)
        n_packets = len(packets)
        resend = [False]*n_packets
        print("number of packets:", n_packets)
        print("start sending packets...")
        
        curr_packet = 0
        packet_have_sent = 0
        success = False
        while packet_have_sent < n_packets:
            end = min(self.windowSize + packet_have_sent, n_packets)
            while curr_packet < end:
                self.sendPacket(packets[curr_packet])               
                if resend[curr_packet]:
                    print("resnd data #%s, winSize = %s" % (curr_packet+1, self.windowSize))
                else:
                    print("send data #%s, winSize = %s" % (curr_packet+1, self.windowSize))
                resend[curr_packet] = True
                curr_packet += 1

            success, ack_return = self.checkACK(packet_have_sent, end)
            if success:
                packet_have_sent = end
                if self.windowSize > self.threshold:
                    self.windowSize += 1
                else:
                    self.windowSize *= 2
            else:
                packet_have_sent = ack_return 
                curr_packet = ack_return
                self.windowSize = 1
        
        finPacket = Packet(header(len(b''), n_packets+1,0,1,0,0), (c_ubyte*1000)(*(b'')))
        print("send fin")
        self.sendPacket(finPacket)
        p = Packet.from_buffer_copy(self.s.recvfrom(1024)[0])
        if p.head.fin == 1:
            print("recv finack")
        else:
            print("Error: expect finack")
                
if __name__ == "__main__":
    s = Sender("localhost", 8887, "localhost", 8888, "localhost", 8889)
    s.send("test.png")