# ------------------------------------------------------------------------------------------
# Copyright James A. Dooley 2021.
#
# Distributed under the MIT License.
# (See accompanying file license.md file or copy at http://opensource.org/licenses/MIT)
#
# ------------------------------------------------------------------------------------------

from microbit import pin15, pin16, sleep, display, button_b
from utime import ticks_ms, ticks_diff

from utime import sleep_us

_DEBOUNCE_DELAY = 50
_HIGH           = 1
_LOW            = 0

class LedButton:
    def __init__(self, button_pin, led_pin):
        self._button_pin = button_pin
        self._led_pin = led_pin
        self._button_state = None
        self._last_button_state = None
        self._last_debounce_time = None
        self._led_state = None
        
        self.off()
        
    def on(self):
        self._led_pin.write_digital(_HIGH)
        self._led_state = True
        
    def off(self):
        self._led_pin.write_digital(_LOW)
        self._led_state = False
        
    def toggle_led(self):
        if self._led_state:
            self.off()
        else:
            self.on()
            
    def is_pressed(self):
        reading = self._button_pin.read_digital()
        
        if reading != self._last_button_state:
            self._last_debounce_time = ticks_ms()
    
        if ticks_diff(ticks_ms(), self._last_debounce_time) > _DEBOUNCE_DELAY:
            if reading != self._button_state:
                self._button_state = reading
    
        self._last_button_state = reading
        
        return (self._button_state == _LOW)
    
def main():
    button = LedButton(pin15, pin16)
    
    display.clear()
    display.show('>')
    
    while True:
        if button_b.was_pressed():
            display.clear()
            break
        
        if button.is_pressed():
            button.on()
        else:
            button.off()

if __name__ == '__main__':
    main()
