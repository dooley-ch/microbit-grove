# ------------------------------------------------------------------------------------------
# Copyright James A. Dooley 2021.
#
# Distributed under the MIT License.
# (See accompanying file license.md file or copy at http://opensource.org/licenses/MIT)
#
# ------------------------------------------------------------------------------------------

from microbit import i2c, sleep
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
    def __init__(self):
        GroveI2CBase.__init__(self, _SIX_POSITION_DIP_SWITCH)
        self._set_register(_EVENT_MODE, True)
        self._last_read = None        
    
    def get_name(self):
        return '6 Position Dip Switch'
    
    def is_button_1_on(self):
        return self._last_read[0] == 0x0
    
    def is_button_2_on(self):
        return self._last_read[1] == 0x0

    def is_button_3_on(self):
        return self._last_read[2] == 0x0

    def is_button_4_on(self):
        return self._last_read[3] == 0x0

    def is_button_5_on(self):
        return self._last_read[4] == 0x0

    def is_button_6_on(self):
        return self._last_read[5] == 0x0

    def has_changed(self):
        return self._read_read()
    
    def get_value(self):
        return int.from_bytes(self._last_read, 'big')
            
    def _probe_id(self):
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
        VER_LEN = 10
        
        if not self._device_id:
            return 0
        
        self._set_register(_FIRMWARE_GET_VER, 0)
        v = i2c.read(self._device_address, VER_LEN)

        version = v[6] - ord('0')
        version = version * 10 + (v[8] - ord('0'))
        
        self._version = version
        
    def _read_read(self):
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