"""
*******************************************************************************    
*   BTChip Bitcoin Hardware Wallet Python API
*   (c) 2014 BTChip - 1BTChip7VfTnrPra5jqci7ejnMguuHogTn
*   
*  Licensed under the Apache License, Version 2.0 (the "License");
*  you may not use this file except in compliance with the License.
*  You may obtain a copy of the License at
*
*      http://www.apache.org/licenses/LICENSE-2.0
*
*   Unless required by applicable law or agreed to in writing, software
*   distributed under the License is distributed on an "AS IS" BASIS,
*   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
*  See the License for the specific language governing permissions and
*   limitations under the License.
********************************************************************************
"""

from abc import ABCMeta, abstractmethod
from btchipException import *
from binascii import hexlify
import hid
import time

try:
	import usb.core # using PyUSB
	WINUSB = True
except ImportError:
	WINUSB = False


class DongleWait(object):
	__metaclass__ = ABCMeta

	@abstractmethod
	def waitFirstResponse(self, timeout):
		pass

class Dongle(object):
	__metaclass__ = ABCMeta

	@abstractmethod
	def exchange(self, apdu, timeout=20000):
		pass

	@abstractmethod
	def close(self):
		pass

	def setWaitImpl(self, waitImpl):
		self.waitImpl = waitImpl

class HIDDongle(Dongle, DongleWait):

	def __init__(self, device, debug=False):
		self.device = device
		self.debug = debug
		self.waitImpl = self 
		try:
			self.device.detach_kernel_driver(0)
		except:
			pass

	def exchange(self, apdu, timeout=20000):
		if self.debug:
			print "=> %s" % hexlify(apdu)
		padSize = len(apdu) % 64
		tmp = apdu
		if padSize <> 0:
			tmp.extend([0] * (64 - padSize))		
		offset = 0
		while(offset <> len(tmp)):
			self.device.write(0x02, tmp[offset:offset + 64], 0)
			offset += 64
		dataLength = 0
		result = self.waitImpl.waitFirstResponse(timeout) 
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
					result.extend(bytearray(self.device.read(0x82, 64, timeout))[0:blockLength])
					remaining -= blockLength
			swOffset = dataLength
			dataLength -= 2
		else:
			swOffset = 0
		sw = (result[swOffset] << 8) + result[swOffset + 1]
		response = result[2 : dataLength + 2]
		if self.debug:
			print "<= %s%.2x" % (hexlify(response), sw)		
		if sw <> 0x9000:
			raise BTChipException("Invalid status %04x" % sw, sw)
		return response

	def waitFirstResponse(self, timeout):
		return bytearray(self.device.read(0x82, 64, timeout))

	def close(self):
		try:
			self.device.attach_kernel_driver(0)
		except:
			pass
		try:
			self.device.reset()
		except:
			pass

class WinUSBDongle(Dongle, DongleWait):

	def __init__(self, device, debug=False):
		self.device = device
		self.debug = debug
		self.waitImpl = self

	def exchange(self, apdu, timeout=20000):
		if self.debug:
			print "=> %s" % hexlify(apdu)
		self.device.write(0x02, apdu, 0)
		result = self.waitImpl.waitFirstResponse(timeout) 
		dataLength = 0
		if result[0] == 0x61: # 61xx : data available
			dataLength = result[1]
			swOffset = dataLength + 2
		else:
			swOffset = 0
		sw = (result[swOffset] << 8) + result[swOffset + 1]
		response = result[2 : dataLength + 2]
		if self.debug:
			print "<= %s%.2x" % (hexlify(response), sw)		
		if sw <> 0x9000:
			raise BTChipException("Invalid status %04x" % sw, sw)
		return response

	def waitFirstResponse(self, timeout):
		return bytearray(self.device.read(0x82, 260, timeout))

	def close(self):
		try:
			self.device.reset()
		except:
			pass

class HIDDongleHIDAPI(Dongle, DongleWait):

	def __init__(self, device, debug=False):
		self.device = device
		self.debug = debug
		self.waitImpl = self 

	def exchange(self, apdu, timeout=20000):
		if self.debug:
			print "=> %s" % hexlify(apdu)
		padSize = len(apdu) % 64
		tmp = apdu
		if padSize <> 0:
			tmp.extend([0] * (64 - padSize))		
		offset = 0
		while(offset <> len(tmp)):
			self.device.write(tmp[offset:offset + 64])
			offset += 64
		dataLength = 0
		result = self.waitImpl.waitFirstResponse(timeout) 
		if result[0] == 0x61: # 61xx : data available
			self.device.set_nonblocking(False)
			dataLength = result[1]
			dataLength += 2
			if dataLength > 62:
				remaining = dataLength - 62
				while(remaining != 0):
					if remaining > 64:
						blockLength = 64
					else:
						blockLength = remaining
					result.extend(bytearray(self.device.read(65))[0:blockLength])
					remaining -= blockLength
			swOffset = dataLength
			dataLength -= 2
			self.device.set_nonblocking(True)
		else:
			swOffset = 0
		sw = (result[swOffset] << 8) + result[swOffset + 1]
		response = result[2 : dataLength + 2]
		if self.debug:
			print "<= %s%.2x" % (hexlify(response), sw)		
		if sw <> 0x9000:
			raise BTChipException("Invalid status %04x" % sw, sw)
		return response

	def waitFirstResponse(self, timeout):
		start = time.time()
		data = ""
		while len(data) == 0:
			data = self.device.read(65)
			if not len(data):
				if time.time() - start > timeout:
					raise BTChipException("Timeout")
				time.sleep(0.02)				
		return bytearray(data)

	def close(self):
		try:
			self.device.close()
		except:
			pass

def getDongle(debug=False):
	dev = None
	hidDevicePath = None
	for hidDevice in hid.enumerate(0, 0):
		if hidDevice['vendor_id'] == 0x2581 and hidDevice['product_id'] == 0x2b7c:
			hidDevicePath = hidDevice['path']
		if hidDevice['vendor_id'] == 0x2581 and hidDevice['product_id'] == 0x1807:
			hidDevicePath = hidDevice['path']		
	if hidDevicePath is not None:
		dev = hid.device()
		dev.open_path(hidDevicePath)
		dev.set_nonblocking(True)
		return HIDDongleHIDAPI(dev, debug)				
	if WINUSB:	
		dev = usb.core.find(idVendor=0x2581, idProduct=0x1b7c) # core application, WinUSB
		if dev is not None:
			return WinUSBDongle(dev, debug)	
		dev = usb.core.find(idVendor=0x2581, idProduct=0x1808) # bootloader, WinUSB
		if dev is not None:
			return WinUSBDongle(dev, debug)	
		dev = usb.core.find(idVendor=0x2581, idProduct=0x2b7c) # core application, Generic HID
		if dev is not None:
			return HIDDongle(dev, debug)
		dev = usb.core.find(idVendor=0x2581, idProduct=0x1807) # bootloader, Generic HID
		if dev is not None:
			return HIDDongle(dev, debug)
	raise BTChipException("No dongle found")
