class DeviceAddressException(Exception):
    def __init__(self, arg=""):
        self.arg = arg

class RecivePacketException(Exception):
    def __init__(self, arg=""):
        self.arg = arg

class McProtocolException(Exception):
    def __init__(self, arg=""):
        self.arg = arg
