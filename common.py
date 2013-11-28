
import struct

def read32(stream):
    return struct.unpack("<L", stream.read(4))[0]

def readstr(stream):
    len = struct.unpack("<B", stream.read(1))[0]
    return stream.read(len)

def readlongstr(stream):
    len = struct.unpack("<H", stream.read(2))[0]
    return stream.read(len)

def write32(data):
    return struct.pack("<L", data)

def writestr(data):
    if len(data) > 255:
        raise Exception("len(string) > 255")
    ret  = struct.pack("<B", len(data))
    ret += data
    return ret

def writelongstr(data):
    if len(data) > 65535:
        raise Exception("len(string) > 65535")
    ret  = struct.pack("<H", len(data))
    ret += data
    return ret
