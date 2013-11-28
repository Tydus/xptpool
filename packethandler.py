

XPT_OPC_C_AUTH_REQ     = 1
XPT_OPC_S_AUTH_ACK     = 2
XPT_OPC_S_WORKDATA1    = 3
XPT_OPC_C_SUBMIT_SHARE = 4
XPT_OPC_S_SHARE_ACK    = 5
XPT_OPC_C_SUBMIT_POW   = 6
XPT_OPC_S_MESSAGE      = 7

ALGORITHM_SHA256       = 1
ALGORITHM_SCRYPT       = 2
ALGORITHM_PRIME        = 3
ALGORITHM_PROTOSHARES  = 4

from common import *

def BasePacketHandler(object):
    pass

def UnknownPacketHandler(BasePacketHandler):
    @staticmethod
    def read(stream):
        pass

def AuthRequestPacketHandler(BasePacketHandler):
    @staticmethod
    def read(stream):
        version = read32(stream)
        username = readstr(stream)
        password = readstr(stream)
        minerver = readstr(stream)
        AuthResponsePacketHandler.write(stream)

def AuthResponsePacketHandler(BasePacketHandler):
    @staticmethod
    def write(stream, rejectReason = ""):
        errcode = (rejectReason != "")
        data = ""
        data += write32(errcode)
        data += writelongstr(rejectReason)
        data += write8(ALGORITHM_PROTOSHARES)
        stream.write(XPT_OPC_S_AUTH_ACK, data)

def GetWorkPacketHandler(BasePacketHandler):
    @staticmethod
    def write(stream):
        pass


def SubmitSharePacketHandler(BasePacketHandler):
    @staticmethod
    def read(stream):
        merkleroot = stream.read(32)
        prevhash   = stream.read(32)
        version    = read32(stream)
        nTime      = read32(stream)
        nonce      = read32(stream)
        nBits      = read32(stream)

        birthdayA  = read32(stream)
        birthdayB  = read32(stream)
        originroot = stream.read(32)
        len  = read8(stream)
        extranonce = stream.read(len)

        shareID    = read32(stream)

        ....

        ShareAckPacketHandler.write(stream, shareID, rejectReason, shareValue)


def ShareAckPacketHandler(BasePacketHandler):
    @staticmethod
    def write(stream, shareID, rejectReason = "", shareValue = 1):
        errcode = (rejectReason != "")
        data = ""
        data += write32(errcode)
        data += writelongstr(rejectReason)
        data += writefloat(shareValue)
        stream.write(XPT_OPC_S_AUTH_ACK, data)

packetHandler = {
    0: UnknownPacketHandler,
    1: AuthRequestPacketHandler,
    4: SubmitSharePacketHandler,
}

__all__ = {'packetHandler'}
