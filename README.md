btchip-python
=============

Python samples for BTChip - work in progress

Requirements
-------------

This API requires cython-hidapi version 0.7.99 (at least).

To install cython-hidapi, refer to the instructions on https://github.com/trezor/cython-hidapi until a packaged version is available. Interim Debian packages have been built by Richard Ulrich at https://launchpad.net/~richi-paraeasy/+archive/ubuntu/bitcoin/ (btchip-python, hidapi and python-hidapi)

For optional BIP 39 support during dongle setup, also install https://github.com/trezor/python-mnemonic - also available as a Debian package at the previous link (python-mnemonic)

Building on Windows
--------------------

  - Download and install Python from https://www.python.org/ftp/python/2.7.8/python-2.7.8.msi
  - Download and install Python QT from http://downloads.sourceforge.net/project/pyqt/PyQt4/PyQt-4.11.1/PyQt4-4.11.1-gpl-Py2.7-Qt4.8.6-x32.exe
  - Download and install PyWin32 from http://sourceforge.net/projects/pywin32/files/pywin32/Build%20218/pywin32-218.win32-py2.7.exe/download
  - Download MinGW setup from http://sourceforge.net/projects/mingw/files/Installer/mingw-get-setup.exe/download
  - Install mingw32-gcc-g++ and mingw32-libz (dev and dll)
  - Create a /Lib/disutils/distutils.cfg file in your Python installation directory (typically /Python27) containing the following content

```
[build]
compliler=mingw32
```

  - Install distribute from https://gist.githubusercontent.com/anonymous/947191a4635cd7b7f79a/raw/36054b7f8d7b0c4c172628fd9bd16f46e53bb34b/distribute_setup.py
  - Install the dependencies by running /Python27/Scripts/easy_install.exe cython hidapi 


