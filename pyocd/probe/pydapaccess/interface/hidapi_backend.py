# pyOCD debugger
# Copyright (c) 2006-2013 Arm Limited
# SPDX-License-Identifier: Apache-2.0
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from .interface import Interface
from .common import filter_device_by_usage_page
from ..dap_access_api import DAPAccessIntf
from ....utility.compatibility import to_str_safe
import logging
import os
import six

log = logging.getLogger('hidapi')

try:
    import hid
except:
    if os.name == "posix" and os.uname()[0] == 'Darwin':
        log.error("cython-hidapi is required on a Mac OS X Machine")
    IS_AVAILABLE = False
else:
    IS_AVAILABLE = True

class HidApiUSB(Interface):
    """
    This class provides basic functions to access
    a USB HID device using cython-hidapi:
        - write/read an endpoint
    """

    isAvailable = IS_AVAILABLE

    def __init__(self):
        super(HidApiUSB, self).__init__()
        # Vendor page and usage_id = 2
        self.device = None

    def open(self):
        try:
            self.device.open_path(self.device_info['path'])
        except IOError as exc:
            raise six.raise_from(DAPAccessIntf.DeviceError("Unable to open device: " + str(exc)), exc)

    @staticmethod
    def get_all_connected_interfaces():
        """
        returns all the connected devices which matches HidApiUSB.vid/HidApiUSB.pid.
        returns an array of HidApiUSB (Interface) objects
        """

        devices = hid.enumerate()

        if not devices:
            log.debug("No Mbed device connected")
            return []

        boards = []

        for deviceInfo in devices:
            product_name = to_str_safe(deviceInfo['product_string'])
            if (product_name.find("CMSIS-DAP") < 0):
                # Skip non cmsis-dap devices
                continue
            
            vid = deviceInfo['vendor_id']
            pid = deviceInfo['product_id']
            
            # Perform device-specific filtering.
            if filter_device_by_usage_page(vid, pid, deviceInfo['usage_page']):
                continue

            try:
                dev = hid.device(vendor_id=vid, product_id=pid, path=deviceInfo['path'])
            except IOError as exc:
                log.debug("Failed to open USB device: %s", exc)
                continue

            # Create the USB interface object for this device.
            new_board = HidApiUSB()
            new_board.vendor_name = deviceInfo['manufacturer_string']
            new_board.product_name = deviceInfo['product_string']
            new_board.serial_number = deviceInfo['serial_number']
            new_board.vid = vid
            new_board.pid = pid
            new_board.device_info = deviceInfo
            new_board.device = dev
            boards.append(new_board)

        return boards

    def write(self, data):
        """
        write data on the OUT endpoint associated to the HID interface
        """
        for _ in range(self.packet_size - len(data)):
            data.append(0)
        #logging.debug("send: %s", data)
        self.device.write([0] + data)
        return


    def read(self, timeout=-1):
        """
        read data on the IN endpoint associated to the HID interface
        """
        return self.device.read(self.packet_size)

    def get_serial_number(self):
        return self.serial_number

    def close(self):
        """
        close the interface
        """
        log.debug("closing interface")
        self.device.close()

    def set_packet_count(self, count):
        # No interface level restrictions on count
        self.packet_count = count

    def set_packet_size(self, size):
        self.packet_size = size
