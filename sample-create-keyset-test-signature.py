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

from btchip import getFirstDongle
from btchip import Dongle
from btchip import SecureChannel
from btchip import BTCHIP_PUT_KEY_USAGE_BITCOIN_PRIVATE_KEY_CONTEXT
from btchip import BTCHIP_SECURE_CHANNEL_SECURITY_LEVEL_CMAC
from btchip import BTChip


def toHex(data):             
   string= ''
   for x in range(len(data)):
     string += '%02x' % data[x]
   return string


print "Locating device ..."
dongle = getFirstDongle()
print "Open Secure Channel ..."
# Open a Secure Channel with the keyset 0x01 to be able to prepare a new key
channel = SecureChannel(dongle, 0x01, BTCHIP_SECURE_CHANNEL_SECURITY_LEVEL_CMAC, "404142434445464748494A4B4C4D4E4F", "404142434445464748494A4B4C4D4E4F", "404142434445464748494A4B4C4D4E4F")
# Create keyset 0x20 as a bitcoin context key. Only the first component of the keyset is used
print "Creating new context key ..."
channel.putKey(0x20, BTCHIP_PUT_KEY_USAGE_BITCOIN_PRIVATE_KEY_CONTEXT, "0000", "505152535455565758595A5B5C5D5E5F", "505152535455565758595A5B5C5D5E5F", "505152535455565758595A5B5C5D5E5F")

btchip = BTChip(dongle)
print "Selecting curve ..."
btchip.selectCurve()
print "Generating keypair ... please wait ~ 5 seconds"
keypair = btchip.generateKeypair(0x20)
hashToSign = "0102030405060708111213141516171821222324252627283132333435363738"
print "Signing ... please wait ~ 5 seconds"
testSign = btchip.sign(0x20, keypair[1], hashToSign)
print "Signature " + testSign
print "Verifying signature ... please wait ~ 10 seconds"
btchip.verify(keypair[0], hashToSign, testSign)
print "Signature verified"

dongle.close()

