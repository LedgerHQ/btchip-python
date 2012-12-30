#!/usr/bin/python

#  BTChip communication APIs - contact@btchip.com
# 
#  This code is copyright (c) BTChip, All rights reserved.
#
#    This code is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This code is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#

import hid
import random
from Crypto.Cipher import DES3
from Crypto.Cipher import DES

BTCHIP_PUT_KEY_USAGE_GP = "01"
BTCHIP_PUT_KEY_USAGE_GP_AUTH = "02"
BTCHIP_PUT_KEY_USAGE_BITCOIN_PRIVATE_KEY_CONTEXT = "20"

BTCHIP_SECURE_CHANNEL_SECURITY_LEVEL_CMAC = 0x01
BTCHIP_SECURE_CHANNEL_SECURITY_LEVEL_CENC = 0x02

class InvalidSW(Exception):
   def __init__(self, value):
     self.value = value
   def __str__(self):
     return "Invalid Status Word " + '%02x' % self.value

class CryptoException(Exception):
   def __init__(self, value):
     self.value = value
   def __str__(self):
     return "Crypto exception " + self.value

class Dongle():
    def __init__(self, hid):
        self.hid = hid

    def toBinaryPad(self, data):
        '''Pad a block sent to the dongle to the size of the HID exchanged data block'''
        output= []
        x = 0
        i = 0
        output.append(0)
        while ((x < len(data)) and (i < 64)):
           output.append(int(data[x:x + 2],16))
           x += 2
           i += 1
        while i < 64:
           output.append(0)
           i += 1
        return output

    def exchangeApdu(self, apdu, status=0x9000):        
       '''Send an APDU to the dongle and get a response'''
       #print "=> " + apdu
       # Send all data split in 64 bytes blocks
       paddedApdu = self.toBinaryPad(apdu)
       self.hid.write(paddedApdu)
       remaining = int(apdu[8:10], 16) + 5
       offset = 64
       remaining = remaining - (64)
       while remaining > 0:
          if remaining > 64:
             blockLength = 64
          else:
             blockLength = remaining
          paddedApdu = self.toBinaryPad(apdu[offset * 2 : (offset + remaining) * 2])
          self.hid.write(paddedApdu)
          offset = offset + blockLength
          remaining = remaining - blockLength
       # Read all response components split in 64 bytes blocks
       result = self.hid.read(65)
       dataLength = 0
       if result[0] == 0x61: # response data available
        dataLength = result[1]
        if dataLength > 62: # 64 bytes read, 2 bytes SW first on the first command
            remaining = dataLength - 62
            while remaining != 0:
                if remaining > 64:
                   blockLength = 64
                else:
                   blockLength = remaining  
                result = result + self.hid.read(65)
                remaining = remaining - blockLength;
        readSW = (result[dataLength + 2] << 8) + (result[dataLength + 3])
       else: # no response data available, read the SW immediately
        readSW = (result[0] << 8) + (result[1])
       if readSW != status:
        raise InvalidSW(readSW)
       return result[2:dataLength + 2]

    def close(self):
        self.hid.close()


class SecureChannel():

    def toBinary(self, string):
        output = []
        x= 0
        while x < len(string):
            output.append(int(string[x:x + 2],16))
            x += 2
        return output
    
    def toBinaryDES(self,string):
        output= ''
        x= 0
        while x < len(string):
            output += chr(int(string[x:x + 2],16))
            x += 2
        return output

    def toHexDES(self, data):
        string= ''
        for x in range(len(data)):
            string += '%02x' % ord(data[x])
        return string

    def derive(self, keyHex, deriveData, sequenceCounter):
        '''Derive session keys for the given diversifier and sequence counter'''
        data = deriveData + sequenceCounter + "000000000000000000000000"
        des = DES3.new(self.toBinaryDES(keyHex), DES3.MODE_CBC, self.toBinaryDES("0000000000000000"))
        return self.toHexDES(des.encrypt(self.toBinaryDES(data)))

    def signSEnc(self, data):
        '''Sign data using the ENC session key'''
        dataToSign = data + "8000000000000000"
        des = DES3.new(self.toBinaryDES(self.sencKey), DES3.MODE_CBC, self.toBinaryDES("0000000000000000"))
        res = des.encrypt(self.toBinaryDES(dataToSign))
        return self.toHexDES(res[16:])

    def retailMac(self, data):
        '''Compute the Retail MAC for an APDU'''
        paddingSize = 8 - ((len(data) / 2) % 8)
        workData = data + "8000000000000000"[0:paddingSize * 2]
        des = DES.new(self.toBinaryDES(self.cmacKey[0:16]), DES.MODE_CBC, self.toBinaryDES("0000000000000000"))
        res = des.encrypt(self.toBinaryDES(workData))
        lastBlock = res[len(res) - 8:]
        des = DES.new(self.toBinaryDES(self.cmacKey[16:32]), DES.MODE_ECB)
        lastBlock = des.decrypt(lastBlock)
        des = DES.new(self.toBinaryDES(self.cmacKey[0:16]), DES.MODE_ECB)
        return self.toHexDES(des.encrypt(lastBlock))

    def encryptEnc(self, data):
        '''Encrypt APDU command using the ENC session key'''
        paddingSize = 8 - ((len(data) / 2) % 8)
        workData = data + "8000000000000000"[0:paddingSize * 2]
        des = DES3.new(self.toBinaryDES(self.sencKey), DES.MODE_CBC, self.toBinaryDES("0000000000000000"))
        return self.toHexDES(des.encrypt(self.toBinaryDES(workData)))

    def wrap(self, apdu):
        '''Wrap an APDU over the Secure Channel'''
        securityLevel = self.securityLevel
        if not self.sessionOpen:
            securityLevel = 0x01 # c-mac only forced
        workApdu = self.toBinary(apdu)
        workApdu[0] = ((workApdu[0] & 0xfc) | 0x04)            
        workApdu[4] = workApdu[4] + 8
        workApdu = toHex(workApdu)        
        if self.sessionOpen:
           workApduForMac = self.cmac + workApdu
        else:
           workApduForMac = workApdu
        if (securityLevel & 0x01)  != 0:           
           self.cmac = self.retailMac(workApduForMac)
        if (securityLevel & 0x02)  != 0:
            apduData = self.encryptEnc(apdu[10:])
            updatedDataLength = len(apduData) / 2
            if (securityLevel & 0x01)  != 0:
                updatedDataLength = updatedDataLength + 8
            workApdu = workApdu[0:8] + '%02x' % updatedDataLength + apduData
        if (securityLevel & 0x01)  != 0:                       
           workApdu = workApdu + self.cmac
        self.sessionOpen = True
        return workApdu

    def __init__(self, dongle, keysetVersion, securityLevel, encHex, macHex, dekHex):
        '''Perform the Secure Channel initialization with INITIALIZE UPDATE / EXTERNAL AUTHENTICATE'''
        self.dongle = dongle
        hostChallenge = ""
        # Prepare INITIALIZE UPDATE / EXTERNAL AUTHENTICATE
        for x in range(8):
           hostChallenge += '%02x' % int(random.uniform(0, 0xff))
        res = self.dongle.exchangeApdu("8050" + '%02x' % keysetVersion + "0008" + hostChallenge)
        cardChallenge = toHex(res[12:20])
        cardCryptogram = toHex(res[20:28])
        sequenceCounter = toHex(res[12:14])
        self.sencKey = self.derive(encHex, "0182", sequenceCounter)
        computedCardCryptogram = self.signSEnc(hostChallenge + cardChallenge)
        if computedCardCryptogram != cardCryptogram:
            raise CryptoException("Invalid card cryptogram")
        hostCryptogram = self.signSEnc(cardChallenge + hostChallenge)
        self.cmacKey = self.derive(macHex, "0101", sequenceCounter)
        self.sdekKey = self.derive(dekHex, "0181", sequenceCounter)
        self.securityLevel = securityLevel
        self.sessionOpen = False
        externalAuthenticate = self.wrap("8082" + '%02x' % securityLevel + "0008" + hostCryptogram)
        self.dongle.exchangeApdu(externalAuthenticate)

    def exchangeApdu(self, apdu, status=0x9000):
        '''Send an APDU over the Secure Channel'''
        return self.dongle.exchangeApdu(self.wrap(apdu), status)

    def encryptData(self, data):
        '''Encrypt APDU data using the DEK session key'''
        des = DES3.new(self.toBinaryDES(self.sdekKey), DES3.MODE_ECB)
        res = des.encrypt(self.toBinaryDES(data))
        return self.toHexDES(res)

    def computeKCV(self, data):
        '''Compute a KCV for the PUT KEY command'''
        des = DES3.new(self.toBinaryDES(data), DES3.MODE_ECB)
        res = des.encrypt(self.toBinaryDES("0000000000000000"))
        return self.toHexDES(res[0:3])

    def putKey(self, keysetVersion, keysetUsage, keysetAccess, encHex, macHex, dekHex):
        '''PUT KEY command : Create or update a keyset on the dongle'''
        data = '%02x' % keysetVersion
        data = data + "ff8010" + self.encryptData(encHex) + "03" + self.computeKCV(encHex)
        data = data + "01" + keysetUsage + "02" + keysetAccess
        data = data + "ff8010" + self.encryptData(macHex) + "03" + self.computeKCV(macHex)
        data = data + "01" + keysetUsage + "02" + keysetAccess
        data = data + "ff8010" + self.encryptData(dekHex) + "03" + self.computeKCV(dekHex)
        data = data + "01" + keysetUsage + "02" + keysetAccess
        apdu = "80d8" + '%02x' % keysetVersion + "81" + '%02x' % (len(data) / 2) + data
        self.exchangeApdu(apdu)

class BTChip():
    def __init__(self, dongle):
        self.dongle = dongle

    def generateRandom(self, size):
        '''Return random data bytes using the dongle generator'''
        res = self.dongle.exchangeApdu("d0240000" + '%02x' % size)
        return toHex(res)

    def selectCurve(self, fileId=0xb1c0):
        '''Select the file containing the curve parameters to use. By default use 0xb1c0 containing secp256k1 parameters'''
        res = self.dongle.exchangeApdu("80a4000002" + '%04x' % fileId)
        return toHex(res)

    def generateKeypair(self, contextKeysetVersion):
        '''Generate a keypair given an encryption key context pointing to a key with BTCHIP_PUT_KEY_USAGE_BITCOIN_PRIVATE_KEY_CONTEXT usage. Returns the public key as first element, the encrypted private key as second element'''
        out = [];
        res = self.dongle.exchangeApdu("e020000002" + '%02x' % contextKeysetVersion + "00") 
        publicKeySize = res[0]
        out.append(toHex(res[1:1 + publicKeySize]))
        out.append(toHex(res[1 + publicKeySize + 1:]))
        return out

    def importPrivateKey(self, contextKeysetVersion, privateComponent):
        '''Import an existing private key. Returns the encrypted private key'''
        apdu = "e0208000" + '%02x' % (len(privateComponent) / 2 + 2) + '%02x' % contextKeysetVersion + "00"
        apdu = apdu + privateComponent
        return toHex(self.dongle.exchangeApdu(apdu))

    def sign(self, contextKeysetVersion, privateKey, hashToSign):
        '''Sign a hash using the provided encrypted private key and associated encryption key context pointing to a key with BTCHIP_PUT_KEY_USAGE_BITCOIN_PRIVATE_KEY_CONTEXT usage'''
        apdu = "e0400000" + '%02x' % (len(privateKey) / 2 + len(hashToSign) / 2 + 2)
        apdu = apdu + '%02x' % contextKeysetVersion
        apdu = apdu + '%02x' % (len(privateKey) / 2)
        apdu = apdu + privateKey
        apdu = apdu + hashToSign
        return toHex(self.dongle.exchangeApdu(apdu))

    def verify(self, publicKey, hashToVerify, signature):
        '''Verify a signature using the provided public key, hash and signature data'''
        apdu = "e0408000" + '%02x' % (len(publicKey) / 2 + len(hashToVerify) / 2 + len(signature) / 2 + 2)
        apdu = apdu + '%02x' % (len(publicKey) / 2)
        apdu = apdu + publicKey
        apdu = apdu + '%02x' % (len(hashToVerify) / 2)
        apdu = apdu + hashToVerify
        apdu = apdu + signature
        return self.dongle.exchangeApdu(apdu)

def toHex(data):             
    string= ''
    for x in range(len(data)):
       string += '%02x' % data[x]
    return string

def getFirstDongle():
    '''Convenience method to return the first available dongle'''
    # Fugly. Should get interface number 1, but this field is not exported in the default cython-hidapi releases
    # in the meantime the different implementations seem to enumerate the interfaces in the right order
    counter = 0
    for device in hid.enumerate(0x2581, 0x1807):
       counter = counter + 1
       if counter == 2:        
	  path = device['path']
          device = hid.device()
          device.open_path(path)
          dongle = Dongle(device)
          return dongle
    return None
