# ------------------------------------------------------------------------------------------
# Copyright James A. Dooley 2021.
#
# Distributed under the MIT License.
# (See accompanying file license.md file or copy at http://opensource.org/licenses/MIT)
#
# ------------------------------------------------------------------------------------------

from microbit import pin16, sleep, button_b, display
from utime import ticks_ms, ticks_diff

from utime import sleep_us

_DEBOUNCE_DELAY = 50
_HIGH           = 1
_LOW            = 0

class Button:
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
    
def main():
    button = Button(pin16)
    
    display.clear()
    display.show('>')
    
    while True:
        if button_b.was_pressed():
            display.clear()
            break
        
        if button.is_pressed():
            print('Button Pressed')
        else:
            print('Button Not Pressed')
        sleep(500)

if __name__ == '__main__':
    main()
