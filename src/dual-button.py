# ------------------------------------------------------------------------------------------
# Copyright James A. Dooley 2021.
#
# Distributed under the MIT License.
# (See accompanying file license.md file or copy at http://opensource.org/licenses/MIT)
#
# ------------------------------------------------------------------------------------------

# Note: This component panel consists of two independent buttons so both signal wires are
# used. When you plug in the grove cable the outer button goes to the named pin, P16 for
# instance and the inner or closer button goes to the lesser pin, in this case P15

from microbit import pin15, pin16, sleep, display, button_b
from utime import ticks_ms, ticks_diff

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
        
        return (self._button_state == _LOW)

def main():
    green_button = Button(pin16)
    red_button = Button(pin15)
    
    display.clear()
    display.show('>')
        
    while True:
        if button_b.was_pressed():
            display.clear()
            break
        
        if green_button.is_pressed():
            print('Green Button Pressed')
            sleep(200)
            
        if red_button.is_pressed():
            print('Red Button Pressed')
            sleep(200)

if __name__ == '__main__':
    main()