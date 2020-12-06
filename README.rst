pyembedded
==========

Python library to interface basic embedded modules like RFID, GPS, GSM, LCD (16x2), DC Motor

Note that some of the hardware like RFID, GPS, GSM can directly be interfaced with Windows or Linux based machine but hardware like LCD and DC Motor will require Raspberry Pi or other simillar embedded devices.

Installation:
=============
Package can be installed via pip::

    $ pip3 install pyembedded

Verify if it is installed::

    $ import pyembedded
    $ pyembedded.__version__


RFID Usage:
===========
Run below basic code to get the rfid id

Note: Use port as 'COM1', 'COM2' etc in case of windows machine. Use port as '/dev/ttyUSB0' in case of linux based devices::

    $ from pyembedded.rfid_module.rfid import RFID
    $ rfid = RFID(port='COM3', baud_rate=9600)
    $ print(rfid.get_id())
