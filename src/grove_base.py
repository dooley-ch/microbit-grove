# ------------------------------------------------------------------------------------------
# Copyright James A. Dooley 2021.
#
# Distributed under the MIT License.
# (See accompanying file license.md file or copy at http://opensource.org/licenses/MIT)
#
# ------------------------------------------------------------------------------------------

from microbit import sleep, i2c

i2c.init()

class GroveI2CBase:
    """
    Base class used to support Grove I2C components with the BBC Micro:bit
    """

    def __init__(self, device_address = 0x0):
        """
        Initializes an instance of the class
        """
        self._device_address = device_address
        self._device_id = 0x0
        self._probe_id()
        self._version = 0x0
        self._probe_version()
        
    def _set_register(self, address, value_1, value_2 = 0):
        """
        Writes data to the I2C bus at a given address for the
        current component
        """
        data = bytes((address, value_1, value_2))
        i2c.write(self._device_address, data)
        sleep(4)
    
    def _probe_id(self):
        """
        - Check's for the component's id number
        - Needs to be implemented by each inheriting class.
        - Called from the base constructor
        """
        pass
    
    def _probe_version(self):
        """
        - Check's for the component's firmware version number
        - Needs to be implemented by each inheriting class.
        - Called from the base constructor
        """
        pass
    
    def get_version(self):
        """
        Returns the firmware version number
        """
        return self._version
    
    def get_device_id(self):
        """
        Returns the id of the component
        """
        return self._device_id
    
    def get_device_address(self):
        """
        Returns the component address on the I2C bus
        """
        return self._device_address
    
    def get_name(self):
        """
        Returns the device name
        """
        return 'Unknown Supported Device'

    def is_present(self):
        """
        Checks if the device is present and
        returns true if it is, otherwise false.
        """
        try:
            i2c.read(self._device_address, 1)
        except OSError:
            return False
        else:
            return True
        