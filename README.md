btchip-python
=============

Python samples for BTChip - work in progress

Requirements
-------------

This API requires cython-hidapi version 0.7.99 (at least) and optionally PyUSB version 1.0.0rc1 (at least) if you plan to use the WinUSB transport.

To install cython-hidapi, refer to the instructions on https://github.com/trezor/cython-hidapi until a packaged version is available. Interim Debian packages have been built by Richard Ulrich at https://launchpad.net/~richi-paraeasy/+archive/ubuntu/bitcoin/ (btchip-python, hidapi and python-hidapi)

To install PyUSB, refer to the instructions on https://github.com/walac/pyusb until a packaged version is available. Interim Debian packages have been built by Richard Ulrich at https://launchpad.net/~richi-paraeasy/+archive/ubuntu/bitcoin/ (btchip-python and pyusb)

For optional BIP 39 support during dongle setup, also install https://github.com/trezor/python-mnemonic - also available as a Debian package at the previous link (python-mnemonic)


