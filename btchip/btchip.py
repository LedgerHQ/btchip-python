"""
*******************************************************************************    
*   BTChip Bitcoin Hardware Wallet C test interface
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

	def __init__(self, dongle):
		self.dongle = dongle

	def verifyPin(self, pin):
		apdu = [ self.BTCHIP_CLA, self.BTCHIP_INS_VERIFY_PIN, 0x00, 0x00, len(pin) ]
		apdu.extend(pin)
		self.dongle.exchange(bytearray(apdu))

	def getWalletPublicKey(self, internal, accountNumber, chainIndex):
		result = {}
		apdu = [ self.BTCHIP_CLA, self.BTCHIP_INS_GET_WALLET_PUBLIC_KEY, (btchip.CHAIN_INTERNAL if internal else btchip.CHAIN_EXTERNAL), 0x00 ]
		params = bytearray(("%.8x%.8x" % (accountNumber, chainIndex)).decode('hex'))
		apdu.append(len(params))
		apdu.extend(params)
		response = self.dongle.exchange(bytearray(apdu))
		result['publicKey'] = response[1:1 + response[0]]
		result['address'] = str(response[2 + response[0]:])
		return result

	def getTrustedInput(self, transaction, index):
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
		return response

	def getPOSSeedKey(self):
		result = {}
		apdu = [ self.BTCHIP_CLA, self.BTCHIP_INS_GET_POS_SEED, 0x01, 0x00, 0x00 ]
		return self.dongle.exchange(bytearray(apdu))

	def getPOSEncryptedSeed(self):
		result = {}
		apdu = [ self.BTCHIP_CLA, self.BTCHIP_INS_GET_POS_SEED, 0x02, 0x00, 0x00 ]
		return self.dongle.exchange(bytearray(apdu))
