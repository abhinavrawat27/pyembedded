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
This module reads and process the GGPA packet received from GPS module.
It returns useful data like, lat, long, time, satellite etc
"""

import serial


class GPS:
    def __init__(self, port, baud_rate):
        """
        Initialize the serial communication port to access gps module
        :param port: port to be used for serial communication.
                    Use COM1, COM2, COM3 etc in case of windows
                    Use /dev/ttyUSB0 etc in case of linux based devices
        :param baud_rate: Set the appropriate baud rate.
        """
        self.gps_serial_port = serial.Serial(port, baud_rate)

    def get_lat_long(self):
        """
        This function reads and process the GPGGA packet & return lat long
        :return: tuple of lat & long
        """
        s = self.gps_serial_port.read(500)
        s = s.decode('utf-8')
        data = s.splitlines()
        for i in range(len(data)):
            d = data[i].split(',')
            if d[0] == "$GPGGA" and len(d) == 15:
                lat = float(d[2]) / 100
                long = float(d[4]) / 100
                return lat, long

    def get_time(self):
        """
        This function reads and process the GPGGA packet & return time value as hh.mm
        :return: str time value as hh.mm
        """
        s = self.gps_serial_port.read(500)
        s = s.decode('utf-8')
        data = s.splitlines()
        for i in range(len(data)):
            d = data[i].split(',')
            if d[0] == "$GPGGA" and len(d) == 15:
                time_val = int(float(d[1]) / 100)
                time_val = time_val / 100
                return time_val

    def get_quality_indicator(self):
        """
        This function reads and process the GPGGA packet & return quality indicator
        :return: str value of quality indicator as below:
        1 = Uncorrected coordinate
        2 = Differentially correct coordinate (e.g., WAAS, DGPS)
        4 = RTK Fix coordinate (centimeter precision)
        5 = RTK Float (decimeter precision.
        """
        s = self.gps_serial_port.read(500)
        s = s.decode('utf-8')
        data = s.splitlines()
        for i in range(len(data)):
            d = data[i].split(',')
            if d[0] == "$GPGGA" and len(d) == 15:
                return d[6]

    def get_no_of_satellites(self):
        """
        This function reads and process the GPGGA packet & return no of satellite
        :return: str value as no of satellite
        """
        s = self.gps_serial_port.read(500)
        s = s.decode('utf-8')
        data = s.splitlines()
        for i in range(len(data)):
            d = data[i].split(',')
            if d[0] == "$GPGGA" and len(d) == 15:
                return d[7]

    def get_raw_data(self):
        """
        :return: returns raw data of ggpa packet
        """
        s = self.gps_serial_port.read(500)
        s = s.decode('utf-8')
        data = s.splitlines()
        for i in range(len(data)):
            d = data[i].split(',')
            if d[0] == "$GPGGA" and len(d) == 15:
                return d


if __name__ == '__main__':
    GPS(port="COM1", baud_rate=9600)
