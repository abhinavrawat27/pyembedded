"""
# Copyright 2020 ABHINAV RAWAT
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
"""
This module read and process the serial data and returns the RFID ID
"""

import serial


class RFID:
    def __init__(self, port, baud_rate):
        """
        Initialize the serial communication port to access rfid module
        :param port: port to be used for serial communication.
                    Use COM1, COM2, COM3 etc in case of windows
                    Use /dev/ttyUSB0 etc in case of linux based devices
        :param baud_rate: Set the appropriate baud rate.
        """
        self.rfid_serial_port = serial.Serial(port, baud_rate)

    def get_id(self):
        """
        This function reads the data from the rfid module
        and returns the 12char of the rfid id
        :return: rfid id
        """
        id_num = []
        i = 0
        while True:
            serial_data = self.rfid_serial_port.read()
            data = serial_data.decode('utf-8')
            i = i + 1
            if i == 12:
                i = 0
                ID = "".join(map(str, id_num))
                return ID
            else:
                id_num.append(data)


if __name__ == '__main__':
    RFID(port="COM1", baud_rate=9600)
