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
This module is used to interface with gsm module
"""

import serial
import time


class GSM:
    def __init__(self, port, baud_rate):
        """
        Initialize the serial communication port to access gsm module
        :param port: port to be used for serial communication.
                    Use COM1, COM2, COM3 etc in case of windows
                    Use /dev/ttyUSB0 etc in case of linux based devices
        :param baud_rate: Set the appropriate baud rate.
        """
        self.gsm_serial_port = serial.Serial(port, baud_rate)
        self.ongoing_call = False

    def modem_active(self):
        """
        This checks if GSM module is working fine or not.
        This sends AT command to modem. If modem responds with OK, means modem is working fine
        Else there might be some error with modem or serial communication
        :return: True if modem is active or else False
        """
        status_cmd = 'AT\r'
        status_cmd = bytes(status_cmd, 'utf-8')
        self.gsm_serial_port.write(status_cmd)
        time.sleep(1)
        status_res = self.gsm_serial_port.read_all()
        status_res = status_res.decode('utf-8')
        if 'OK' in status_res:
            return True
        else:
            return False

    def get_signal_strength(self):
        """
        This function runs command AT+CSQ
        :return: returns tuple of signal strength
        """
        csq_cmd = "AT+CSQ\r"
        csq_cmd = bytes(csq_cmd, "utf-8")
        self.gsm_serial_port.write(csq_cmd)
        time.sleep(1)
        csq_res = self.gsm_serial_port.read_all()
        csq_res = csq_res.decode("utf-8")
        if 'OK' in csq_res:
            csq_res = csq_res.split(',')
            csq_res = csq_res[0].split(':')
            signal = int(csq_res[1].strip())
            if signal >= 20:
                return "Excellent", signal
            else:
                return "Poor", signal

    def get_modem_manufacturer(self):
        """
        Queries command AT+CGMI
        :return: string of modem manufacturer name
        """
        manufacturer_cmd = 'AT+CGMI\r'
        manufacturer_cmd = bytes(manufacturer_cmd, 'utf-8')
        self.gsm_serial_port.write(manufacturer_cmd)
        time.sleep(1)
        manufacturer_res = self.gsm_serial_port.read_all()
        manufacturer_res = manufacturer_res.decode('utf-8')
        if 'OK' in manufacturer_res:
            manufacturer_res = manufacturer_res.split('\r\n')
            return manufacturer_res[1]
        else:
            return False

    def get_modem_model_number(self):
        """
        Queries command AT+CGMM
        :return: string of modem manufacturer name
        """
        model_cmd = 'AT+CGMM\r'
        model_cmd = bytes(model_cmd, 'utf-8')
        self.gsm_serial_port.write(model_cmd)
        time.sleep(1)
        model_res = self.gsm_serial_port.read_all()
        model_res = model_res.decode('utf-8')
        if 'OK' in model_res:
            model_res = model_res.split('\r\n')
            return model_res[1]
        else:
            return False

    def get_modem_revision_number(self):
        """
        Queries command AT+CGMR
        :return: string of modem revision number
        """
        revision_cmd = 'AT+CGMR\r'
        revision_cmd = bytes(revision_cmd, 'utf-8')
        self.gsm_serial_port.write(revision_cmd)
        time.sleep(1)
        revision_res = self.gsm_serial_port.read_all()
        revision_res = revision_res.decode('utf-8')
        if 'OK' in revision_res:
            revision_res = revision_res.split(':')
            revision_res = revision_res[1].split('\r\n')
            return revision_res[0]
        else:
            return False

    def get_modem_serial_number(self):
        """
        Queries command AT+CGSN
        :return: string of modem serial number
        """
        revision_cmd = 'AT+CGSN\r'
        revision_cmd = bytes(revision_cmd, 'utf-8')
        self.gsm_serial_port.write(revision_cmd)
        time.sleep(1)
        serial_res = self.gsm_serial_port.read_all()
        serial_res = serial_res.decode('utf-8')
        if 'OK' in serial_res:
            serial_res = serial_res.split('\r\n')
            return serial_res[1]
        else:
            return False

    def get_international_subscriber_identity(self):
        """
        Queries command AT+CIMI
        :return: string of modem serial number
        """
        international_cmd = 'AT+CIMI\r'
        international_cmd = bytes(international_cmd, 'utf-8')
        self.gsm_serial_port.write(international_cmd)
        time.sleep(1)
        international_res = self.gsm_serial_port.read_all()
        international_res = international_res.decode('utf-8')
        if 'OK' in international_res:
            international_res = international_res.split('\r\n')
            return international_res[1]
        else:
            return False

    def make_call(self, number):
        """
        This function makes a call to the number
        :param number: phone number to dial
        :return: True if call was made successfully or else False
        """
        call_cmd = 'ATD' + number + ';\r'
        call_cmd = bytes(call_cmd, 'utf-8')
        self.gsm_serial_port.write(call_cmd)
        time.sleep(1)
        call_res = self.gsm_serial_port.read_all()
        call_res = call_res.decode('utf-8')
        if 'OK' in call_res:
            self.ongoing_call = True
            return True
        else:
            return False

    def make_miss_call(self, number, timeout=3):
        """
        This will make a call to given number and will cancel it after the timeout
        :param number: phone number to dial
        :param timeout: time in secs
        :return: tuple of miss call status
        """
        miss_call_cmd = 'ATD' + number + ';\r'
        miss_call_cmd = bytes(miss_call_cmd, 'utf-8')
        self.gsm_serial_port.write(miss_call_cmd)
        time.sleep(1)
        miss_call_res = self.gsm_serial_port.read_all()
        miss_call_res = miss_call_res.decode('utf-8')
        if 'OK' in miss_call_res:
            time.sleep(timeout)
            end_miss_call_cmd = 'ATH\r'
            end_miss_call_cmd = bytes(end_miss_call_cmd, 'utf-8')
            self.gsm_serial_port.write(end_miss_call_cmd)
            time.sleep(1)
            end_miss_call_res = self.gsm_serial_port.read_all()
            end_miss_call_res = end_miss_call_res.decode('utf-8')
            if 'OK' in end_miss_call_res:
                return True, "Call Missed"
            else:
                return False, "Error"
        else:
            return False, "Unable to make call"

    def end_ongoing_call(self):
        """
        This functions ends an ongoing call
        :return: True if call was canceled or else False in tuple
        """
        if not self.ongoing_call:
            return False, "No Ongoing Call"
        else:
            end_cmd = 'ATH\r'
            end_cmd = bytes(end_cmd, 'utf-8')
            self.gsm_serial_port.write(end_cmd)
            time.sleep(1)
            end_call_res = self.gsm_serial_port.read_all()
            end_call_res = end_call_res.decode('utf-8')
            if 'OK' in end_call_res:
                self.ongoing_call = False
                return True, "Call Cancelled"
            else:
                return False, "Error"


if __name__ == '__main__':
    GSM(port="COM1", baud_rate=9600)
