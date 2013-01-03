btchip-python
=============

Python setup and samples for BTChip - how to start playing with the samples distributed @ 29c3 - for more details, check http://www.btchip.com / drop a line to contact@btchip.com

Description
-----------

Marketing version : BTChip let you secure your bitcoin private keys and use bitcoins safely in hostile environments (public PC, 
 Windows PC you forgot to update 3 years ago ...)

Technical version : BTChip is a smartcard chip performing keypair generation, signing and verification over the secp256k1 elliptic curve. Communication with the host is done over USB HID APIs. No asymmetric keys are kept on the dongle - the private keys are sent back and forth encrypted by a Triple DES context key.

A healthy amount of ISO 7816-4 (http://www.cardwerk.com/smartcards/smartcard_standard_ISO7816-4.aspx), GlobalPlatform Secure Channel (http://www.globalplatform.org) is referenced by the samples. If confused by the samples, it is recommended to check other projects for inspiration, such as GPShell - http://sourceforge.net/projects/globalplatform/files/

Getting started 
---------------

  * Verify that the following dependencies are installed
    * Cython http://cython.org
    * PyCrypto https://www.dlitz.net/software/pycrypto
  * Check out the repository.
  * Compile/Install cython-hidapi
  * Try a few samples
    * start with the -create- samples
    * sample-interoperability.py shows how to decrypt a private key knowing the context key and how to import an external private key
  * Create at least one symmetric key to encrypt the private keys (context key)
  * Modify your favorite client to support it. You can also find a sample integration into bitcoinj here http://code.google.com/r/contact-bitcoinj-btchip/ - on the following revision http://code.google.com/r/contact-bitcoinj-btchip/source/detail?r=228c010d5ad872cde58d75221bed689225de3afb

You can pull the repository dependency to cython-hidapi and hidapi with

          git submodule update --init --recursive

Linux users : you'll need to add a new udev rule to access the dongle from a non root account, described below. Also make sure to use the libusb backend for hidapi

          SUBSYSTEMS=="usb", ATTRS{idVendor}=="2581", ATTRS{idProduct}=="1807", MODE="0660", GROUP="yourgroup"

Creating a context key for non paranoid people
----------------------------------------------

The following creation mode is recommended, in order to avoid bankruptcy if the dongle is lost/broken/stolen :

  * On a trusted computer, generate random components using the generate random API of the dongle
  * Install a key containing this component
  * GPG encrypt this component to yourself, and store it where you won't lose it

However if the dongle is stolen, everyone is able to sign using your private keys (supposing they got their encrypted blobs too) and steal your coins :(

Creating a context key for paranoid people
-------------------------------------------

Proceed as before, but link this context key to an authentication key (-pin samples)

When doing this, you'll have to authenticate to the dongle by opening a Secure Channel to the authentication key before being able to use it when it's powered on (i.e. plugged in to a computer)
 

Personalization
---------------

The sample BTChip cards are initialized with a Secure Channel key in keyset 0x01, initialized to the default test value 404142434445464748494A4B4C4D4E4F for all components 

Reference transactions
----------------------

   * http://blockchain.info/tx/63edf213d775ba3d3999afcc315819ffa08143b3aeb6b2e490a18553b2aa96b4 
   * http://blockchain.info/tx/b335de5ac4390ea0f82ce07c2ae148154d199de8a5c3d3de3235f2294df1fdb2
   * http://blockchain.info/tx/68956f3d5f460b29a3ccb2ea721c704ad5e62b9832e5424d3f0aab4d32544b12

FAQ
---

  * How do I use it ?

Detach the shape starting from the center, then gently bend downward the small element labelled "clip" until it clips in place. This will make the chip large enough to fit a USB port, which is conveniently where it should go next.

  * Why not PCSC ? It's a smartcard after all 

Due to firmware size limitations and heavy recycling, it was not possible to include PCSC support in this firmware revision. 

  * The signature time is too long 

It can and will be improved in the future, and the dongle supports firmware updates.

  * How secure is it ? 

The chip is a smartcard certified platform (for the time being we'll let the potential attackers name it to avoid spoiling the game :p) and the software was designed by people who usually know what they're doing, so we don't think you'll be disappointed. However feel free to attack it. 

  * When will it go for sale ? 

The final version should be available early 2013 and cost around 1 BTC with shipping included

License
-------

  GPL v2 for all standalone code submitted - project license for integrated code


