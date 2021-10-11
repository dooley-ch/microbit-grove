# ------------------------------------------------------------------------------------------
# Copyright James A. Dooley 2021.
#
# Distributed under the MIT License.
# (See accompanying file license.md file or copy at http://opensource.org/licenses/MIT)
#
# ------------------------------------------------------------------------------------------

from microbit import pin16, sleep
from utime import ticks_ms, ticks_diff

from utime import sleep_us

_DEBOUNCE_DELAY = 50
_HIGH           = 1
_LOW            = 0

class GroveButton:
    def __init__(self, pin):
        self._pin = pin
        self._button_state = None
        self._last_button_state = None
        self._last_debounce_time = None
        
    def is_pressed(self):
        reading = self._pin.read_digital()
        
        if reading != self._last_button_state:
            self._last_debounce_time = ticks_ms()
    
        if ticks_diff(ticks_ms(), self._last_debounce_time) > _DEBOUNCE_DELAY:
            if reading != self._button_state:
                self._button_state = reading
    
        self._last_button_state = reading
        
        return (self._button_state == _HIGH)
    
def demo():
    button = GroveButton(pin16)
    
    while True:
        if button.is_pressed():
            print('Button On')
        else:
            print('Button Off')
        sleep(1000)

if __name__ == '__main__':
    demo()
