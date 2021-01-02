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
This module is used to get some useful data about raspberry pi
"""

import os
import psutil
import re
import subprocess


class PI:

    def get_ram_info(self):
        """
        :return: Return RAM information (unit=kb) in a list
                 Index 0: total RAM
                 Index 1: used RAM
                 Index 2: free RAM
        """
        p = os.popen('free')
        i = 0
        while True:
            i = i + 1
            line = p.readline()
            if i == 2:
                return line.split()[1:4]

    def get_disk_space(self):
        """
        :return: # Return information about disk space as a list (unit included)
                # Index 0: total disk space
                # Index 1: used disk space
                # Index 2: remaining disk space
                # Index 3: percentage of disk used
        """
        p = os.popen("df -h /")
        i = 0
        while 1:
            i = i + 1
            line = p.readline()
            if i == 2:
                return line.split()[1:5]

    def get_cpu_usage(self):
        """
        :return: Return % of CPU used by user as a character string
        """
        return str(psutil.cpu_percent())

    def get_connected_ip_addr(self, network):
        """
        :param network: which network interface i.e. 'wlan0', 'eth0'
        :return: string of ip
        """
        cmd = "/sbin/ifconfig " + str(network) + " | grep 'inet '"
        resp = (subprocess.check_output(cmd, shell=True)).decode("utf-8")
        ip = re.search('inet (.+) netmask', resp).group(1)
        return ip

    def get_cpu_temp(self):
        """
        :return: float of cpu temp
        """
        tFile = open('/sys/class/thermal/thermal_zone0/temp')
        temp = float(tFile.read())
        cpu_temp = temp / 1000
        return cpu_temp

    def get_wifi_status(self):
        """
        :return: return list of [ssid, signal quality, signal level, signal percentage]
        """
        ssid = os.popen("iwgetid -r").read()
        ssid = ssid.rstrip("\n")

        cmd1 = "iwconfig wlan0 | grep -i quality"
        res1 = (subprocess.check_output(cmd1, shell=True))
        resp = res1.decode("utf-8")
        start = resp.index("k") + len("k")
        end = resp.index('S', start)
        strength = resp[start:end]
        signal_level = strength.replace("Quality=", "")

        dat = signal_level
        actual = int(dat[:3])
        maxx = int(dat[4:6])
        wifi_percentage = int((actual / maxx) * 100)

        start1 = resp.index("S") + len("S")
        end1 = resp.index('m', start1)
        temp = resp[start1:end1]
        level = 'S' + temp
        signal_quality = level.replace("Signal level=", "")
        return [ssid, signal_quality.strip(), signal_level.strip(), wifi_percentage]


if __name__ == '__main__':
    PI()
