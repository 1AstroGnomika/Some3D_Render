import struct

class Decoder:
    
	data:bytes
	position:int

	def __init__(self, data:bytes):
		self.data = data
		self.position = int()
		
	@property
	def available(self) -> bool:
		return max(0, len(self.data) - self.position)

	def __decoder(self, type, buffer):
		return struct.unpack(type, buffer)[0]

	def readUTF(self):
		stringLen = self.readShort()
		return self.readBytes(stringLen).decode("utf-8")

	def readDouble(self):
		return self.__decoder("d", self.readBytes(8))
		
	def readLong(self):
		return self.__decoder("q", self.readBytes(8))

	def readInt(self):
		return self.__decoder("i", self.readBytes(4))
		
	def readFloat(self):
		return self.__decoder("f", self.readBytes(4))
		
	def readShort(self):
		return self.__decoder("h", self.readBytes(2))
		
	def readBoolean(self):
		return self.__decoder("?", self.readBytes(1))
		
	def readByte(self):
		return self.readBytes(1)[0]

	def readBytes(self, length):
		if(self.position + length <= len(self.data)):
			buffer = self.data[self.position : self.position + length]
			self.position += length
			return buffer
		raise Exception(f"Not enougth bytes for unpack [{length}/{self.available}]")