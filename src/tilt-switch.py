# ------------------------------------------------------------------------------------------
# Copyright James A. Dooley 2021.
#
# Distributed under the MIT License.
# (See accompanying file license.md file or copy at http://opensource.org/licenses/MIT)
#
# ------------------------------------------------------------------------------------------

from microbit import pin16, sleep, button_b, display, Image
from utime import ticks_ms, ticks_diff

_LOW            = 0
_HIGH           = 1
_DEBOUNCE_DELAY = 50

class TiltSwitch:
    def __init__(self, pin):
        self._pin = pin
        self._state = None
        self._last_state = None
        self._last_debounce_time = None
        
    def is_on(self):
        reading = self._pin.read_digital()
        
        if reading != self._last_state:
            self._last_debounce_time = ticks_ms()
    
        if ticks_diff(ticks_ms(), self._last_debounce_time) > _DEBOUNCE_DELAY:
            if reading != self._state:
                self._state = reading
    
        self._last_state = reading
        
        return self._state == _LOW

def main():
    switch = TiltSwitch(pin16)

    display.clear()
    display.show('>')
    
    while True:
        if button_b.was_pressed():
            display.clear()
            break
        
        if switch.is_on():
            print('Is On')
        else:
            print('Is Off')
             
        sleep(100)
        
if __name__ == '__main__':
    main()
