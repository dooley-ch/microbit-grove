# ------------------------------------------------------------------------------------------
# Copyright James A. Dooley 2021.
#
# Distributed under the MIT License.
# (See accompanying file license.md file or copy at http://opensource.org/licenses/MIT)
#
# ------------------------------------------------------------------------------------------

# Note although rated for 5v, it seems to work OK with power from the board

from microbit import pin16, sleep
from utime import ticks_ms, ticks_diff

from utime import sleep_us

_HIGH           = 1
_LOW            = 0

class GroveMagneticSwitch:
    def __init__(self, pin):
        self._pin = pin
        
    def is_on(self):
        reading = self._pin.read_digital()        
        return (reading == _HIGH)
    
def demo():
    button = GroveMagneticSwitch(pin16)
    
    while True:
        if button.is_on():
            print('Switch On')
        else:
            print('Switch Off')
        sleep(1000)

if __name__ == '__main__':
    demo()
