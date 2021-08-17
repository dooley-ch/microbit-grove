# ------------------------------------------------------------------------------------------
# Copyright James A. Dooley 2021.
#
# Distributed under the MIT License.
# (See accompanying file license.md file or copy at http://opensource.org/licenses/MIT)
#
# ------------------------------------------------------------------------------------------

from microbit import *
from grove_base import GroveI2CBase

_SIX_POSITION_DIP_SWITCH  = 0x03

_GET_DEV_ID               = 0x00
_GET_DATA                 = 0x01
_EVENT_MODE               = 0x02
_BLOCK_MODE               = 0x03
_FIRMWARE_GET_VER         = 0xE2

_PID_MULTI_SWITCH         = 0x2886
_PID_5_WAY_TACTILE_SWITCH = 0x0002
_PID_6_POS_DIP_SWITCH     = 0x0003

class GroveSixPositionDipSwitch(GroveI2CBase):
    """
    This class supports the Grove 6-Position DIP Switch.
    https://www.seeedstudio.com/Grove-6-Position-DIP-Switch.html
    """
    def __init__(self):
        GroveI2CBase.__init__(self, _SIX_POSITION_DIP_SWITCH)
        self._set_register(_EVENT_MODE, True)
        self._last_read = None        
    
    def get_name(self):
        """
        Returns the name of the component
        """
        return '6 Position Dip Switch'
    
    def is_button_1_on(self):
        """
        Returns true if the button on the switch is set, otherwise false
        """
        return self._last_read[0] == 0x0
    
    def is_button_2_on(self):
        """
        Returns true if the button on the switch is set, otherwise false
        """        
        return self._last_read[1] == 0x0

    def is_button_3_on(self):
        """
        Returns true if the button on the switch is set, otherwise false
        """        
        return self._last_read[2] == 0x0

    def is_button_4_on(self):
        """
        Returns true if the button on the switch is set, otherwise false
        """        
        return self._last_read[3] == 0x0

    def is_button_5_on(self):
        """
        Returns true if the button on the switch is set, otherwise false
        """        
        return self._last_read[4] == 0x0

    def is_button_6_on(self):
        """
        Returns true if the button on the switch is set, otherwise false
        """        
        return self._last_read[5] == 0x0

    def has_changed(self):
        """
        Indicates if the switch settings have changed since the
        last time they were read.
        """
        return self._read_read()
    
    def get_value(self):
        """
        Returns an integer value based on the switch settings
        """
        return int.from_bytes(self._last_read, 'big')
            
    def _probe_id(self):
        """
        Check's for the component's id number
        """
        ID_LEN = 4
        
        for tr in range(4):
            self._set_register(_GET_DEV_ID, 0)
            v = i2c.read(self._device_address, ID_LEN)
            
            id = 0
            for i in range(ID_LEN):
                id = (id >> 8) | (int(v[i]) << 24)
            
            if (id >> 16) == _PID_MULTI_SWITCH:
                if (id & 0xFFFF) == 0x0003:
                    self._device_id = hex(id)
                    return
                
        raise Exception('Device not found: ' + self.get_name())
    
    def _probe_version(self):
        """
        Check's for the component's firmware version number
        """
        VER_LEN = 10
        
        if not self._device_id:
            return 0
        
        self._set_register(_FIRMWARE_GET_VER, 0)
        v = i2c.read(self._device_address, VER_LEN)

        version = v[6] - ord('0')
        version = version * 10 + (v[8] - ord('0'))
        
        self._version = version
        
    def _read_read(self):
        """
        Reads the dip switch settings from the component
        """
        DATA_LEN = 4
        NUM_BUTTONS = 6
        SIZE = DATA_LEN + NUM_BUTTONS
        
        if not self._device_id:
            return None
        
        sleep(5) # ensure method is not called to quickly in a loop
        
        self._set_register(_GET_DATA, 0)
        v = i2c.read(self._device_address, SIZE)
        # print("Data = {}".format(str(v)))
        v = v[DATA_LEN:]
        
        if v == self._last_read:
            return False
        
        self._last_read = v
        
        return True
    
def main():
    """
    Demo for the class
    """
    display.clear()

    dipSwitch = GroveSixPositionDipSwitch()

    print('Device Name:', dipSwitch.get_name())
    print('Device Id:', dipSwitch.get_device_id())
    print('Device Address:', dipSwitch.get_device_address())
    print('Firmware:', dipSwitch.get_version())


    while True:
        if dipSwitch.has_changed():
            print()
            print('Button one:', dipSwitch.is_button_1_on())
            print('Button two:', dipSwitch.is_button_2_on())
            print('Button three:', dipSwitch.is_button_3_on())
            print('Button four:', dipSwitch.is_button_4_on())
            print('Button five:', dipSwitch.is_button_5_on())
            print('Button six:', dipSwitch.is_button_6_on())
            print()
            print('Value:', dipSwitch.get_value())

if __name__ == '__main__':
    main()