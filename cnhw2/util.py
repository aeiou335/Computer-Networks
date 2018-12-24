from ctypes import *

class header(Structure):
    _fields_ = [("length", c_uint32),
                ("seqNumber", c_uint32),
                ("ackNumber", c_uint32),
                ("fin", c_uint32),
                ("syn", c_uint32),
                ("ack", c_uint32)]

class Packet(Structure):
    _fields_ = [("head",header), ("data", c_ubyte*1000)]
