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

from btchipComm import *
from bitcoinTransaction import *
from bitcoinVarint import *
from btchipException import *
from btchipHelpers import *

class btchip:
	BTCHIP_CLA = 0xe0

	BTCHIP_INS_SETUP = 0x20
	BTCHIP_INS_VERIFY_PIN = 0x22
	BTCHIP_INS_GET_OPERATION_MODE = 0x24
	BTCHIP_INS_SET_OPERATION_MODE = 0x26
	BTCHIP_INS_SET_KEYMAP = 0x28
	BTCHIP_INS_SET_COMM_PROTOCOL = 0x2a
	BTCHIP_INS_GET_WALLET_PUBLIC_KEY = 0x40
	BTCHIP_INS_GET_TRUSTED_INPUT = 0x42
	BTCHIP_INS_HASH_INPUT_START = 0x44
	BTCHIP_INS_HASH_INPUT_FINALIZE = 0x46
	BTCHIP_INS_HASH_SIGN = 0x48
	BTCHIP_INS_HASH_INPUT_FINALIZE_FULL = 0x4a
	BTCHIP_INS_GET_INTERNAL_CHAIN_INDEX = 0x4c
	BTCHIP_INS_SIGN_MESSAGE = 0x4e
	BTCHIP_INS_GET_TRANSACTION_LIMIT = 0xa0
	BTCHIP_INS_SET_TRANSACTION_LIMIT = 0xa2
	BTCHIP_INS_IMPORT_PRIVATE_KEY = 0xb0
	BTCHIP_INS_GET_PUBLIC_KEY = 0xb2
	BTCHIP_INS_DERIVE_BIP32_KEY = 0xb4
	BTCHIP_INS_SIGNVERIFY_IMMEDIATE = 0xb6
	BTCHIP_INS_GET_RANDOM = 0xc0
	BTCHIP_INS_GET_ATTESTATION = 0xc2
	BTCHIP_INS_GET_FIRMWARE_VERSION = 0xc4
	BTCHIP_INS_COMPOSE_MOFN_ADDRESS = 0xc6
	BTCHIP_INS_GET_POS_SEED = 0xca

	CHAIN_EXTERNAL = 0x01
	CHAIN_INTERNAL = 0x02

	OPERATION_MODE_WALLET = 0x01
	OPERATION_MODE_RELAXED_WALLET = 0x02
	OPERATION_MODE_SERVER = 0x04
	OPERATION_MODE_DEVELOPER = 0x08

	FEATURE_UNCOMPRESSED_KEYS = 0x01
	FEATURE_RFC6979 = 0x02
	FEATURE_FREE_SIGHASHTYPE = 0x04

	QWERTY_KEYMAP = bytearray("000000000000000000000000760f00d4ffffffc7000000782c1e3420212224342627252e362d3738271e1f202122232425263333362e37381f0405060708090a0b0c0d0e0f101112131415161718191a1b1c1d2f3130232d350405060708090a0b0c0d0e0f101112131415161718191a1b1c1d2f313035".decode('hex'))
	AZERTY_KEYMAP = bytearray("08000000010000200100007820c8ffc3feffff07000000002c38202030341e21222d352e102e3637271e1f202122232425263736362e37101f1405060708090a0b0c0d0e0f331112130415161718191d1b1c1a2f64302f2d351405060708090a0b0c0d0e0f331112130415161718191d1b1c1a2f643035".decode('hex'))	

	def __init__(self, dongle):
		self.dongle = dongle

	def verifyPin(self, pin):
		apdu = [ self.BTCHIP_CLA, self.BTCHIP_INS_VERIFY_PIN, 0x00, 0x00, len(pin) ]
		apdu.extend(bytearray(pin))
		self.dongle.exchange(bytearray(apdu))

	def getWalletPublicKey(self, internal, accountNumber, chainIndex):
		result = {}
		apdu = [ self.BTCHIP_CLA, self.BTCHIP_INS_GET_WALLET_PUBLIC_KEY, \
		(btchip.CHAIN_INTERNAL if internal else btchip.CHAIN_EXTERNAL), 0x00 ]
		params = []
		writeUint32BE(accountNumber, params)
		writeUint32BE(chainIndex, params)
		apdu.append(len(params))
		apdu.extend(params)
		response = self.dongle.exchange(bytearray(apdu))
		result['publicKey'] = response[1:1 + response[0]]
		result['address'] = str(response[2 + response[0]:])
		return result

	def getTrustedInput(self, transaction, index):
		result = {}
		# Header
		apdu = [ self.BTCHIP_CLA, self.BTCHIP_INS_GET_TRUSTED_INPUT, 0x00, 0x00 ]
		params = bytearray(("%.8x" % (index)).decode('hex'))
		params.extend(transaction.version)		
		writeVarint(len(transaction.inputs), params)
		apdu.append(len(params))
		apdu.extend(params)
		self.dongle.exchange(bytearray(apdu))
		# Each input
		for trinput in transaction.inputs:
			apdu = [ self.BTCHIP_CLA, self.BTCHIP_INS_GET_TRUSTED_INPUT, 0x80, 0x00 ]
			params = bytearray(trinput.prevOut)
			writeVarint(len(trinput.script), params)
			# TODO : in the unlikely case the script is longer, cut here
			params.extend(trinput.script)
			params.extend(trinput.sequence)
			apdu.append(len(params))
			apdu.extend(params)
			self.dongle.exchange(bytearray(apdu))
		# Number of outputs
		apdu = [ self.BTCHIP_CLA, self.BTCHIP_INS_GET_TRUSTED_INPUT, 0x80, 0x00 ]
		params = []
		writeVarint(len(transaction.outputs), params)
		apdu.append(len(params))
		apdu.extend(params)
		self.dongle.exchange(bytearray(apdu))
		# Each output
		for troutput in transaction.outputs:
			apdu = [ self.BTCHIP_CLA, self.BTCHIP_INS_GET_TRUSTED_INPUT, 0x80, 0x00 ]
			params = bytearray(troutput.amount)
			writeVarint(len(troutput.script), params)
			# TODO : in the unlikely case the script is longer, cut here
			params.extend(troutput.script)
			apdu.append(len(params))
			apdu.extend(params)
			self.dongle.exchange(bytearray(apdu))
		# Locktime
		apdu = [ self.BTCHIP_CLA, self.BTCHIP_INS_GET_TRUSTED_INPUT, 0x80, 0x00, len(transaction.lockTime) ]
		apdu.extend(transaction.lockTime)
		response = self.dongle.exchange(bytearray(apdu))
		result['trustedInput'] = True
		result['value'] = response
		return result

	def startUntrustedTransaction(self, newTransaction, inputIndex, outputList, redeemScript):
		# Start building a fake transaction with the passed inputs
		apdu = [ self.BTCHIP_CLA, self.BTCHIP_INS_HASH_INPUT_START, 0x00, (0x00 if newTransaction else 0x80) ]
		params = bytearray([0x01, 0x00, 0x00, 0x00]) # default version
		writeVarint(len(outputList), params)
		apdu.append(len(params))
		apdu.extend(params)
		self.dongle.exchange(bytearray(apdu))
		# Loop for each input
		currentIndex = 0;		
		for passedOutput in outputList:
			apdu = [ self.BTCHIP_CLA, self.BTCHIP_INS_HASH_INPUT_START, 0x80, 0x00 ]	
			params = []
			script = redeemScript
			if passedOutput['trustedInput']:
				params.append(0x01)
			else:
				params.append(0x00)
			params.append(len(passedOutput['value']))
			params.extend(passedOutput['value'])
			if currentIndex <> inputIndex:
				script = bytearray()
			writeVarint(len(script), params)
			params.extend(script)
			params.extend(bytearray([0xFF, 0xFF, 0xFF, 0xFF])) # default sequence
			apdu.append(len(params))
			apdu.extend(params)
			self.dongle.exchange(bytearray(apdu))		
			currentIndex += 1

	def finalizeInput(self, outputAddress, amount, fees, changeInternal, changeAccountNumber, changeChainIndex):
		result = {}
		apdu = [ self.BTCHIP_CLA, self.BTCHIP_INS_HASH_INPUT_FINALIZE, \
		0x02, (btchip.CHAIN_INTERNAL if changeInternal else btchip.CHAIN_EXTERNAL) ]
		params = []
		params.append(len(outputAddress))
		params.extend(bytearray(outputAddress))
		writeHexAmountBE(btc_to_satoshi(str(amount)), params)
		writeHexAmountBE(btc_to_satoshi(str(fees)), params)
		writeUint32BE(changeAccountNumber, params)
		writeUint32BE(changeChainIndex, params)
		response = apdu.append(len(params))
		apdu.extend(params)
		response = self.dongle.exchange(bytearray(apdu))		
		result['confirmationNeeded'] = response[1 + response[0]] == 0x01
		result['outputData'] = response[1 : 1 + response[0]]
		return result

	def finalizeInputFull(self, outputData):
		result = {}
		offset = 0
		while (offset < len(outputData)):
			blockLength = 255
			if ((offset + blockLength) > len(outputData)):
				dataLength = len(outputData) - offset
				p1 = 0x00
			else:
				dataLength = blockLength
				p1 = 0x80
			apdu = [ self.BTCHIP_CLA, self.BTCHIP_INS_HASH_INPUT_FINALIZE_FULL, \
			p1, 0x00, dataLength ]
			apdu.extend(outputData[offset : offset + dataLength])
			response = self.dongle.exchange(bytearray(apdu))		
			offset += dataLength
		result['confirmationNeeded'] = response[0] == 0x01
		return result

	def untrustedHashSign(self, internal, accountNumber, chainIndex, pin="", lockTime=0, sighashType=0x01):
		apdu = [ self.BTCHIP_CLA, self.BTCHIP_INS_HASH_SIGN, 0x00, 0x00 ]		
		params = []
		writeUint32BE(accountNumber, params)		
		writeUint32BE(chainIndex, params)
		if internal:
			params.append(btchip.CHAIN_INTERNAL)
		else:
			params.append(btchip.CHAIN_EXTERNAL)
		params.append(len(pin))
		params.extend(bytearray(pin))
		writeUint32BE(lockTime, params)
		params.append(sighashType)
		apdu.append(len(params))
		apdu.extend(params)
		result = self.dongle.exchange(bytearray(apdu))		
		return result

	def signMessagePrepare(self, internal, accountNumber, chainIndex, message):
		result = {}
		apdu = [ self.BTCHIP_CLA, self.BTCHIP_INS_SIGN_MESSAGE, 0x00, 0x00 ]
		params = []
		writeUint32BE(accountNumber, params)		
		writeUint32BE(chainIndex, params)
		if internal:
			params.append(btchip.CHAIN_INTERNAL)
		else:
			params.append(btchip.CHAIN_EXTERNAL)
		params.append(len(message))		
		params.extend(bytearray(message))
		apdu.append(len(params))
		apdu.extend(params)
		response = self.dongle.exchange(bytearray(apdu))		
		result['confirmationNeeded'] = response[0] == 0x01
		return result

	def signMessageSign(self, pin=None):
		apdu = [ self.BTCHIP_CLA, self.BTCHIP_INS_SIGN_MESSAGE, 0x80, 0x00 ]
		params = []
		if pin is not None:
			params.append(len(pin))
			params.extend(bytearray(pin))
		else:
			params.append(0x00)
		apdu.append(len(params))
		apdu.extend(params)
		response = self.dongle.exchange(bytearray(apdu))		
		return response		

	def setup(self, operationModeFlags, featuresFlag, keyVersion, keyVersionP2SH, userPin, wipePin, keymapEncoding, seed=None, userEntropy=None, developerKey=None):
		result = {}
		apdu = [ self.BTCHIP_CLA, self.BTCHIP_INS_SETUP, 0x00, 0x00 ]
		params = [ operationModeFlags, featuresFlag, keyVersion, keyVersionP2SH ]
		params.append(len(userPin))
		params.extend(bytearray(userPin))
		if wipePin is not None:
			params.append(len(wipePin))
			params.extend(bytearray(wipePin))
		else:
			params.append(0x00)
		params.extend(keymapEncoding)
		if seed is not None:
			params.append(0x01)
			params.extend(seed)
		else:
			params.append(0x00)
			if userEntropy is not None:
				params.extend(userEntropy)
			else:
				params.extend([0] * 32)
		if developerKey is not None:
			params.append(len(developerKey))		
			params.extend(developerKey)
		else:
			params.append(0x00)
		apdu.append(len(params))
		apdu.extend(params)
		response = self.dongle.exchange(bytearray(apdu))		
		result['trustedInputKey'] = response[0:16]
		result['developerKey'] = response[16:]
		return result

	def getOperationMode(self):
		apdu = [ self.BTCHIP_CLA, self.BTCHIP_INS_GET_OPERATION_MODE, 0x00, 0x00, 0x00]
		response = self.dongle.exchange(bytearray(apdu))
		return response[0]

	def setOperationMode(self, operationMode):
		if operationMode <> btchip.OPERATION_MODE_WALLET \
			and operationMode <> btchip.OPERATION_MODE_RELAXED_WALLET \
			and operationmdoe <> btchip.OPERATION_MODE_SERVER \
			and operationMode <> btchip.OPERATION_MODE_DEVELOPER:
			raise BTChipException("Invalid operation mode")			
		apdu = [ self.BTCHIP_CLA, self.BTCHIP_INS_SET_OPERATION_MODE, 0x00, 0x00, 0x01, operationMode ]
		self.dongle.exchange(bytearray(apdu))

	def getFirmwareVersion(self):
		result = {}
		apdu = [ self.BTCHIP_CLA, self.BTCHIP_INS_GET_FIRMWARE_VERSION, 0x00, 0x00, 0x00 ]
		try:
			response = self.dongle.exchange(bytearray(apdu))
		except BTChipException as e:
			if (e.sw == 0x6985):
				response = [0x00, 0x00, 0x01, 0x04, 0x03 ]
				pass
			else:
				raise
		result['compressedKeys'] = (response[0] == 0x01)
		result['version'] = "%d.%d.%d" % (((response[1] << 8) + response[2]), response[3], response[4])
		return result				

	def getPOSSeedKey(self):
		result = {}
		apdu = [ self.BTCHIP_CLA, self.BTCHIP_INS_GET_POS_SEED, 0x01, 0x00, 0x00 ]
		return self.dongle.exchange(bytearray(apdu))

	def getPOSEncryptedSeed(self):
		result = {}
		apdu = [ self.BTCHIP_CLA, self.BTCHIP_INS_GET_POS_SEED, 0x02, 0x00, 0x00 ]
		return self.dongle.exchange(bytearray(apdu))
