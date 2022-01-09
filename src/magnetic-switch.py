# ------------------------------------------------------------------------------------------
# Copyright James A. Dooley 2021.
#
# Distributed under the MIT License.
# (See accompanying file license.md file or copy at http://opensource.org/licenses/MIT)
#
# ------------------------------------------------------------------------------------------

# Note although rated for 5v, it seems to work OK with power from the board

from microbit import pin16, sleep, display, button_b
from utime import ticks_ms, ticks_diff

from utime import sleep_us

_HIGH           = 1
_LOW            = 0

class MagneticSwitch:
    def __init__(self, pin):
        self._pin = pin
        
    def is_on(self):
        reading = self._pin.read_digital()        
        return (reading == _HIGH)
    
def main():
    button = MagneticSwitch(pin16)
    
    display.clear()
    display.show('>')
    
    while True:
        if button_b.was_pressed():
            display.clear()
            break
        
        if button.is_on():
            print('Switch On')
            
        sleep(100)

if __name__ == '__main__':
    main()
