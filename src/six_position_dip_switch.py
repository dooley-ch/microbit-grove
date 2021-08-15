# ------------------------------------------------------------------------------------------
# Copyright James A. Dooley 2021.
#
# Distributed under the MIT License.
# (See accompanying file license.md file or copy at http://opensource.org/licenses/MIT)
#
# ------------------------------------------------------------------------------------------

from microbit import i2c
from micropython import const
from grove import I2CBase

#
# Device Id = 0x03 -> b'\x00\x00\x00\x00\x00\x00\x01\x01'
# Device Id Address = 0x00 -> b'\x00\x00\x00\x00\x00\x00\x00\x00'
# Firmware Address = 0xE2 -> b'\x01\x01\x01\x00\x00\x00\x01\x00'
# Block Mode = 0x03 -> b'\x00\x00\x00\x00\x00\x00\x01\x01'
# Data Address = 0x01 -> b'\x00\x00\x00\x00\x00\x00\x00\x01'
#

class SixPositionDipSwitch(I2CBase):
    _SIX_POSITION_DIP_SWITCH  = 0x03
    
    _GET_DEV_ID               = 0x00
    _GET_DATA                 = 0x01
    _EVENT_MODE               = 0x02
    _BLOCK_MODE               = 0x03
    _FIRMWARE_GET_VER         = 0xE2

    _PID_MULTI_SWITCH         = 0x2886
    _PID_5_WAY_TACTILE_SWITCH = 0x0002
    _PID_6_POS_DIP_SWITCH     = 0x0003
    
    def __init__(self):
        I2CBase.__init__(self, SixPositionDipSwitch._SIX_POSITION_DIP_SWITCH)
        self._set_register(self._BLOCK_MODE, True)
        self.data_read()
        
    def _probe_id(self):
        ID_LEN = 4
        
        for tr in range(4):
            self._set_register(self._GET_DEV_ID, 0)
            v = i2c.read(self._device_address, ID_LEN)
            
            id = 0
            for i in range(ID_LEN):
                id = (id >> 8) | (int(v[i]) << 24)
            
            if (id >> 16) == self._PID_MULTI_SWITCH:
                if (id & 0xFFFF) == 0x0003:
                    self._device_id = hex(id)
                    return
                
        raise Exception('Device not found: ' + self.get_name())
    
    def get_name(self):
        return '6 Position Dip Switch'
    
    def isButtonOneOn(self):
        return self.dip_1
    
    def isButtonTwoOn(self):
        return self.dip_2

    def isButtonThreeOn(self):
        return self.dip_3

    def isButtonFourOn(self):
        return self.dip_4

    def isButtonFiveOn(self):
        return self.dip_5

    def isButtonSixOn(self):
        return self.dip_6

    def _probe_version(self):
        VER_LEN = 10
        
        if not self._device_id:
            return 0
        
        self._set_register(self._FIRMWARE_GET_VER, 0)
        v = i2c.read(self._device_address, VER_LEN)

        version = v[6] - ord('0')
        version = version * 10 + (v[8] - ord('0'))
        
        self._version = version
        
    def data_read(self):
        DATA_LEN = 4
        NUM_BUTTONS = 6
        SIZE = DATA_LEN + NUM_BUTTONS
        
        if not self._device_id:
            return None
        
        self._set_register(self._GET_DATA, 0)
        v = i2c.read(self._device_address, SIZE)
        v = v[DATA_LEN:]
        
        self.dip_1 = v[0] == 0x0
        self.dip_2 = v[1] == 0x0
        self.dip_3 = v[2] == 0x0
        self.dip_4 = v[3] == 0x0
        self.dip_5 = v[4] == 0x0
        self.dip_6 = v[5] == 0x0
    