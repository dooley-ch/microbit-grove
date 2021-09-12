# ------------------------------------------------------------------------------------------
# Copyright James A. Dooley 2021.
#
# Distributed under the MIT License.
# (See accompanying file license.md file or copy at http://opensource.org/licenses/MIT)
#
# ------------------------------------------------------------------------------------------

_LOW            = 0
_HIGH           = 1
_DEBOUNCE_DELAY = 50

from microbit import pin16, sleep, button_b, display
from utime import ticks_ms, ticks_diff

class GroveTouchSensor:
    def __init__(self, pin):
        self._pin = pin
        self._state = None
        self._last_state = None
        self._last_debounce_time = None
        
    def is_pressed(self):
        reading = self._pin.read_digital()
        
        if reading != self._last_state:
            self._last_debounce_time = ticks_ms()
    
        if ticks_diff(ticks_ms(), self._last_debounce_time) > _DEBOUNCE_DELAY:
            if reading != self._state:
                self._state = reading
    
        self._last_state = reading
        
        return (self._state == _HIGH)

def demo():
    sensor = GroveTouchSensor(pin16)

    display.clear()
    display.show('>')
    
    while True:
        if button_b.was_pressed():
            break
        
        if sensor.is_pressed():
            print('Pressed')
        else:
            print('Not Pressed')
        
        sleep(500)
        
        
if __name__ == '__main__':
    demo()
