btchip-python
=============

Python setup and samples for BTChip - how to start playing with the samples distributed @ 29c3 - for more details, drop a line to contact@btchip.com

.. contents::

Description
-----------

Marketing version : BTChip let you secure your bitcoin private keys and use bitcoins safely in hostile environments (public PC, 
 Windows PC you forgot to update 3 years ago ...)

Technical version : BTChip is a smartcard chip performing keypair generation, signing and verification over the secp256k1 elliptic curve. Communication with the host is done over USB HID APIs. No asymmetric keys are kept on the dongle - the private keys are sent back encrypted by a Triple DES context key.

A healthy amount of ISO 7816-4 (http://www.cardwerk.com/smartcards/smartcard_standard_ISO7816-4.aspx), GlobalPlatform Secure Channel (http://www.globalplatform.org) is referenced by the samples. If confused by the samples, it is recommended to check other projects for inspiration, such as GPShell - http://sourceforge.net/projects/globalplatform/files/

Getting started 
---------------

  * Check out the repository
  * Compile cython-hidapi
  * Create a symmetric key to encrypt the private keys (context key)
  * Try a few samples
  * Modify your favorite client to support it

Linux users : you'll need to add a new udev rule to access the dongle from a non root account::

  SUBSYSTEMS=="usb", ATTRS{idVendor}=="2581", ATTRS{idProduct}=="1807", MODE="0660", GROUP="yourgroup"

Creating a context key for non paranoid people
----------------------------------------------

The following creation mode is recommended, in order to avoid bankruptcy if the dongle is lost/broken/stolen :

  * On a trusted computer, generate random components using the generate random API of the dongle
  * Install a key containing this component
  * GPG encrypt this component to yourself, and keep it away

If the dongle is stolen, everyone is able to sign using your private keys and steal your coins :(

Creating a context key for paranoid people
-------------------------------------------

Proceed as before, but link this context key to an authentication key (-pin samples)

When doing this, you'll have to authenticate to the dongle by opening a Secure Channel to the authentication key before being able to use it when it's powered on (i.e. plugged in to a computer)
 

Personalization
---------------

The sample BTChip cards are initialized with a Secure Channel key in keyset 0x01, initialized to the default test value 404142434445464748494A4B4C4D4E4F for all components 

License
-------

  GPL v2 for all code submitted


