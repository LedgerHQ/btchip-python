from btchipException import BTChipException

def readVarint(buffer, offset):
	varintSize = 0
	value = 0
	if (buffer[offset] < 0xfd):
		value = buffer[offset]
		varintSize = 1
	elif (buffer[offset] == 0xfd):
		value = (buffer[offset + 2] << 8) | (buffer[offset + 1])
		varintSize = 3
	elif (buffer[offset] == 0xfe):
		value = (buffer[offset + 4] << 24) | (buffer[offset + 3] << 16) | (buffer[offset + 2] << 8) | (buffer[offset + 1])
		varintSize = 5
	else:
			raise BTChipException("unsupported varint")
	return { "value": value, "size": varintSize }

def writeVarint(value, buffer):
	if (value < 0xfd):
		buffer.append(value)
	elif (value <= 0xffff):
		buffer.append(0xfd)
		buffer.append(value & 0xff)
		buffer.append((value >> 8) & 0xff)
	elif (value <= 0xffffffff):
		buffer.append(0xfe)
		buffer.append(value & 0xff)
		buffer.append((value >> 8) & 0xff)
		buffer.append((value >> 16) & 0xff)
		buffer.append((value >> 24) & 0xff)
	else:		
		raise BTChipException("unsupported encoding")
	return buffer

def getVarintSize(value):
	if (value < 0xfd):
		return 1
	elif (value <= 0xffff):
		return 3
	elif (value <= 0xffffffff):
		return 5
	else:
		raise BTChipException("unsupported encoding")
