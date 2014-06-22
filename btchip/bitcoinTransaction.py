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

from bitcoinVarint import *
from binascii import hexlify

class bitcoinInput:

	def __init__(self, bufferOffset=None):
		self.prevOut = ""
		self.script = ""
		self.sequence = ""
		if bufferOffset is not None:
			buf = bufferOffset['buffer']
			offset = bufferOffset['offset']
			self.prevOut = buf[offset:offset + 36]
			offset += 36
			scriptSize = readVarint(buf, offset)
			offset += scriptSize['size']
			self.script = buf[offset:offset + scriptSize['value']]
			offset += scriptSize['value']
			self.sequence = buf[offset:offset + 4]			
			offset += 4
			bufferOffset['offset'] = offset

	def serialize(self):
		result = []
		result.extend(self.prevOut)
		writeVarint(len(self.script), result)
		result.extend(self.script)
		result.extend(self.sequence)
		return result

	def __str__(self):
		buf =  "Prevout : " + hexlify(self.prevOut) + "\r\n"
		buf += "Script : " + hexlify(self.script) + "\r\n"
		buf += "Sequence : " + hexlify(self.sequence) + "\r\n"
		return buf		

class bitcoinOutput:

	def __init__(self, bufferOffset=None):
		self.amount = ""
		self.script = ""		
		if bufferOffset is not None:
			buf = bufferOffset['buffer']
			offset = bufferOffset['offset']
			self.amount = buf[offset:offset + 8]
			offset += 8
			scriptSize = readVarint(buf, offset)
			offset += scriptSize['size']
			self.script = buf[offset:offset + scriptSize['value']]
			offset += scriptSize['value']
			bufferOffset['offset'] = offset

	def serialize(self):
		result = []
		result.extend(self.amount)
		writeVarint(len(self.script), result)
		result.extend(self.script)
		return result

	def __str__(self):
		buf =  "Amount : " + hexlify(self.amount) + "\r\n"
		buf += "Script : " + hexlify(self.script) + "\r\n"
		return buf		


class bitcoinTransaction:

	def __init__(self, data=None):
		self.version = ""
		self.inputs = []
		self.outputs = []
		self.lockTime = ""
		if data is not None:
			offset = 0
			self.version = data[offset:offset + 4]
			offset += 4
			inputSize = readVarint(data, offset)
			offset += inputSize['size']
			numInputs = inputSize['value']
			for i in range(numInputs):
				tmp = { 'buffer': data, 'offset' : offset}
				self.inputs.append(bitcoinInput(tmp))
				offset = tmp['offset']
			outputSize = readVarint(data, offset)
			offset += outputSize['size']				
			numOutputs = outputSize['value']
			for i in range(numOutputs):
				tmp = { 'buffer': data, 'offset' : offset}
				self.outputs.append(bitcoinOutput(tmp))
				offset = tmp['offset']
			self.lockTime = data[offset:offset + 4]

	def serialize(self, skipOutputLocktime=None):
		result = []
		result.extend(self.version)
		writeVarint(len(self.inputs), result)
		for trinput in self.inputs:
			result.extend(trinput.serialize())
		if not skipOutputLocktime:
			writeVarint(len(self.outputs), result)
			for troutput in self.outputs:
				result.extend(troutput.serialize())
			result.extend(self.lockTime)
		return result

	def __str__(self):
		buf =  "Version : " + hexlify(self.version) + "\r\n"
		index = 1
		for trinput in self.inputs:
			buf += "Input #" + str(index) + "\r\n"
			buf += str(trinput)
			index+=1
		index = 1
		for troutput in self.outputs:
			buf += "Output #" + str(index) + "\r\n"
			buf += str(troutput)
			index+=1
		buf += "Locktime : " + hexlify(self.lockTime) + "\r\n"
		return buf		
