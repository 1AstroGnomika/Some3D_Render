import struct

class Encoder:
    
    index:int
    data:bytes

    def __init__(self, index:int):
        self.index = index
        self.data = bytes()
    
    def package(self) -> bytes:
        package:bytes = struct.pack("i", self.index)
        package += struct.pack("i", len(self.data))
        package += self.data
        return package
                
    def writeUTF(self, string: str):
        utf_bytes = string.encode('utf-8')
        self.writeShort(len(utf_bytes))
        self.writeBytes(utf_bytes)
            
    def writeLong(self, value: int):
        self.writeBytes(struct.pack("q", value))

    def writeInt(self, value: int):
        self.writeBytes(struct.pack("i", value))
            
    def writeFloat(self, value: float):
        self.writeBytes(struct.pack("f", value))

    def writeShort(self, value: int):
        self.writeBytes(struct.pack("h", value))
            
    def writeByte(self, value: int):
        self.writeBytes(struct.pack("B", value))
            
    def writeBoolean(self, value: bool):
        self.writeBytes(struct.pack("?", value))
        
    def writeBytes(self, byte_array: bytes):
        self.data += byte_array