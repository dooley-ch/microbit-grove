# ------------------------------------------------------------------------------------------
# Copyright James A. Dooley 2021.
#
# Distributed under the MIT License.
# (See accompanying file license.md file or copy at http://opensource.org/licenses/MIT)
#
# ------------------------------------------------------------------------------------------

from microbit import sleep, i2c
from micropython import const

i2c.init()

class I2CBase:    
    def __init__(self, device_address = 0x0):
        self._device_address = device_address
        self._device_id = 0x0
        self._probe_id()
        self._version = 0x0
        self._probe_version()
        
    def _set_register(self, address, value):
        data = bytes((address, value))
        i2c.write(self._device_address, data)
        sleep(4)
    
    def _probe_id(self):
        pass
    
    def _probe_version(self):
        pass
    
    def get_version(self):
        return self._version
    
    def get_device_id(self):
        return self._device_id
    
    def get_device_address(self):
        return self._device_address
    
    def get_name(self):
        return 'Unknown Supported Device'

    def is_present(self):
        try:
            i2c.read(self._device_address, 1)
        except OSError:
            return False
        else:
            return True
        