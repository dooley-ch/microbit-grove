# ------------------------------------------------------------------------------------------
# Copyright James A. Dooley 2021.
#
# Distributed under the MIT License.
# (See accompanying file license.md file or copy at http://opensource.org/licenses/MIT)
#
# ------------------------------------------------------------------------------------------

from microbit import sleep, i2c

_DEFAULT_ADDRESS = 0x03
_GET_DATA        = 0x01
_EVENT_MODE      = 0x02
_BLOCK_MODE      = 0x03
_SWITCH_ON       = 0x00

class SixPositionDipSwitch:
    def __init__(self):
        self._device_address = _DEFAULT_ADDRESS
        self._data = None
        
    def read_device(self):
        DATA_LEN = 4
        NUM_BUTTONS = 6
        BYTES_TO_READ = DATA_LEN + NUM_BUTTONS
        
        data = bytes((_GET_DATA, 0, 0))
        i2c.write(self._device_address, data)
        
        v = i2c.read(self._device_address, BYTES_TO_READ)
        v = v[DATA_LEN:]
        # print("Data = {}".format(str(self._data)))
        
        if self._data == v:
            return False
        
        self._data = v
        return True

    def is_button_1_on(self):
        return self._data[0] == _SWITCH_ON
    
    def is_button_2_on(self):
        return self._data[1] == _SWITCH_ON

    def is_button_3_on(self):
        return self._data[2] == _SWITCH_ON

    def is_button_4_on(self):
        return self._data[3] == _SWITCH_ON

    def is_button_5_on(self):
        return self._data[4] == _SWITCH_ON

    def is_button_6_on(self):
        return self._data[5] == _SWITCH_ON

def print_status(switches):
    if switches.is_button_1_on():
        print("Button 1: ON")
    else:
        print("Button 1: OFF")
        
    if switches.is_button_2_on():
        print("Button 2: ON")
    else:
        print("Button 2: OFF")
        
    if switches.is_button_3_on():
        print("Button 3: ON")
    else:
        print("Button 3: OFF")
        
    if switches.is_button_4_on():
        print("Button 4: ON")
    else:
        print("Button 4: OFF")
        
    if switches.is_button_5_on():
        print("Button 5: ON")
    else:
        print("Button 5: OFF")
        
    if switches.is_button_6_on():
        print("Button 6: ON")
    else:
        print("Button 6: OFF")
        
def main():
    switches = SixPositionDipSwitch()
    
    while True:
        if switches.read_device():
            print("")
            print_status(switches)
        sleep(2)
    
if __name__ == '__main__':
    main()
