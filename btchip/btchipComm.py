from abc import ABCMeta, abstractmethod
from btchipException import *
from binascii import hexlify
import usb.core # using PyUSB

class Dongle(object):
	__metaclass__ = ABCMeta

	@abstractmethod
	def exchange(self, apdu):
		pass

	@abstractmethod
	def close(self):
		pass

class HIDDongle(Dongle):

	def __init__(self, device):
		self.device = device
		try:
			self.device.detach_kernel_driver(0)
		except:
			pass

	def exchange(self, apdu):
		print "=> " + hexlify(apdu)
		padSize = len(apdu) % 64
		tmp = apdu
		if padSize <> 0:
			tmp.extend([0] * (64 - padSize))		
		offset = 0
		while(offset <> len(tmp)):
			self.device.write(0x02, tmp[offset:offset + 64], 0)
			offset += 64
		dataLength = 0
		result = bytearray(self.device.read(0x82, 64, 0, 10000))
		if result[0] == 0x61: # 61xx : data available
			dataLength = result[1]
			dataLength += 2
			if dataLength > 62:
				remaining = dataLength - 62
				while(remaining != 0):
					if remaining > 64:
						blockLength = 64
					else:
						blockLength = remaining
					result.extend(bytearray(self.device.read(0x82, 64, 0, 10000))[0:blockLength])
					remaining -= blockLength
			swOffset = dataLength
			dataLength -= 2
		else:
			swOffset = 0
		sw = (result[swOffset] << 8) + result[swOffset + 1]
		if sw <> 0x9000:
			raise BTChipException("Invalid status %04x" % sw)
		response = result[2 : dataLength + 2]
		print "<= " + hexlify(response)
		return response

	def close(self):
		try:
			self.device.attach_kernel_driver(0)
		except:
			pass

class WinUSBDongle(Dongle):

	def __init__(self, device):
		self.device = device

	def exchange(self, apdu):
		self.device.write(0x02, apdu, 0)
		result = bytearray(self.device.read(0x82, 260, 0, 10000))
		dataLength = 0
		if result[0] == 0x61: # 61xx : data available
			dataLength = result[1]
			swOffset = dataLength + 2
		else:
			swOffset = 0
		sw = (result[swOffset] << 8) + result[swOffset + 1]
		if sw <> 0x9000:
			raise BTChipException("Invalid status %04x" % sw)
		return result[2 : dataLength + 2]

	def close(self):
		pass

def getDongle():
	dev = usb.core.find(idVendor=0x2581, idProduct=0x1b7c) # core application, WinUSB
	if dev is not None:
		return WinUSBDongle(dev)	
	dev = usb.core.find(idVendor=0x2581, idProduct=0x1808) # bootloader, WinUSB
	if dev is not None:
		return WinUSBDongle(dev)	
	dev = usb.core.find(idVendor=0x2581, idProduct=0x2b7c) # core application, Generic HID
	if dev is not None:
		return HIDDongle(dev)
	dev = usb.core.find(idVendor=0x2581, idProduct=0x1807) # bootloader, Generic HID
	if dev is not None:
		return HIDDongle(dev)
	raise BTChipException("No dongle found")
