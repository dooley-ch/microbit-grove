# ------------------------------------------------------------------------------------------
# Copyright James A. Dooley 2021.
#
# Distributed under the MIT License.
# (See accompanying file license.md file or copy at http://opensource.org/licenses/MIT)
#
# ------------------------------------------------------------------------------------------

# Light does not work, seems that it is not compatible with the neopixel library

from microbit import pin15, pin16, sleep
from utime import ticks_ms, ticks_diff
import neopixel

from utime import sleep_us

_DEBOUNCE_DELAY = 50
_PIXEL_COUNT    = 60
_HIGH           = 1
_LOW            = 0

class GroveMechKeycap:
    def __init__(self, button_pin, led_pin):
        self._button_pin = button_pin
        self._pixel = neopixel.NeoPixel(led_pin, _PIXEL_COUNT)
        self._button_state = None
        self._last_button_state = None
        self._last_debounce_time = None
        self._led_state = None
                            
        self._pixel.clear()
        self._pixel.show()
        
    def is_pressed(self):
        reading = self._button_pin.read_digital()
        
        if reading != self._last_button_state:
            self._last_debounce_time = ticks_ms()
    
        if ticks_diff(ticks_ms(), self._last_debounce_time) > _DEBOUNCE_DELAY:
            if reading != self._button_state:
                self._button_state = reading
    
        self._last_button_state = reading
        
        return (self._button_state == _HIGH)
    
    def fill(red, green, blue):
        self._pixel.fill((red, green, blue))
        self._pixel.show()
        
def demo():
    button = GroveMechKeycap(pin16, pin15)
    
    while True:
        if button.is_pressed():
            button.fill(200, 200, 200)
            print('Button On')
        else:
            button.fill(255, 255, 255)
            print('Button Off')
            
        sleep(1000)

if __name__ == '__main__':
    demo()
