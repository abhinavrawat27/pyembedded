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

    def send_sms(self, number, message):
        """
        This sends sms to given number
        :param number: phone number on which sms will be sent
        :param message: sms content
        :return: tuple of sms status
        """
        text_mode_cmd = "AT+CMGF=1\r"
        text_mode_cmd = bytes(text_mode_cmd, 'utf-8')
        self.gsm_serial_port.write(text_mode_cmd)
        time.sleep(3)
        text_mode_res = self.gsm_serial_port.read_all()
        text_mode_res = text_mode_res.decode("utf-8")
        if 'OK' in text_mode_res:
            sms_cmd = 'AT+CMGS="' + number + '"\r'
            sms_cmd = bytes(sms_cmd, 'utf-8')
            self.gsm_serial_port.write(sms_cmd)
            time.sleep(3)
            self.gsm_serial_port.reset_output_buffer()
            time.sleep(1)
            self.gsm_serial_port.write(str.encode(message + chr(26)))
            time.sleep(10)
            sms_res = self.gsm_serial_port.read_all()
            sms_res = sms_res.decode('utf-8')
            if 'OK' in sms_res:
                return True, "Message sent", sms_res
            else:
                return False, "Message not sent", sms_res
        else:
            return False, "Unable to activate sms text mode", text_mode_res

    def read_all_sms(self):
        """
        This read all sms
        :return:
        """
        read_sms_cmd = 'AT+CMGL="ALL"\r'
        read_sms_cmd = bytes(read_sms_cmd, 'utf-8')
        self.gsm_serial_port.write(read_sms_cmd)
        time.sleep(5)
        read_sms_res = self.gsm_serial_port.read_all()
        read_sms_res = read_sms_res.decode('utf-8')
        if 'OK' in read_sms_res:
            return True, read_sms_res
        else:
            return False, read_sms_res

    def read_sms_by_msg_id(self, msg_id):
        """
        This will return the sms content of the given msg id
        :param msg_id: which msg to read i.e. 1 being the 1st msg in memory
        :return: tuple of the sms content
        """
        read_msg = "AT+CMGR=" + str(msg_id) + "\r"
        read_msg = bytes(read_msg, 'utf-8')
        self.gsm_serial_port.write(read_msg)
        time.sleep(5)
        msg_res = self.gsm_serial_port.read_all()
        msg_res = msg_res.decode('utf-8')
        if 'OK' in msg_res:
            return True, msg_res
        else:
            return False, msg_res


if __name__ == '__main__':
    GSM(port="COM1", baud_rate=9600)
